# Waze2PostGIS
API Call for Waze For Cities Data Feed and inserts into PostGIS Enabled Database


## Purpose and background
This project is meant to serve to download data from the Waze For Cities datafeed and insert into tables within a PostGIS enabled database. This will allow for integration with desktop-based GIS software. The SQL script will create the schema, tables, indexes, and set the timezone for the database. 

The general overview of the script implementation is as follows:
1. Create Postgres Database (manually)
2. Run database initialization script
3. Run the datafeed script through CRON every X minutes. 
4. Run the duplicate removal script through CRON every X+1 minutes. 

### Flow of the "datafeed" script

1. Prints opening statement and initiates a timestamp
2. Establishes an autocommit database connection to the PostgreSQL/PostGIS database you created
3. Performs an API call, converts it from JSON to python dictionary, and then inserts into the database
    - This does this 3 times for each different layer in the Waze API:
        - Alerts (User generated incidents) which are POINT geometries
        - Detected traffic jams which are LINESTRING geometries
        - Traffic Irregularities which are LINESTRING geometries
4. Closes database connection and psycopg2 cursor
5. Prints final time stamp


### Flow of the "duplicate removal" script

1. Prints opening statement and initiates a timestamp
2. Establishes an autocommit database connection to the PostgreSQL/PostGIS database you created
3. Compares the Alerts and Detected Jams tables to a digital duplicate of each respective table deletes the more recent inputted version of any duplicate event based on the Waze UUID/ID. 
4. Closes database connection and psycopg2 cursor
5. Prints final time stamp

## Python Packages Required

This is a fairly "light" script in terms of packages required. I used the Anaconda program (Conda) to install *requests* and *psycopg2*, but you can use PIP as well. 

- requests (will need to be installed using PIP or Conda)
- psycopg2 (will need to be installed using PIP or Conda)
    - If you use PIP then the package is psycopg2-binary
- datetime (standard library)
- json (standard library)

## The future of this project

This is a "first draft" of this project. I wanted to get this code out there for any other Waze For Cities Partners who are seeking a server based implementation. 

I do have a few "future feature" items I'd like to add over time:

1. Refactor code to increase readability and efficiency
2. Create a Microsoft SQL Server version to increase compatible software
3. Drop psycopg2 and use an Object Relational Mapper like SQLAlchemy



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
