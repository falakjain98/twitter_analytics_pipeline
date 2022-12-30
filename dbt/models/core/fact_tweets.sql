{{ config(materialized='view') }}

with cte1 as (
    select * from {{ ref('stg_query_1_data') }}
    UNION ALL
    select * from {{ ref('stg_query_2_data') }}
    UNION ALL
    select * from {{ ref('stg_query_3_data') }}),
cte2 as (
    select * from cte1
    UNION ALL
    select 
        'All Queries' query,
        date,
        count(distinct tweet_count) as tweet_count,
        sum(total_likes) as total_likes,
        sum(total_retweets) as total_retweets,
        round(avg(positive_perc),2) as positive_perc,
        round(avg(neutral_perc),2) as neutral_perc,
        round(avg(negative_perc),2) as negative_perc,
        round(avg(avg_subjectivity),2) as avg_subjectivity
    from cte1
    group by date)
select * from cte2 order by date, query

-- dbt run --select <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}