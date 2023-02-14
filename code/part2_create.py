from logging import critical
import psycopg2
from psycopg2 import Error
from sqlalchemy import TEXT, create_engine, text
import pandas as pd
import numpy as np
from pathlib import Path
import datetime

weekdays = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday"
]

def to_weekday(s):
    """s range from 1~7"""
    return weekdays.index(s)


def run_from_sql(conn, sql_file):
    """ create tables in the PostgreSQL database"""
    cur = conn.cursor()
    sql_command = ''
    for line in sql_file:      
        # Ignore commented lines
        if not line.startswith('--') and line.strip('\n'):        
        # Append line to the command string, prefix with space
           sql_command +=  ' ' + line.strip('\n')

        # If the command string ends with ';', it is a full statement
        if sql_command.endswith(';'):
            # Try to execute statement and commit it
            try:
                cur.execute(sql_command)
            # Assert in case of error
            except:
                print('Error at command:'+sql_command)
                ret_ =  False
            # Finally, clear command string
            finally:
                sql_command = ''           
                ret_ = True
    return ret_



def data_to_db(conn):
    """ read data from excel and insert into database """
    cur = conn.cursor()
    path = Path(__file__).parent.parent
    data_path = str(path)+"/data/vaccine-distribution-data.xlsx"

    ## VaccineType -> Vaccine
    df = pd.read_excel(data_path, sheet_name="VaccineType")
    sql = """INSERT INTO Vaccine(ID, name, doses, tempMin, tempMax)
        VALUES(%s, %s, %s, %s, %s);
    """
    for index, r in df.iterrows():
        cur.execute(sql, (r['ID'],r['name'],r['doses'],r['tempMin'],r['tempMax']))
    
    ## Manucfactur -> Manu
    df = pd.read_excel(data_path, sheet_name="Manufacturer")
    sql = """INSERT INTO Manufacturer(manufID, country, phone)
        VALUES(%s, %s, %s);
    """
    sql2 = """INSERT INTO ManufacturedBy(manufID, vaccID)
        VALUES(%s, %s);
    """
    for index, r in df.iterrows():
        cur.execute(sql, (r['ID'],r['country'],r['phone']))
        cur.execute(sql2, (r['ID'],r['vaccine']))

    ## VaccineBatch -> Batch
    df = pd.read_excel(data_path, sheet_name="VaccineBatch")
    sql = """INSERT INTO Batch(batchID, amount, vaccID, manufID, prodDate, expirDate, org)
        VALUES(%s, %s, %s, %s, %s, %s, %s);
    """
    for index, r in df.iterrows():
        cur.execute(sql, (r['batchID'],r['amount'],r['type'],r['manufacturer'],
            r['manufDate'],r['expiration'],r['location']))
    
    ## VaccinationStations -> Organization
    df = pd.read_excel(data_path, sheet_name="VaccinationStations")
    sql = """INSERT INTO Organization(name, address, telephone)
        VALUES(%s, %s, %s);
    """
    for index, r in df.iterrows():
        cur.execute(sql, (r['name'],r['address'],r['phone']))

    ## Transportation log -> Transportation
    df = pd.read_excel(data_path, sheet_name="Transportation log")
    sql = """INSERT INTO Transportation(batchID, depDate, arrDate, depOrg, arrOrg)
        VALUES(%s, %s, %s, %s, %s);
    """
    for index, r in df.iterrows():
        cur.execute(sql, (r['batchID'],r['dateDep'],r['dateArr'],r['departure '],r['arrival']))

    ## StaffMembers -> Staff
    df = pd.read_excel(data_path, sheet_name="StaffMembers")
    sql = """INSERT INTO Staff(ssNo, name, birthday, phone, status, role, org)
        VALUES(%s, %s, %s, %s, %s, %s, %s);
    """
    for index, r in df.iterrows():
        cur.execute(sql, (r['social security number'],r['name'],r['date of birth'],
            r['phone'],r['vaccination status'],r['role'],r['hospital']))

    ## Shifts -> Shift
    df = pd.read_excel(data_path, sheet_name="Shifts")
    sql = """INSERT INTO Shift(org, weekday, ssNo)
        VALUES(%s, %s, %s);
    """
    for index, r in df.iterrows():
        weekday = to_weekday(r['weekday'])
        cur.execute(sql, (r['station'],weekday,r['worker']))

    ## Vaccinations -> Vaccination
    df = pd.read_excel(data_path, sheet_name="Vaccinations")
    sql = """INSERT INTO Vaccination(eventdate, organization, batchID)
        VALUES(%s, %s, %s);
    """
    for index, r in df.iterrows():
        cur.execute(sql, (r['date'],r['location '],r['batchID']))

    ## Patients -> Patient
    df = pd.read_excel(data_path, sheet_name="Patients")
    sql = """INSERT INTO Patient(ssNo, name, birthday, gender)
        VALUES(%s, %s, %s, %s);
    """
    for index, r in df.iterrows():
        cur.execute(sql, (r['ssNo'],r['name'],r['date of birth'],r['gender']))
    
    ## VaccinePatients -> Attendance
    df = pd.read_excel(data_path, sheet_name="VaccinePatients")
    sql = """INSERT INTO Attendance(ssNo, eventDate, org)
        VALUES(%s, %s, %s);
    """
    for index, r in df.iterrows():
        cur.execute(sql, (r['patientSsNo'],r['date'],r['location']))

    ## Symptoms -> Symptom
    df = pd.read_excel(data_path, sheet_name="Symptoms")
    sql = """INSERT INTO Symptom(name, critical)
        VALUES(%s, %s);
    """
    for index, r in df.iterrows():
        critical = True if r['criticality'] else False
        cur.execute(sql, (r['name'], critical))

    ## Diagnosis -> Diagnose
    df = pd.read_excel(data_path, sheet_name="Diagnosis")
    sql = """INSERT INTO Diagnose(patient, symptom, reportDate)
        VALUES(%s, %s, %s);
    """
    for index, r in df.iterrows():
        if not isinstance(r['date'], datetime.date):  # check valid date
            continue
        cur.execute(sql, (r['patient'],r['symptom'],r['date']))



def main():
    try:
        # Connect the postgres database from your local machine using psycopg2
        # conn = psycopg2.connect(
        #                 database="dbproject",  # TO BE REPLACED
        #                 user='postgres',    # TO BE REPLACED
        #                 password='123', # TO BE REPLACED
        #                 host='127.0.0.1',  # by default
        #                 port= '5432'  # by default
        #                 )
        # remote postgresql
        conn = psycopg2.connect(
            database="grp8_vaccinedist",
            user='grp08',
            password='fEv7uCrV',
            host='dbcourse2022.cs.aalto.fi', 
            port= '5432'
        )

        conn.autocommit = True
        # Create a cursor to perform database operations
        cur = conn.cursor()
        # Print PostgreSQL details
        print("PostgreSQL server information")
        print(conn.get_dsn_parameters(), "\n")
        # Executing a SQL query
        cur.execute("SELECT version();")
        # Fetch result
        record = cur.fetchone()
        print("You are connected to - ", record, "\n")



        DATADIR = str(Path(__file__).parent)
        # create tables by reading sql file
        sql_file = open(DATADIR+'/part2_create.sql')
        run_from_sql(conn, sql_file)
        # populate the tables
        data_to_db(conn)

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (conn):
            # psql_conn.close()
            # cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")


main()