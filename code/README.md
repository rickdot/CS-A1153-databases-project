## Files
1. **part2_create.sql** contains all the SQL commands to create the table
2. **part2_create.py** is used to create table on either local server or remote server, and populate the database by given dataset. It  will read from create_tables.sql and execute the SQL commands.
3. **part2_query.sql** contains queries for the 7 required queries
4. **part2_query.py** is used to run the queries contained in query.sql, and print the result of the queries
5. **part3_analysis.ipynb** is the file to analyze the dataset on given problems. It can be run in Jupyter Notebook, all results are visible.
6. **test_postgresql_conn.py** helper program to test the connection to local or the remote database server.
7. **requirements.txt** required packages to run the code. run by 
    ```pip install -r requirements.txt```