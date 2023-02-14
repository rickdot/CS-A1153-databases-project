# Source: https://pynative.com/python-postgresql-tutorial/
import psycopg2
from psycopg2 import Error

try:
   # Connect to an test database 
   # NOTE: 
   # 1. NEVER store credential like this in practice. This is only for testing purpose
   # 2. Replace your "database" name, "user" and "password" that we provide to test the connection to your database 

   # local postgresql database
   #    connection = psycopg2.connect(
   #    database="dbproject",  # TO BE REPLACED
   #    user='postgres',    # TO BE REPLACED
   #    password='123', # TO BE REPLACED
   #    host='127.0.0.1', 
   #    port= '5432'
   # )

   # remote postgresql
   connection = psycopg2.connect(
      database="grp8_vaccinedist",  # TO BE REPLACED
      user='grp08',    # TO BE REPLACED
      password='fEv7uCrV', # TO BE REPLACED
      host='dbcourse2022.cs.aalto.fi', 
      port= '5432'
   )

   # Create a cursor to perform database operations
   cursor = connection.cursor()
   # Print PostgreSQL details
   print("PostgreSQL server information")
   print(connection.get_dsn_parameters(), "\n")
   # Executing a SQL query
   cursor.execute("SELECT version();")
   # Fetch result
   record = cursor.fetchone()
   print("You are connected to - ", record, "\n")

except (Exception, Error) as error:
   print("Error while connecting to PostgreSQL", error)
finally:
   if (connection):
      cursor.close()
      connection.close()
      print("PostgreSQL connection is closed")