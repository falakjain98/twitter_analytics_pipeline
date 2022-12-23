import os
import logging

import datetime

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

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
client = tweepy.Client(bearer_token = config.bearer_token)

QUERY_1_TEMPLATE = 'FIFA2022 -is:retweet'
START_TIME_TEMPLATE = '{{ (execution_date-macros.timedelta(days=1)).strftime(\'%Y-%m-%d\') }}T00:00:00Z'
END_TIME_TEMPLATE = '{{ execution_date.strftime(\'%Y-%m-%d\') }}T00:00:00Z'
LOCAL_PATH_TEMPLATE = AIRFLOW_HOME + '/query_1_data_{{ execution_date.strftime(\'%Y-%m-%d\') }}.parquet.gzip'

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
}

def get_tweets(query, start_time, end_time,output_path):
    # output fields
    fields = ['id','tweet','date','source','likes','RTs','lang']
    df = pd.DataFrame(columns = fields)

    # run paginated search to extract all tweet
    for tweet in tweepy.Paginator(
                client.search_recent_tweets, query=query,max_results = 10,
                start_time = start_time, end_time = end_time, 
                tweet_fields = ['created_at','lang','public_metrics']).flatten(limit=10):
        # only parse english tweets
        if tweet.lang == 'en':
            df = df.append(
                pd.DataFrame([[tweet.id,
                               tweet.text,
                               tweet.created_at,
                               tweet.source,
                               tweet.public_metrics['like_count'],
                               tweet.public_metrics['retweet_count'],
                               tweet.lang]],columns = fields))
    
    # write to parquet gzipped file
    print(df.head())
    df.to_parquet(output_path, compression = 'gzip')

# NOTE: DAG declaration - using a Context Manager (an implicit way)
def download_nlp_upload_dag(
    dag,
    query_template,
    start_time_template,
    end_time_template,
    local_path_template
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

        download_dataset_task

# Run dag for yellow taxi
query_1_dag = DAG(
    dag_id="query_1_data",
    schedule_interval="0 0 * * *",
    start_date=datetime.datetime(2022, 12, 19),
    end_date=datetime.datetime(2022, 12, 20),
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
    local_path_template = LOCAL_PATH_TEMPLATE,
)


