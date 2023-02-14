from calendar import weekday
from logging import critical
import psycopg2
from psycopg2 import Error
from sqlalchemy import TEXT, create_engine, text
import pandas as pd
import numpy as np
from pathlib import Path


def select_from(conn, sql_command):
    """ query data from database """
    try:
        cur = conn.cursor()
        cur.execute(sql_command)
        # print("The number of parts: ", cur.rowcount)
        row = cur.fetchone()

        while row is not None:
            print(row)
            row = cur.fetchone()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)




def main():
    try:
        # connect to database
        conn = psycopg2.connect(
            database="grp8_vaccinedist",
            user='grp08',
            password='fEv7uCrV',
            host='dbcourse2022.cs.aalto.fi', 
            port= '5432'
        )
        conn.autocommit = True
        cur = conn.cursor()

        # Print PostgreSQL details
        print("PostgreSQL server information")
        print(conn.get_dsn_parameters(), "\n")

        cur.execute("SELECT version();")
        record = cur.fetchone()
        print("You are connected to - ", record, "\n")





        DATADIR = str(Path(__file__).parent)
        sql_file = open(DATADIR+'/part2_query.sql')
        



        # execute commands in the sql file
        sql_command = ''
        for line in sql_file:      
            # Ignore commented lines
            if not line.startswith('--') and line.strip('\n'):        
            # Append line to the command string, prefix with space
                sql_command +=  ' ' + line.strip('\n')
            # If the command string ends with ';', it is a full statement
            if sql_command.endswith(';'):
                # execute the query and print the result
                try:
                    # print(sql_command)
                    select_from(conn, sql_command)
                    print("\n\n\n")
                # Assert in case of error
                except:
                    print('Error at command:'+sql_command + ".")
                
                # Finally, clear command string
                finally:
                    sql_command = ''


        
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (conn):
            conn.close()
            print("PostgreSQL connection is closed")


main()