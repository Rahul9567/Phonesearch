import pandas as pd
from db import connect_online
import streamlit as st
import psycopg2
def insert_data_from_csv(connection, csv_file_path):
    df = pd.read_csv(csv_file_path)

    columns = ', '.join(df.columns)
    placeholders = ', '.join(['%s'] * len(df.columns))
    query = f'INSERT INTO phonestable ({columns}) VALUES ({placeholders})'

    cursor = connection.cursor()
    for row in df.itertuples(index=False):
        row_values = [None if pd.isna(value) else value for value in row]
        cursor.execute(query, row_values)

    connection.commit()
    cursor.close()

def insert_values(connection, data):
    try:
        cursor = connection.cursor()
        insert_query = "INSERT INTO products (brand, model, operating_system, internal_memory, RAM, performance, main_camera, selfie_camera, battery_size, screen_size, weight, price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, data)
        connection.commit()
        st.success("Data inserted successfully!")
    except psycopg2.Error as err:
        st.error(f"Error: {err}")
        if connection:
            connection.rollback()

def create_db():
    conn = connect_online()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS phonestable (id int primary key, brand VARCHAR(30), model VARCHAR(50), operating_system VARCHAR(10), internal_memory INT, RAM INT, performance INT, main_camera INT, selfie_camera INT, battery_size INT, screen_size FLOAT, weight FLOAT, price FLOAT)")
    conn.commit()
    cursor.close()
    conn.close()

def insert_online_from_csv(connection, csv_file_path):
    df = pd.read_csv(csv_file_path)
    n = len(df)
    columns = ', '.join(df.columns)
    placeholders = ', '.join(['%s'] * len(df.columns))
    cursor = connection.cursor()
    query = f'INSERT INTO phonestable ({columns}) VALUES ({placeholders})'
    for row in df.itertuples(index=False):
        row_values = [None if pd.isna(value) else value for value in row]
        cursor.execute(query, row_values)
    connection.commit()
    cursor.close()
