import os
import logging

import datetime
from datetime import timezone

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import tweepy
import pandas as pd

from google.cloud import storage
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator
import pyarrow.csv as pv
import pyarrow.parquet as pq

import config
from sentiment_analysis import *

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/home/falakjain/twitter_analytics_pipeline/api_data/")
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET","tweets")

QUERY_1_TEMPLATE = 'crypto lang:en -is:retweet'
QUERY_2_TEMPLATE = 'storm OR flood lang:en -is:retweet'
QUERY_3_TEMPLATE = 'climate change lang:en -is:retweet'
START_TIME_TEMPLATE = '{{ (execution_date-macros.timedelta(days=1)).strftime(\'%Y-%m-%d\') }}T00:00:00Z'
END_TIME_TEMPLATE = '{{ execution_date.strftime(\'%Y-%m-%d\') }}T00:00:00Z'
INPUT_FILETYPE = 'parquet'

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 3,
}

def get_tweets(query, start_time, end_time,output_path):
    # output fields
    fields = ['id','tweet','date','likes','RTs','lang']
    df = pd.DataFrame(columns = fields)
    
    # tweepy client
    client = tweepy.Client(bearer_token = config.bearer_token,wait_on_rate_limit = True)

    # run paginated search to extract all tweet
    for tweet in tweepy.Paginator(
                client.search_recent_tweets, query=query,max_results = 100,
                start_time = start_time, end_time = end_time, 
                tweet_fields = ['created_at','lang','public_metrics']).flatten():
        # only parse english tweets
        if tweet.lang == 'en':
            df = df.append(
                pd.DataFrame([[tweet.id,
                               tweet.text,
                               tweet.created_at,
                               tweet.public_metrics['like_count'],
                               tweet.public_metrics['retweet_count'],
                               tweet.lang]],columns = fields))
    
    # write to parquet file
    df.to_parquet(output_path)
    
# udf to perform sentiment_analysis
def perform_sentiment_analysis(output_path):
    # read python file
    df = pd.read_parquet(output_path)
    
    # clean data and perform sentiment analysis
    df = clean_data_nlp(df)
    
    # test
    print(df.head())
    
    # write to parquet file
    df.to_parquet(output_path)
    
def upload_to_gcs(bucket, object_name, local_file):
    client_gcs = storage.Client()
    bucket = client_gcs.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)

# NOTE: DAG declaration - using a Context Manager (an implicit way)
def download_nlp_upload_dag(
    dag,
    query_template,
    start_time_template,
    end_time_template,
    local_path_template,
    gcs_path_template,
    table_id,
    gcs_parent_folder,
):
    with dag:
        download_dataset_task = PythonOperator(
            task_id="api_call_data",
            python_callable=get_tweets,
            op_kwargs={
                "query": query_template,
                "start_time" : start_time_template,
                "end_time" : end_time_template,
                "output_path" : local_path_template
            },
        )
        
        perform_nlp_save = PythonOperator(
            task_id="perform_sentiment_analysis",
            python_callable=perform_sentiment_analysis,
            op_kwargs={
                "output_path" : local_path_template
            },
        )
        
        local_to_gcs_task = PythonOperator(
            task_id="local_to_gcs_task",
            python_callable=upload_to_gcs,
            op_kwargs={
                "bucket": BUCKET,
                "object_name": gcs_path_template,
                "local_file": local_path_template,
            },
        )
        
        # Remove file for local folder to reduce storage
        rm_task = BashOperator(
            task_id = "rm_task",
            bash_command = f"rm {local_path_template}"
        )
        
        # Creating BigQuery External Table
        bq_external_table_task = BigQueryCreateExternalTableOperator(
            task_id=f"bq_external_table_task",
            table_resource={
                "tableReference": {
                    "projectId": PROJECT_ID,
                    "datasetId": BIGQUERY_DATASET,
                    "tableId": table_id,
                },
                "externalDataConfiguration": {
                    "autodetect": "True",
                    "sourceFormat": f"{INPUT_FILETYPE.upper()}",
                    "sourceUris": [f"gs://{BUCKET}/raw_tweets/{gcs_parent_folder}/*"],
                },
            },
        )

        download_dataset_task >> perform_nlp_save >> local_to_gcs_task >> rm_task >> bq_external_table_task

# Assign date variable
date = datetime.datetime.now(timezone.utc)-datetime.timedelta(days=5)

# Run dag for Query 1
query_1_dag = DAG(
    dag_id="query_1_data",
    schedule_interval="0 0 * * *",
    start_date=datetime.datetime(date.year, date.month, date.day),
    default_args=default_args,
    catchup=True,
    max_active_runs=3,
    tags=['tweets_de'],
)

download_nlp_upload_dag(
    dag = query_1_dag,
    query_template = QUERY_1_TEMPLATE,
    start_time_template = START_TIME_TEMPLATE,
    end_time_template = END_TIME_TEMPLATE,
    local_path_template = AIRFLOW_HOME + '/query_1_data_{{ execution_date.strftime(\'%Y-%m-%d\') }}.parquet',
    gcs_path_template = "raw_tweets/query_1_data/{{ execution_date.strftime(\'%Y-%m-%d\') }}.parquet",
    table_id="query_1_external_table",
    gcs_parent_folder="query_1_data"
)

# Run dag for Query 2
query_2_dag = DAG(
    dag_id="query_2_data",
    schedule_interval="0 0 * * *",
    start_date=datetime.datetime(date.year, date.month, date.day),
    default_args=default_args,
    catchup=True,
    max_active_runs=3,
    tags=['tweets_de'],
)

download_nlp_upload_dag(
    dag = query_2_dag,
    query_template = QUERY_2_TEMPLATE,
    start_time_template = START_TIME_TEMPLATE,
    end_time_template = END_TIME_TEMPLATE,
    local_path_template = AIRFLOW_HOME + '/query_2_data_{{ execution_date.strftime(\'%Y-%m-%d\') }}.parquet',
    gcs_path_template = "raw_tweets/query_2_data/{{ execution_date.strftime(\'%Y-%m-%d\') }}.parquet",
    table_id="query_2_external_table",
    gcs_parent_folder="query_2_data"
)

# Run dag for Query 3
query_3_dag = DAG(
    dag_id="query_3_data",
    schedule_interval="0 0 * * *",
    start_date=datetime.datetime(date.year, date.month, date.day),
    default_args=default_args,
    catchup=True,
    max_active_runs=3,
    tags=['tweets_de'],
)

download_nlp_upload_dag(
    dag = query_3_dag,
    query_template = QUERY_3_TEMPLATE,
    start_time_template = START_TIME_TEMPLATE,
    end_time_template = END_TIME_TEMPLATE,
    local_path_template = AIRFLOW_HOME + '/query_3_data_{{ execution_date.strftime(\'%Y-%m-%d\') }}.parquet',
    gcs_path_template = "raw_tweets/query_3_data/{{ execution_date.strftime(\'%Y-%m-%d\') }}.parquet",
    table_id="query_3_external_table",
    gcs_parent_folder="query_3_data"
)

