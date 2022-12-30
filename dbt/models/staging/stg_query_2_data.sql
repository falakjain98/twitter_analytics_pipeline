{{ config(materialized='view') }}

WITH query1_data AS
(
    select 
        'Query 2' as query,
        cast(id as integer) as id,
        FORMAT_DATE('%Y-%m-%d', cast(date as timestamp)) as date,
        cast(likes as integer) as likes,
        cast(RTs as integer) as retweets,
        cast(score as numeric) as score,
        cast(sentiment as integer) as sentiment,
        cast(subjectivity as numeric) as subjectivity

    from {{ source('staging','query_2_external_table')}})

select
    query,
    date,
    count(distinct id) as tweet_count,
    sum(likes) as total_likes,
    sum(retweets) as total_retweets,
    round(sum(IF(sentiment = 2,1,0))*100/count(distinct id),2) as positive_perc,
    round(sum(IF(sentiment = 1,1,0))*100/count(distinct id),2) as neutral_perc,
    round(sum(IF(sentiment = 0,1,0))*100/count(distinct id),2) as negative_perc,
    avg(subjectivity) as avg_subjectivity
from query2_data
group by query, date

-- dbt run --select <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}