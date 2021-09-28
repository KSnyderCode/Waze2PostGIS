/* TCRPC Implementation for W4C Datafeed */
/* 2021 */

/*Enables PostGIS on database */
create extension postgis;

/* Setting timezone to NY Timezone for timestamp Data Type */
SET timezone = 'America/New_York';

/* Create Schema for Waze data */
create schema if not exists w4c;
SET search_path TO w4c,public;

/* Create Tables for Waze Alerts */
create table w4c.alerts(
        pk bigserial primary key, 
        time_stamp timestamp, 
        geom geometry(point, 4326),  --This may need to be 'geometry'
        magvar integer,
        alert_type varchar(25),
        subtype varchar(40),
        report_description varchar(500), 
        street varchar(80),
        city varchar(80),
        country varchar(2),
        road_type integer,
        report_rating integer,
        uuid varchar(40) NOT NULL,
        confidence integer,
        reliability integer,
        no_thumbsup integer 
);

/* Create Table for Waze Detected Jams */
create table w4c.detected_jams (
        pk bigserial primary key,
        id bigint,
        time_stamp timestamp,
        geom geometry (linestring, 4326), --this may need to be geometry
        street varchar(80),
        city varchar(80), 
        country varchar(2),
        jam_speed float,
        jam_speed_mph float,
        jam_length integer,
        jam_length_ft float,  --revise column name
        delay_seconds integer, --revise column name
        delay_minutes float,
        road_type integer,
        start_node varchar(80),
        end_node varchar(80), 
        jam_level integer,
        uuid varchar(40) NOT NULL, --bigint?
        blocking_alert_uuid varchar(40), 
        turn_line geometry(linestring,4326), --double check, needs to be pairs of coordinates
        turn_type varchar(25)
);

/* Create Table for Waze Irregularities */
create table w4c.irregularities(
        pk bigserial primary key,
        id bigint, --double check
        geom geometry (linestring, 4326), 
        detection_date timestamp,
        update_date timestamp,
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
        street varchar(60),
        city varchar(40),
        country varchar(2), 
        jam_severity float, 
        jam_level integer,
        highway boolean, 
        drivers_count integer, 
        alerts_count integer,
        no_thumbsup integer 
);

CREATE INDEX alerts_geom_idx
    ON w4c.alerts
    USING GIST (geom);

CREATE INDEX jams_geom_idx
    ON w4c.detected_jams
    USING GIST (geom);

CREATE INDEX irreg_geom_idx
    ON w4c.irregularities
    USING GIST (geom);

/*
--Alerts table column comments 
comment on column w4c.alerts.pk is 'Serial Primary Key';
comment on column w4c.alerts.time_stamp is 'Publication date (Unix time – milliseconds since epoch) converted using python datetime package';
comment on column w4c.alerts.geom is 'Point location for the report (WGS84)':
comment on column w4c.alerts.uuid is 'Unique system ID for each alert';
comment on column w4c.alerts.magvar is 'Event direction (Driver heading at time of report. 0 degrees at North, according to driver's device)'; 
comment on column w4c.alerts.alert_type is 'Type of alert reported. '; 
comment on column w4c.alerts.subtype is 'Event subtype reported'; 
comment on column w4c.alerts.report-discription is 'Primary Key'; 
comment on column w4c.alerts.street is 'Street name (as written in database, no canonical form). Supplied when available.'; 
comment on column w4c.alerts.city is 'City and State name [City, State] in case both are available. [State] if not associated with a city. Supplied when available.'; 
comment on column w4c.alerts.road_type is 'Integer road type'; 
comment on column w4c.alerts.report_rating is 'Integer value on the report? Not clearly identified in Waze API documentation.'; 
comment on column w4c.alerts.uuid is 'Unique identifier value for '; 
comment on column w4c.alerts.confidence is 'Confidence rating in the report. '; 
comment on column w4c.alerts.reliability is 'Reliability based on the Wazer's accrued points.';
comment on column w4c.alerts.no_thumbsup is 'Number of thumbs up by users';  

--Jams table column comments 
comment on column w4c.detected_jams.pk is 'Serial primary key':
comment on column w4c.detected_jams.id is 'Waze assigned ID for the jam';
comment on column w4c.detected_jams.time_stamp is 'Publication date (Unix time – milliseconds since epoch) converted using python datetime package';
comment on column w4c.detected_jams.alert_type is 'Primary Key'; --need to revise for geometry column
comment on column w4c.detected_jams.geom is 'Linestring geometry of the traffic jam (WGS84)';
comment on column w4c.detected_jams.speed is 'Current average speed on a jammed segment in meters/second'; 
comment on column w4c.detected_jams.jam_length is 'Jam length in meters'; 
comment on column w4c.detected_jams.delay_seconds is 'Delay of jam compared to free flow speed, in seconds (in case of block, -1)'; 
comment on column w4c.detected_jams.street is 'Street name (as written in database, no canonical form). Supplied when available.'; 
comment on column w4c.detected_jams.city is 'City and State name [City, State] in case both are available. [State] if not associated with a city. Supplied when available.'; 
comment on column w4c.detected_jams.country is 'Two letter country code.'; 
comment on column w4c.detected_jams.road_type is 'Integer road type'; 
comment on column w4c.detected_jams.start_node is 'Nearest junction/city/street to jam start. Supplied when available.'; 
comment on column w4c.detected_jams.end_node is 'Nearest junction/city/street to jam end. Supplied when available.'; 
comment on column w4c.detected_jams.level is 'Level of traffic congestion (0 = free flow, 5 = blocked).'; 
comment on column w4c.detected_jams.uuid is 'Unique jam ID'; 
comment on column w4c.detected_jams.turn_line is 'A set of coordinates of a turn - only when the jam is in a turn. Supplied when available.'; 
comment on column w4c.detected_jams.turn_type is 'Type of turn if the jam occurs in a turn. Options are: left, right, exit R or L, continue straight, or NONE. Supplied when available. '; 
comment on column w4c.detected_jams.blocking_alert_uuid is 'If jam is connected to a block.'; 

--Irregularities table column comments 
comment on column w4c.irregularities.id is 'Identified for irregularity'; 
comment on column w4c.irregularities.pub_millis is 'Publication date (Unix time – milliseconds since epoch)';
comment on column w4c.irregularities.detection_date is 'Date timestamp for the traffic irregularity'; 
comment on column w4c.irregularities.detection_date_millis is 'Date of irregularity (in milliseconds)';
comment on column w4c.irregularities.update_date is 'Last update'; 
comment on column w4c.irregularities.update_date_millis is 'Last update. Time in milliseconds.'; 
comment on column w4c.irregularities.geom is 'Linestring geometry of the traffic irregularity. WGS84. '; 
comment on column w4c.irregularities.type is 'Irregularity type: None(0), Small(1), Medium(2), Large (3), Huge(4)'; 
comment on column w4c.irregularities.speed is 'Traffic speed in the irregularity'; 
comment on column w4c.irregularities.regular_speed is 'Historical regular speed in the segment'; 
comment on column w4c.irregularities.delay_seconds is 'Delay in seconds from the regular speed'; 
comment on column w4c.irregularities.seconds is 'Current traffic speed'; 
comment on column w4c.irregularities.irregularity_length is 'Length of the traffic irregularity in meters.'; --presumed to be meters 
comment on column w4c.irregularities.trend is 'Trend of the traffic irregularity: -1 = improving, 0 = constant, 1 = getting worse'; 
comment on column w4c.irregularities.street is 'Street name (as written in database, no canonical form). Supplied when available.'; 
comment on column w4c.irregularities.city is 'City and State name [City, State] in case both are available. [State] if not associated with a city. Supplied when available.'; 
comment on column w4c.irregularities.country is 'Two letter country code.'; 
comment on column w4c.irregularities.severity is 'Calculated severity of the traffic irregularity (0-5). 5 is the most severe.';
comment on column w4c.irregularities.jam_level is 'Indicator of the traffic irregularity severity (1-4). 4 is the most severe.'; 
comment on column w4c.irregularities.drivers_count is 'Number of Wazers in the irregularity.'; 
comment on column w4c.irregularities.alerts_count is 'How many alerts from Wazers in irregularity segments.';  
*/
