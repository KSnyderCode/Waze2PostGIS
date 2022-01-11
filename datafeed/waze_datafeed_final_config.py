#!/usr/bin/env python
# coding: utf-8

# waze_data_feed.py
# Copyright 2021 Tri-County Regional Planning Commission

''' import modules / packages '''
import datetime
import json
import requests
import psycopg2
from psycopg2 import Error

''' variables '''


''' define functions '''

# converts api response into json and then into a python dictionary
def json_to_dict(url):
    api_response = requests.get(url)
    response_json = api_response.text
    response_dict = json.loads(response_json)
    return response_dict

# establishes connection to postgis database with an autocommit connection
def db_connection():
    try:
        #connection to PostgreSQL database
        global connection
        connection = psycopg2.connect(user="user",
                                    password="password",
                                    host="localhost / ip address",
                                    port="5432",
                                    database="db_name")
        connection.autocommit = True
        # creating global cursor for database operations
        global cursor
        cursor = connection.cursor()
        # logs success statement after connection established
        return cursor, connection
    except (Exception, Error) as error:
        cursor = db_connection()
        cursor.close()
        connection.close()

def db_connection_close():
    # close cursor command, and close out database connection
    #cursor = db_connection()
    cursor.close()
    #connection = db_connection()
    connection.close()

# function for when exceptions are raised to close out DB connection
def db_exception(table):
    #cursor = db_connection()
    cursor.close()
    #connection = db_connection()
    connection.close()

# calls waze datafeed api and puts point data into postgres table called alerts
def alerts_call():
    alerts_url = ('waze_API_url')

    response_dict = json_to_dict(alerts_url)
    #cursor = db_connection()

    conditions = (["HAZARD_ON_ROAD", "HAZARD_ON_SHOULDER", "HAZARD_ON_SHOULDER_CAR_STOPPED", "HAZARD_ON_ROAD_CAR_STOPPED",
                "HAZARD_ON_ROAD_CAR_POT_HOLE", "HAZARD_ON_ROAD_CAR_ROAD_KILL", "HAZARD_ON_SHOULDER_ANIMALS",
                "HAZARD_WEATHER_FOG", "HAZARD_WEATHER_HAIL","HAZARD_WEATHER_HEAVY_RAIN", "HAZARD_WEATHER_HEAVY_SNOW",
                "HAZARD_WEATHER_HEAT_WAVE", "HAZARD_WEATHER_HURRICANE", "HAZARD_WEATHER_TORNADO","HAZARD_WEATHER_MONSOON",
                "HAZARD_WEATHER_FREEZING_RAIN", "HAZARD_ON_ROAD_ICE","HAZARD_ON_ROAD_OIL", "HAZARD_ON_ROAD_OBJECT", 
                "HAZARD_ON_ROAD_ROAD_KILL", "" ])

    for alert in response_dict['alerts']:
        filter = alert['subtype']
        if filter not in conditions:
            # establishing variables for SQL insert
            time_stamp = datetime.datetime.fromtimestamp(alert['pubMillis'] / 1000)
            geom = ("SRID=4326;POINT(" + str(alert['location']['x']) + " " + str(alert['location']['y']) + ")")
            magvar = alert['magvar']
            alert_type = alert['type']
            subtype = alert['subtype']
            try:
                report_description = alert['reportDescription']
            except:
                report_description = None
            try:
                street = alert['street']
            except:
                street = None
            try:
                city = alert['city']
            except:
                city = None
            try:
                country = alert['country']
            except:
                country = "US"
            try:
                road_type = alert['roadType']
            except:
                road_type = None
            report_rating = alert['reportRating']
            uuid = alert['uuid']
            confidence = alert['confidence']
            reliability = alert['reliability']
            try:
                no_thumbsup = alert['nThumbsUp']
            except:
                no_thumbsup = None

            # SQL insert statement for waze alerts
            try:
                cursor.execute("""
                    INSERT INTO staging.alerts (
                        time_stamp,
                        geom,
                        magvar,
                        alert_type,
                        subtype,
                        report_description,
                        street,
                        city,
                        country,
                        road_type,
                        report_rating,
                        uuid,
                        confidence,
                        reliability,
                        no_thumbsup)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        (time_stamp, geom, magvar, alert_type, subtype, report_description, street,
                        city, country, road_type, report_rating, uuid, confidence,reliability, no_thumbsup))
            except (Exception, Error) as error:
                db_exception("alerts")

# calls waze datafeed api and puts jam linestring data into postgres table called detected_jams
def jams_call():
    jams_url = ('waze_API_url')

    response_dict = json_to_dict(jams_url)
    #cursor = db_connection()

    for jam in response_dict['jams']:

        # establishing all of my variables for SQL insert statement
        id = jam['id']
        time_stamp = datetime.datetime.fromtimestamp(jam['pubMillis'] / 1000)
        try:
            geom_type = ('SRID=4326;LINESTRING(')
            temp_geom = []
            # for loop to convert X, Y pairs
            for coordinate in jam['line']:
                temp_coor = (str(coordinate['x']) + ' ' + str(coordinate['y']))
                temp_geom.append(temp_coor)
            temp_geom_str = ', '.join([str(coor) for coor in temp_geom])
            geom = geom_type + temp_geom_str + ')'
        except:
            geom = None
        jam_speed = jam['speedKMH']
        jam_speed_mph = jam['speedKMH'] / 1.609
        jam_length = jam['length']
        jam_length_ft = jam['length'] * 3.2804
        delay_seconds = jam['delay']
        delay_minutes = jam['delay'] / 60
        try:
            street = jam['street']
        except:
            street = None
        try:
            city = jam['city']
        except:
            city = None
        try:
            country = jam['country']
        except:
            country = "US"
        try:
            road_type = jam['roadType']
        except:
            road_type = None
        try:
            start_node = jam['startNode']
        except:
            start_node = None
        try:
            end_node = jam['endNode']
        except:
            end_node = None
        jam_level = jam['level']
        uuid = jam['uuid']
        try:
            blocking_alert_uuid = jam['blockingAlertUuid']
        except:
            blocking_alert_uuid = None
        try:
            for coordinate in response_dict['segments']:
                geom_type = ('SRID=4326;LINESTRING(')
                temp_geom = []
                temp_coor = (str(coordinate['x']) + ' ' + str(coordinate['y']))
                temp_geom.append(temp_coor)
            temp_geom_str = ','.join([str(coor) for coor in temp_geom])
            turn_line = geom_type + temp_geom_str + ')'
        except:
            turn_line = None
        turn_type = jam['turnType']

        # SQL insert statement for waze detected jams
        try:
            cursor.execute("""
                INSERT INTO staging.detected_jams (
                    id,
                    time_stamp,
                    geom,
                    street,
                    city,
                    country,
                    jam_speed,
                    jam_speed_mph,
                    jam_length,
                    jam_length_ft,
                    delay_seconds,
                    delay_minutes,
                    road_type,
                    start_node,
                    end_node,
                    jam_level,
                    uuid,
                    blocking_alert_uuid,
                    turn_line,
                    turn_type)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (id, time_stamp, geom, street, city, country, jam_speed, jam_speed_mph, jam_length, jam_length_ft,
                    delay_seconds, delay_minutes, road_type, start_node, end_node, jam_level, uuid, blocking_alert_uuid,
                    turn_line, turn_type))
        except (Exception, Error) as error:
            db_exception("detected jams")

# calls waze datafeed api and puts traffic irregularity linestring data into postgres table called irregularities
def irregularities_call():
    irregularities_url = ('waze_API_url')
    
    response_dict = json_to_dict(irregularities_url)
    #cursor = db_connection()

    try:

        for irreg in response_dict['irregularities']:
            # establish variables for SQL insert statement
            id = irreg['id']

            try:
                geom_type = ('SRID=4326;LINESTRING(')
                temp_geom = []
                # for loop to convert X, Y pairs
                for coordinate in irreg['line']:
                    temp_coor = (str(coordinate['x']) + ' ' + str(coordinate['y']))
                    temp_geom.append(temp_coor)
                temp_geom_str = ', '.join([str(coor) for coor in temp_geom])
                geom = (geom_type + temp_geom_str + ')')
            except:
                geom = None

            detection_date = datetime.datetime.fromtimestamp(irreg['detectionDateMillis'] / 1000)
            try:
                update_date = datetime.datetime.fromtimestamp(irreg['updateDateMillis'] / 1000)
            except:
                update_date = None
            irregularity_type = irreg['type']
            try:
                start_node = irreg['startNode']
            except:
                start_node = None
            try:
                end_node = irreg['endNode']
            except:
                end_node = None
            try:
                speed = irreg['speed']
            except:
                speed = None
            try:
                speed_mph = irreg['speed'] / 1.609
            except:
                speed_mph = None
            try:
                delay_seconds = irreg['seconds']
            except:
                delay_seconds = None
            try:
                delay_minutes = irreg['seconds'] / 60
            except:
                delay_minutes = None
            try:
                jam_length = irreg['speed']
            except:
                jam_length = None
            try:
                jam_length_ft = irreg['speed'] * 3.2804
            except:
                jam_length_ft = None
            try:
                jam_trend = irreg['trend']
            except:
                jam_trend = None
            try:
                street = irreg['street']
            except:
                street = None
            try:
                city = irreg['city']
            except:
                city = None
            try:
                country = irreg['country']
            except:
                country = "US"
            try:
                jam_severity = irreg['severity']
            except:
                jam_severity = None
            try:
                jam_level = irreg['jamLevel']
            except:
                jam_level = None
            try:
                highway = irreg['highway']
            except:
                highway = None
            try:
                drivers_count = irreg['driversCount']
            except:
                drivers_count = None
            try:
                alerts_count = irreg['alertsCount']
            except:
                alerts_count = None
            try:
                no_thumbsup = irreg['nThumbsUp']
            except:
                no_thumbsup = None

        # SQL insert statement for waze irregularities
        try:
            cursor.execute("""
                INSERT INTO staging.irregularities (
                    id,
                    geom,
                    detection_date,
                    update_date,
                    irregularity_type,
                    start_node,
                    end_node,
                    speed,
                    speed_mph,
                    delay_seconds,
                    delay_minutes,
                    jam_length,
                    jam_length_ft,
                    jam_trend,
                    street,
                    city,
                    country,
                    jam_severity,
                    jam_level,
                    highway,
                    drivers_count,
                    alerts_count,
                    no_thumbsup)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                           , (id, geom, detection_date, update_date, irregularity_type, start_node, end_node, speed,
                              speed_mph, delay_seconds, delay_minutes, jam_length, jam_length_ft, jam_trend, street,
                              city, country, jam_severity, jam_level, highway, drivers_count, alerts_count,
                              no_thumbsup))
        except (Exception, Error) as error:
            db_exception("irregularities")
    except:
        pass

    
def alert_duplicate():
    try:
        cursor.execute("""
            DELETE FROM
                staging.alerts a
            USING staging.alerts b
            WHERE
                a.pk > b.pk
                AND a.uuid = b.uuid;""")
    except (Exception, Error) as error:
        cursor.close()
        connection.close()

def jam_duplicate():
    try:
        cursor.execute("""
            DELETE FROM
	            staging.detected_jams a
		    USING staging.detected_jams b
            WHERE
	            a.pk > b.pk
	            AND a.uuid = b.uuid;""")
    except (Exception, Error) as error:
        cursor.close()
        connection.close()

''' defining main '''

def main():
    db_connection()
    alerts_call()
    jams_call()
    irregularities_call()
    alert_duplicate()
    jam_duplicate()
    db_connection_close()

''' main execution '''
if __name__ == "__main__":
    main()
