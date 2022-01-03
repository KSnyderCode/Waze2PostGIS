CREATE EXTENSION postgis;

SET timezone = 'America/New_York';

CREATE SCHEMA if not exists w4c;
SET search_path TO w4c,public;

/* Create Tables for Waze Alerts */
create table w4c.alerts(
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
create table w4c.detected_jams (
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
create table w4c.irregularities(
        pk bigserial PRIMARY KEY,
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
        no_thumbsup integer 
);

