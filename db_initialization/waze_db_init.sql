CREATE EXTENSION postgis;

SET timezone = 'America/New_York';

CREATE SCHEMA if not exists staging;
SET search_path TO staging,public;

/* Create Tables for Waze Alerts */
create table staging.alerts(
        pk bigserial PRIMARY KEY, 
        time_stamp timestamp, 
        geom geometry(point, 4326),  --This may need to be 'geometry'
        magvar integer,
        alert_type varchar,
        subtype varchar,
        report_description varchar, 
        street varchar,
        city varchar,
        country varchar,
        road_type integer,
        report_rating integer,
        uuid varchar NOT NULL,
        confidence integer,
        reliability integer,
        no_thumbsup integer 
);

/* Create Table for Waze Detected Jams */
create table staging.detected_jams(
        pk BIGSERIAL PRIMARY KEY,
        id bigint,
        time_stamp timestamp,
        geom geometry(linestring, 4326), --this may need to be geometry
        street varchar,
        city varchar, 
        country varchar,
        jam_speed float,
        jam_speed_mph float,
        jam_length integer,
        jam_length_ft float,  --revise column name
        delay_seconds integer, --revise column name
        delay_minutes float,
        road_type integer,
        start_node varchar,
        end_node varchar, 
        jam_level integer,
        uuid varchar NOT NULL, --bigint?
        blocking_alert_uuid varchar, 
        turn_line geometry(linestring, 4326), --double check, needs to be pairs of coordinates
        turn_type varchar
);

/* Create Table for Waze Irregularities */
create table staging.irregularities(
        pk bigserial PRIMARY KEY,
        id bigint, --double check
        geom geometry(linestring, 4326), 
        detection_date timestamp,
        update_date varchar(50),
        irregularity_type varchar(15),
        start_node varchar(40),
        end_node varchar(40),
        speed float,
        speed_mph float,
        delay_seconds float, --delay in seconds from regular speed
        delay_minutes float, 
        jam_length integer, --assuming the irregularity is in meters
        jam_length_ft float,
        jam_trend integer, 
        street varchar,
        city varchar,
        country varchar, 
        jam_severity float, 
        jam_level integer,
        highway varchar, --changed from boolean to varchar 
        drivers_count integer, 
        alerts_count integer,
        no_thumbsup integer 
);

-- Create table script for traffic view API irregularities
create table staging.traffic_view_routes(
        pk bigserial PRIMARY KEY,
        route_name varchar,
        to_name varchar,
        from_name varchar,
        historic_time integer,
        current_travel_time varchar,
        jam_level integer,
        jam_length integer,
        jam_length_ft float,
        route_id integer,
        route_type varchar,
        travel_time_index float,
        geom geometry(linestring, 4326)
);

CREATE SCHEMA if not exists production;
SET search_path TO production,public;

/* Create Tables for Waze Alerts */
create table production.alerts(
        time_stamp timestamp, 
        geom geometry(point, 4326),  --This may need to be 'geometry'
        magvar integer,
        alert_type varchar,
        subtype varchar,
        report_description varchar, 
        street varchar,
        city varchar,
        country varchar,
        road_type integer,
        report_rating integer,
        uuid varchar NOT NULL,
        confidence integer,
        reliability integer,
        no_thumbsup integer,
        municipality varchar,
        county varchar,
        travel_dir varchar
);

/* Create Table for Waze Detected Jams */
create table production.detected_jams(
        id bigint,
        time_stamp timestamp,
        geom geometry(linestring, 4326), --this may need to be geometry
        street varchar,
        city varchar, 
        country varchar,
        jam_speed float,
        jam_speed_mph float,
        jam_length integer,
        jam_length_ft float,  --revise column name
        delay_seconds integer, --revise column name
        delay_minutes float,
        road_type integer,
        start_node varchar,
        end_node varchar, 
        jam_level integer,
        uuid varchar NOT NULL, --bigint?
        blocking_alert_uuid varchar, 
        turn_line geometry(linestring, 4326), --double check, needs to be pairs of coordinates
        turn_type varchar,
        jam_muni varchar,
        jam_county varchar,
        travel_dir varchar
        travel_azimuth integer
);

/* Create Table for Waze Irregularities */
create table production.irregularities(
        id bigint, --double check
        geom geometry, 
        detection_date timestamp,
        update_date varchar(50),
        irregularity_type varchar(15),
        start_node varchar(40),
        end_node varchar(40),
        speed float,
        speed_mph float,
        delay_seconds float, --delay in seconds from regular speed
        delay_minutes float, 
        jam_length integer, --assuming the irregularity is in meters
        jam_length_ft float,
        jam_trend integer, 
        street varchar,
        city varchar,
        country varchar, 
        jam_severity float, 
        jam_level integer,
        highway varchar, --changed from boolean to varchar 
        drivers_count integer, 
        alerts_count integer,
        no_thumbsup integer,
        irreg_muni varchar,
        irreg_county varchar,
        travel_dir varchar,
        travel_azimuth integer
);

create table production.traffic_view_routes(
        route_name varchar,
        to_name varchar,
        from_name varchar,
        historic_time integer,
        current_travel_time varchar,
        jam_level integer,
        jam_length integer,
        jam_length_ft float,
        route_id integer,
        route_type varchar,
        travel_time_index float,
        geom geometry(linestring, 4326),
        route_muni varchar,
        route_county varchar,
        travel_azimuth integer,
        travel_dir varchar
);

