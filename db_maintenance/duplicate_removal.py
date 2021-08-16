#!/usr/bin/env python
# coding: utf-8

# waze_duplciate_removal.py
# Copyright 2021 Tri-County Regional Planning Commission


''' import modules / packages'''
import datetime
import psycopg2
from psycopg2 import Error

''' defining functions '''


# creates variables for starting a timestamp
def ts_start():
    global execute_time
    execute_time = datetime.datetime.now()
    print("Initiating CRUD Operations \nCurrent time: ", execute_time)


# calculates elapsed time and prints timestamp
def ts_end():
    elapsed_time = datetime.datetime.now() - execute_time
    print("\nTime to execute program: ", elapsed_time)


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

        # creating global cursor for database operations
        global cursor
        cursor = connection.cursor()
        # print database information after connection established
        print("Successfully connected to Database.\n")
    except (Exception, Error) as error:
        print('exception given')
        print("Error while connecting to Irregularities Table in PostgreSQL", error)
        cursor.close()
        connection.close()
        print("PostgreSQL Connection is closed")


# deletes duplicate out of the database by comparing virtual twins
#  of the database tables and keeping the lower primary key value
def alert_duplicate():
    try:
        cursor.execute("""
            DELETE FROM
	            w4c.alerts a
	        USING w4c.alerts b
            WHERE
                a.pk > b.pk
                AND a.uuid = b.uuid;""")
        print("SUCCESSFUL: Duplicates removed from Alert table.\n")
    except (Exception, Error) as error:
        print("Error while executing Alert Duplicate Removal: ", error)
        cursor.close()
        connection.close()
        print("PostgreSQL Connection for Alerts Table is closed")


def jam_duplicate():
    try:
        cursor.execute("""
            DELETE FROM
	            w4c.detected_jams a
		    USING w4c.detected_jams b
            WHERE
	            a.pk > b.pk
	            AND a.uuid = b.uuid;""")
        print("SUCCESSFUL: Duplicates removed from Jam table.\n")
    except (Exception, Error) as error:
        print("ERROR while executing Jam Duplicate Removal: ", error)
        cursor.close()
        connection.close()
        print("PostgreSQL Connection for Detected Jam Table is closed")


# commits changes to database and closes database connection
def db_commit():
    # write changes to database, close cursor command, and close out database connection
    connection.commit()
    cursor.close()
    connection.close()
    print("Changes commmitted to database and connection closed.")


''' defining main '''


def main():
    ts_start()
    db_connection()
    alert_duplicate()
    jam_duplicate()
    db_commit()
    ts_end()


''' main execution '''
if __name__ == "__main__":
    main()
