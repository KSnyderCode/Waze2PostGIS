# Waze2PostGIS
API Call for Waze For Cities Data Feed and inserts into PostGIS Enabled Database


## Purpose and background
This project is meant to serve to download data from the Waze For Cities datafeed and insert into tables within a PostGIS enabled database. This will allow for integration with desktop-based GIS software. The SQL script will create the schema, tables, indexes, and set the timezone for the database. 

## Python Packages Required

- requests
- psycopg2
