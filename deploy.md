# Deploying a live pipeline for your desired Twitter API Queries

### Please follow the following steps after [setting up](setup.md) to deploy the analytics tool

1. SSH into VM `ssh <VM-alias>` after editing config file with VM's external IP

2. Navigate to the terraform directory within the git repo folder `cd twitter_analytics_pipeline/terraform/`

3. Run `terraform init`, `terraform plan` and `terraform apply` to create GCS and BigQuery resources

4. Navigate to the airflow directory within the git repo folder `cd twitter_analytics_pipeline/airflow/`

5. Enter your desired [Twitter API queries](https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query) within `airflow/dags/data-ingestion-nlp-bq-dag.py` and the staging sql codes in `dbt/models/staging'

6. Build docker-compose image `docker-compose build`

7. Initialize docker images `docker-compose up airflow-init` and `docker-compose up -d`

8. Airflow will set up the orchestration of the different tasks in the pipeline and push the raw data retrieved from the API to a dataset in BigQuery
    - DAG progress can be viewed at `localhost:8080` provided port forwarding is enabled

9. Create a [dbt](https://cloud.getdbt.com) account, set up a project by cloning this repo and using google credentails, in project settings point to /dbt subdirectory

10. Deploy a dbt production model to run on a schedule with `dbt run --var 'is_test_run: false'` command

11. The dbt model will create a BigQuery table with aggregated data which can be accessed using a report from [Google Data Studio](https://lookerstudio.google.com/overview) by connecting to a BigQuery data source

12. Using this data source, a live report can be set up according to user preference

### Steps to shut down pipeline
1. Kill docker images `docker-compose down`

2. Navigate to the terraform directory within the git repo folder `cd twitter_analytics_pipeline/terraform/`

3. Run `terraform destroy` to destroy GCS and BigQuery resources

4. Switch off VM using `sudo shutdown now` to avoid charges
