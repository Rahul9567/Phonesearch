import pandas as pd
import streamlit as st
import psycopg2

def get_alldata_from_database():
    # Connect to the MySQL database
    conn = connect_online()

    # Query to fetch data from the table
    query = "SELECT * FROM phonestable;"

    # Use pandas to read data from the database and create a DataFrame
    df = pd.read_sql_query(query, conn)

    # Close the connection
    conn.close()

    return df

def connect_online():
    db_config = {
        'dbname': 'verceldb',
        'user': 'default',
        'password': '7jK2RVPDZSpx',
        'host': 'ep-shrill-mountain-97630726.ap-southeast-1.postgres.vercel-storage.com',
        'port': '5432'
    }
    try:
        # Establish a connection to the database
        connection = psycopg2.connect(**db_config)
        print("Connection to PostgreSQL is successful.")
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL:", error)
        return None

connect_online()
