{{ config(materialized='view') }}

select 
    'Query 1' as query,
    cast(id as integer) as id,
    FORMAT_DATE('%Y-%m-%d', cast(date as timestamp)) as date,
    cast(likes as integer) as likes,
    cast(RTs as integer) as retweets,
    cast(score as numeric) as score,
    cast(sentiment as integer) as sentiment,
    cast(subjectivity as numeric) as subjectivity

from {{ source('staging','query_1_external_table')}}

-- dbt run --select <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

  limit 10

{% endif %}