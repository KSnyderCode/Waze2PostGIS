# Waze2PostGIS
API Call for Waze For Cities Data Feed and inserts into PostGIS Enabled Database


## Purpose and background
This project is meant to serve to download data from the Waze For Cities datafeed and insert into tables within a PostGIS enabled database. This will allow for integration with desktop-based GIS software. The SQL script will create the schema, tables, indexes, and set the timezone for the database. 

The general overview of the repository is as follows:
-Create Postgres Database (manually)
-Run database initialization script
-Run the datafeed script through CRON every X minutes. 
-Run the duplicate removal script through CRON every X+1 minutes. 

## Python Packages Required

- requests
- psycopg2

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
