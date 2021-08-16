#!/usr/bin/env python
# coding: utf-8

'''
Name:       waze_duplciate_removal.py
Purpose:    cleaning up data from within the W4C database 
Author:     Snyder, Kyle
Created:    12AUG2021
Copyright:  Copyright 2021 Tri-County Regional Planning Commission
'''

'''
License:    <Permission is hereby granted, free of charge, to any person obtaining a copy of this
            software and associated documentation files (the "Software"), to deal in the Software
            without restriction, including without limitation the rights to use, copy, modify, 
            merge, publish, distribute, sublicense, and/or sell copies of the Software, and to 
            permit persons to whom the Software is furnished to do so, subject to the following conditions:

            The above copyright notice and this permission notice shall be included in all 
            copies or substantial portions of the Software.

            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING 
            BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
            IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
            WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
            SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.>
'''

''' Import python modules '''
import datetime
import psycopg2
from psycopg2 import Error

''' defining functions '''

#creates variables for starting a timestamp
def ts_start():
    global execute_time
    execute_time = datetime.datetime.now()
    print("Initiating CRUD Operations \nCurrent time: ", execute_time)

#calculates elapsed time and prints timestamp
def ts_end():
    elapsed_time = datetime.datetime.now() - execute_time
    print("\nTime to execute program: ", elapsed_time)

def success(schema):
    print("SUCCESS:","All indexes in schema:", schema, "are re-indexed." )

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
        print("Successfully connected to Database.\n")
    except (Exception, Error) as error:
        print('exception given')
        print("Error while connecting to Irregularities Table in PostgreSQL", error)
        cursor.close()
        connection.close()            
        print("PostgreSQL Connection is closed")

# reindexes the created schema named w4c
def w4c_idx():
    try:
        cursor.execute("""REINDEX SCHEMA w4c;""")
        success("w4c")   
    except (Exception, Error) as error:
        print("Error while executing Alert re-indexing: ", error)
        cursor.close()
        connection.close()
        print("PostgreSQL Connection for Alerts Table is closed")

#closes postgresql connection       
def db_close():
    #write changes to database, close cursor command, and close out database connection
    cursor.close()
    connection.close()
    print("Changes commmitted to database and connection closed.")

''' defining main '''
def main():
    ts_start()
    db_connection()
    w4c_idx()
    db_close()
    ts_end()

''' main execution '''
if __name__ == "__main__":
    main()