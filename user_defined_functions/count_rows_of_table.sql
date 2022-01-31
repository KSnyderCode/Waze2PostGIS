/* Original Script pulled from: 
https://blog.yugabyte.com/row-counts-of-tables-in-a-sql-schema-database-postgresql-yugabytedb/ */
create function count_rows_of_table(
  schema    text,
  tablename text
  )
  returns   integer

  security  invoker
  language  plpgsql
as
$body$
declare
  query_template constant text not null :=
    '
      select count(*) from "?schema"."?tablename"
    ';

  query constant text not null :=
    replace(
      replace(
        query_template, '?schema', schema),
     '?tablename', tablename);

  result int not null := -1;
begin
  execute query into result;
  return result;
end;
$body$;