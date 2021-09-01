#!/usr/bin/env python
# coding: utf-8

# waze_duplciate_removal.py
# Copyright 2021 Tri-County Regional Planning Commission


''' import modules / packages '''
import logging
import psycopg2
from psycopg2 import Error

''' variables '''
#establishing logging config
logging.basicConfig(filename ='reindexing.log',
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

def success(schema):
    logging.info("SUCCESS:","All indexes in {} are re-indexed.".format(schema))

#establishes connection to postgis database with an autocommit connection
def db_connection():
    try:
        #global connection to PostgreSQL database
        global connection 
        connection = psycopg2.connect(user="user",
                                     password = "password",
                                     host="localhost / ip address",
                                     port="5432",
                                     database="db_name")
        connection.autocommit = True
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

# reindexes the created schema named w4c
def w4c_idx():
    try:
        cursor.execute("""REINDEX SCHEMA w4c;""")
        success("w4c")   
    except (Exception, Error) as error:
        logging.error("Error while executing Alert re-indexing: {}".format(error))
        cursor.close()
        connection.close()
        logging.error("PostgreSQL Connection for Alerts Table is closed")

#closes postgresql connection       
def db_close():
    #write changes to database, close cursor command, and close out database connection
    cursor.close()
    connection.close()
    logging.info("Changes commmitted to database and connection closed.")

''' defining main '''
def main():
    prog_start()
    db_connection()
    w4c_idx()
    db_close()
    prog_end()

''' main execution '''
if __name__ == "__main__":
    main()