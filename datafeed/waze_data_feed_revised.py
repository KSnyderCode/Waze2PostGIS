#!/usr/bin/env python
# coding: utf-8

# waze_data_feed.py
# Copyright 2021 Tri-County Regional Planning Commission


''' import modules / packages '''
# note that "requests" is not a base module and will need to be installed with Conda (or whatever you use)
import datetime
import json
import requests
import psycopg2
from psycopg2 import Error

''' define functions '''


# creates variables for starting a timestamp
def ts_start():
    global execute_time
    execute_time = datetime.datetime.now()
    print("Initiating CRUD Operations \nCurrent time: ", execute_time)


# calculates elapsed time and prints timestamp
def ts_end():
    elapsed_time = datetime.datetime.now() - execute_time
    print("\nTime to execute program: ", elapsed_time)


# converts api response into json and then into a python dictionary
def json_to_dict(url):
    api_response = requests.get(url)
    responseAsJson = api_response.text
    global responseAsDict
    responseAsDict = json.loads(responseAsJson)


# establishes connection to postgis database with an autocommit connection
def db_connection():
    try:
        # global connection to PostgreSQL database
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
        # print database information after connection established
        print("Successfully connected to Database.\n")
        return connection, cursor
    except (Exception, Error) as error:
        print('EXCEPTION GIVEN DURING CONNECTION')
        print("Error while connecting to Irregularities Table in PostgreSQL", error)
        cursor.close()
        connection.close()
        print("PostgreSQL Connection is closed")


# prints a completed statement with the count of records insert into database
def commit_statement(table, counter):
    print(table.title(), "updated. Count: ", counter, "\n")


def db_connection_close():
    # close cursor command, and close out database connection
    cursor.close()
    connection.close()
    print("All updates commmitted to database and connection closed.")


# function for when exceptions are raised to close out DB connection
def db_exception(table):
    print('EXCEPTION GIVEN DURING CONNECTION')
    cursor.close()
    connection.close()
    print("PostgreSQL Connection to", table.upper(), "is closed")


# calls waze datafeed api and puts point data into postgres table called alerts
def alertsCall():
    alerts_url = ('waze_datafeed_url')

    json_to_dict(alerts_url)
    counter = 0

    for alert in responseAsDict['alerts']:

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
                INSERT INTO w4c.alerts (
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
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (time_stamp, geom, magvar,
                                                                                             alert_type, subtype,
                                                                                             report_description, street,
                                                                                             city, country, road_type,
                                                                                             report_rating,
                                                                                             uuid, confidence,
                                                                                             reliability, no_thumbsup))
            counter += 1
        except (Exception, Error) as error:
            print("Error while executing SQL insert: ", error)
            db_exception("alerts")
    commit_statement("alerts", counter)


# calls waze datafeed api and puts jam linestring data into postgres table called detected_jams
def jamsCall():
    jams_url = ('waze_datafeed_url')

    json_to_dict(jams_url)
    counter = 0

    for jam in responseAsDict['jams']:

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
            for coordinate in responseAsDict['segments']:
                geom_type = ('SRID=4326;LINESTRING(')
                temp_geom = []
                temp_coor = (str(coordinate['x']) + ' ' + str(coordinate['y']))
                temp_geom.append(temp_coor)
            temp_geom_str = ','.join([str(coor) for coor in temp_geom])
            turn_line = geom_type + temp_geom_str + ')'
        except:
            turn_line = None
        turn_type = jam['turnType']

        # SQL insert statement for waze alerts
        try:
            cursor.execute("""
                INSERT INTO w4c.detected_jams (
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
            counter += 1
        except (Exception, Error) as error:
            print("Error while executing SQL insert: ", error)
            db_exception("detected jams")
    commit_statement("jams", counter)


# calls waze datafeed api and puts traffic irregularity linestring data into postgres table called irregularities
def irregularitiesCall():
    irregularities_url = ('waze_datafeed_url')

    json_to_dict(irregularities_url)
    counter = 0

    try:

        for irreg in responseAsDict['irregularities']:
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

                # SQL insert statement for waze alerts
        try:
            cursor.execute("""
                INSERT INTO w4c.irregularities (
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
                              speed_mph,
                              delay_seconds, delay_minutes, jam_length, jam_length_ft, jam_trend, street, city, country,
                              jam_severity, jam_level, highway, drivers_count, alerts_count, no_thumbsup))
            counter += 1
        except (Exception, Error) as error:
            print("Error while executing SQL insert: ", error)
            db_exception("irregularities")

        commit_statement("irregularities", counter)

    except:
        print("No irregularities detected.\n")


''' defining main '''


def main():
    ts_start()
    db_connection()
    alertsCall()
    jamsCall()
    irregularitiesCall()
    db_connection_close()
    ts_end()


''' main execution '''
if __name__ == "__main__":
    main()
