{{ config(materialized='view') }}

select * from {{ source('staging','query_1_external_table')}}
limit 10