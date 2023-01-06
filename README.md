# Twitter Analytics Pipeline

### Project Summary

This repository will allow you to deploy your own analytics pipeline for your chosen [twitter API queries](https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query) in a few quick steps. You will need to register for a [Twitter Developer Account](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api) in order to receive authorization for API calls.

The following technologies are utilized in this project:
- [GCP Services](https://cloud.google.com/): *Cloud platform*
  - [Compute Engine](https://cloud.google.com/compute): *Virtual Machine*
  - [Cloud Storage](https://cloud.google.com/storage): *Data Lake*
  - [BigQuery](https://cloud.google.com/bigquery): *Data Warehouse*
- [Terraform](https://developer.hashicorp.com/terraform/downloads): *Infrastructure-as-Code (IaC)*
- [Docker](https://www.docker.com): *Containerization*
- [dbt](https://cloud.getdbt.com): *Data Transformation*
- [Python (via Anaconda)](https://www.anaconda.com/products/distribution): *Programming Language*
- SQL: *Data Analysis*

### Project Architecture

<img width="900" alt="image" src="https://user-images.githubusercontent.com/54712290/210926048-9b9f0c75-2918-4022-9073-7e07a7f557f1.png">

### Dashboard

The analytics dashboard which utilizes this pipeline can be viewed at https://datastudio.google.com/reporting/07fdca1d-a669-4356-acc5-3b2a4faaabb0/page/DrhBD.

The data can be filtered by date and query in order to customize analysis

Metrics Displayed (for each query and total):
1. Change in daily number of tweets
2. Change in daily % of positive, negative and neutral tweets
3. Total number of tweets, likes and retweets based on date range selection
4. Average tweet sentiment based on date range selection

### Setup & Deploy
Please refer to [setup](setup.md) file for more details regarding infrastructure setup.

After setup, deploy the pipeline using steps on the [deploy](deploy.md) file.

### Learn More
To learn more about Data and Analytics Engineering, check out [DataTalksClub's](https://github.com/DataTalksClub) amazing [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp)!
