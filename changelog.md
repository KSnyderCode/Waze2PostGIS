# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) or as close to
semantic versioning as possible.

## [Unreleased]
### Future Features
1. Refactor code to increase readability and efficiency
2. Drop psycopg2 and use an Object Relational Mapper (ORM) like SQLAlchemy
3. Add additional views. 

## [0.3.0] -2022-1-11
### Added
- A "staging" schema. Data will bed fed into this from the data feed python script.
- A "production" schema. This will serve as the "forward-facing" schema which GIS and PowerBI connect to. Data will be rolled into this using the "production_rollover.sql" script. 
- Data rollover script to push data to the production schema from the staging schema. Does not allow duplicates to be rolled into the database. 
- Created trigger functions to automatically assign either the alert point, or the starting point (for detected jams and irregularities) into the corresponding municipality and county. 
    - This uses ST_Intersects / ST_StartPoint functions from PostGIS
- A SQL script to create GIST indexes on Alerts, Detected Jams, and Irregularities in the production schema. Spatial indexes should be updated as the data is loaded in. 
- Created a few views just for basic understanding of alerts. 

### Changed
- Added duplicate removal funcationality directly into the data feed script. It will call the API, add into the database, and then remove any duplicates. 

### Removed
- Removed reindexing script. No need to have a spatial index on a staging table. 
- Removed logging. Not needed for for our server. 

## [0.2.1] -2021-09-01
### Changed
- Finalized logging features

## [0.2.0] -2021-09-01
### Added
- Created changelog and assigned minor versions
- Added logging functionality to output to "waze_ingestion.log"

### Changed
- Moved future feature wishlist to the changelog in the "Unreleased" feature section
- Cleaned up some formatting, removed extra white space

### Removed
- Removed all print statements from program

## [0.1.1] -2021-08-16
### Changed
- Updated the README to provide more in-depth information on script workflow and overall implementation
- Added wishlist of future features into the README

## [0.1.0] -2021-08-15
### Added
- Initial commit to Github


