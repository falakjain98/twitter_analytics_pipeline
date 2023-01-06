# Deploying a live pipeline for your desired Twitter API Queries

### Please follow the following steps after [setting up](setup.md) to deploy the analytics tool

1. SSH into VM `ssh <VM-alias>` after editing config file with VM's external IP
2. Navigate to the terraform directory within the git repo folder `cd twitter_analytics_pipeline/terraform/`
3. Run `terraform init`, `terraform plan` and `terraform apply` to create GCS and BigQuery resources
4. Navigate to the airflow directory within the git repo folder `cd twitter_analytics_pipeline/airflow/`
5. Enter your desired [Twitter API queries](https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query) within `dags/data-ingestion-nlp-bq-dag.py`
6. Build docker-compose image `docker-compose build`
7. Initialize docker images `docker-compose up airflow-init` and `docker-compose up -d`
8. Airflow will set up the orchestration of the different tasks in the pipeline and push the raw data retrieved from the API to a dataset in BigQuery
9. You can then utilize [dbt](dbt.md) to aggregate and visualize the data using different visualization tools. I have used Google Data Studio in this project

### Steps to shutdown pipeline
1. Kill docker images `docker-compose down`
2. Navigate to the terraform directory within the git repo folder `cd twitter_analytics_pipeline/terraform/`
3. Run `terraform destroy` to destroy GCS and BigQuery resources
4. Switch off VM using `sudo shutdown now` to avoid charges
