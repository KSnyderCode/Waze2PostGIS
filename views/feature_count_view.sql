CREATE VIEW feature_count AS
select
  table_schema,
  table_name,
  count_rows_of_table(table_schema, table_name)
from
  information_schema.tables
where 
  table_schema IN ('production', 'staging')
  and table_name != ('municipalities')
  and table_type = 'BASE TABLE'
order by
  1 asc,
  3 desc;