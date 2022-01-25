# Waze2PostGIS
API Call for Waze For Cities Data Feed and inserts into PostGIS Enabled Database


## Purpose and background
This project is meant to serve to download data from the Waze For Cities datafeed and insert into tables within a PostGIS enabled database. This will allow for integration with desktop-based GIS software. The SQL script will create the schema, tables, indexes, and set the timezone for the database. 

The general overview of the script implementation is as follows:
1. Create Postgres Database (manually)
2. Run database initialization script
3. Execute script for all of the trigger functions to be added into the production schema. 
4. Run the datafeed script through CRON every X minutes. 
5. Run the production_rollover.sql script as needed.  

### Flow of the "datafeed" script

1. Establishes an autocommit database connection to the PostgreSQL/PostGIS database you created
2. Performs an API call, converts it from JSON to python dictionary, and then inserts into the database
    - This does this 3 times for each different layer in the Waze API:
        - Alerts (User generated incidents) which are POINT geometries
        - Detected traffic jams which are LINESTRING geometries
        - Traffic Irregularities which are LINESTRING geometries
        - Irregularities (Traffic View API) which are LINESTRING
3. Removes duplicate records in the staging tables. 
4. Closes database connection and psycopg2 cursor

### Data Rollover

- I've created two database schemas now to hopefully remove any potential issues with database locks. 
- "Staging" is the temporary set of tables which is being updated every 5 minutes by the data feed python script. 
- "Production" is intended to be a more static data set for interaction with GIS and PowerBI (or whatever else you'd like)
- The "Production_Rollover.sql" script is a large INSERT statement to take data from the staging schema and roll it into the production schema. 
    - Currently this is a mannual process, but now the user can determine when production gets updated. 

### Trigger Functions

- There are now trigger functions added into the database which use PostGIS functions:
    - Municipal Boundary: these trigger functions take either the point geometry or the beginning of the line geometry
    and run a spatial intersect to determine what municipality the feature is in 
    - County Boundary: these trigger functions take either the point geometry or the beginning of the line geometry
    and run a spatial intersect to determine what municipality the feature is in
    - Azimuth calculation: This calculates an azimuth (ultimately in degrees) between the start and end of a line geometry to
    determine an angle of travel.
    - Travel Direction: For the alerts table, this is based entirely off of the *magvar* column. For the line features
    the azimuth calculation is what determines the direction of travel. 

## Python Packages Required

This is a fairly "light" script in terms of packages required. I used the Anaconda program (Conda) to install *requests* and *psycopg2*, but you can use PIP as well. 

- requests (will need to be installed using PIP or Conda)
- psycopg2 (will need to be installed using PIP or Conda)
    - If you use PIP then the package is psycopg2-binary
- datetime (standard library)
- json (standard library)

## The future of this project

This is a "working draft" of this project. I wanted to get this code out there for any other Waze For Cities Partners who are seeking a server based implementation. 

I do have a few "future feature" items I'd like to add over time:

1. Refactor code to increase readability and efficiency
2. Drop psycopg2 and use an Object Relational Mapper like SQLAlchemy
3. Get more into PostGIS functions wherever possible. 


## Contributing to this project

If you enjoy this project and would like to contribute, do the following:

1. Fork this respository.
2. Create a new branch: <code>git checkout -b <branch_name></code>.
3. Make your changes and commit them: <code>git commit -m '<commit_name>'</code>.
4. Push to the origin branch: <code>git push origin <project_name></code>.
5. Create a pull request. 

## Contact

If you have questions, please contact me at: ksnyder@tcrpc-pa.org. 

## License

This project uses an MIT License. 
