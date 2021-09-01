#!/usr/bin/env python
# coding: utf-8

# waze_duplciate_removal.py
# Copyright 2021 Tri-County Regional Planning Commission

''' import modules / packages'''
import logging
import psycopg2
from psycopg2 import Error

''' variables '''
#establishing logging config
logging.basicConfig(filename ='waze_ingestion.log',
                    level = logging.INFO,
                    filemode ='a',
                    format = '%(asctime)s:%(levelname)s:%(message)s')


''' defining functions '''

# logs the execution of the script
def prog_start():
    logging.info("Initiating data ingestion & CRUD operations.")

# logs the completion of the script
def prog_end():
    logging.info("Program operations completed.")

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
        logging.info("Successfully connected to Database.")
    except (Exception, Error) as error:
        logging.error("Error while connecting to PostgreSQL: {}".format(error))
        cursor.close()
        connection.close()
        logging.error("PostgreSQL Connection closed due to connection error")

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
        logging.info("SUCCESSFUL: Duplicates removed from Alert table.")
    except (Exception, Error) as error:
        logging.error("Error while executing Alert Duplicate Removal: {}".format(error))
        cursor.close()
        connection.close()
        logging.error("PostgreSQL Connection for Alerts Table is closed")

def jam_duplicate():
    try:
        cursor.execute("""
            DELETE FROM
	            w4c.detected_jams a
		    USING w4c.detected_jams b
            WHERE
	            a.pk > b.pk
	            AND a.uuid = b.uuid;""")
        logging.info("SUCCESSFUL: Duplicates removed from Jam table.")
    except (Exception, Error) as error:
        logging.error("ERROR while executing Jam Duplicate Removal: {}".format(error))
        cursor.close()
        connection.close()
        logging.error("PostgreSQL Connection for Detected Jam Table is closed")


# commits changes to database and closes database connection
def db_commit():
    # write changes to database, close cursor command, and close out database connection
    connection.commit()
    cursor.close()
    connection.close()
    logging.info("Changes commmitted to database and connection closed.")

''' defining main '''

def main():
    prog_start()
    db_connection()
    alert_duplicate()
    jam_duplicate()
    db_commit()
    prog_end()


''' main execution '''
if __name__ == "__main__":
    main()
