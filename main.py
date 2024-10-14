#Admin.py
import streamlit as st
from insert import insert_values
from db import connect_online, get_alldata_from_database
def main():
    st.header("Admin Page")
    if st.checkbox("Insert Data"):
        brand = st.text_input("Brand", placeholder="Enter Brand", key="brand")
        model = st.text_input("Model", placeholder="Enter Model", key="model")
        # Operating System dropdown
        operating_system = st.selectbox("Operating System", ["Android", "iOS"] , key="operating_system")
        internal_memory = st.number_input("Internal Memory (GB)", min_value=0, key="internal_memory")
        RAM =st.number_input("RAM", min_value=0, key="RAM")
        performance = st.number_input("Performance", min_value=0, max_value=10, key="performance")
        main_camera = st.number_input("Main Camera (MP)", min_value=0, key="main_camera")
        selfie_camera = st.number_input("Selfie Camera (MP)", min_value=0, key="selfie_camera")
        battery_size = st.number_input("Battery Size (mAh)", min_value=0, key="battery_size")
        screen_size = st.number_input("Screen Size (in)", min_value=0.0, key="screen_size") 

        weight = st.number_input("Weight (g)", min_value=0.0, key="weight")
        price = st.number_input("Price ($)", min_value=0.0, key="price")
        if st.button("Insert Data"):
            connection = connect_online()
            if connection:
                data = (brand, model, operating_system, internal_memory, RAM, performance, main_camera, selfie_camera, battery_size, screen_size, weight, price)
                insert_values(connection, data)
                connection.close()
        if st.checkbox("View Data"):
            data = get_alldata_from_database()
            st.dataframe(data)
    if __name__ == "__main__":
        main()
#db.py
import pandas as pd
import streamlit as st
import psycopg2
def get_alldata_from_database():
    # Connect to the MySQL database
    conn = connect_online()
    # Query to fetch data from the table
    query = "SELECT * FROM abcheck;"
    # Use pandas to read data from the database and create a DataFrame
    df = pd.read_sql_query(query, conn)
    # Close the connection
    conn.close()
    return df
def connect_online():
    db_config = {'dbname': 'verceldb','user': 'default','password': '7jK2RVPDZSpx','host': 'ep-shrill-mountain-97630726.ap-southeast=1.postgres.vercel-storage.com', 'port': '5432'}
    try:
        # Establish a connection to the database
        connection = psycopg2.connect(**db_config)
        print("Connection to PostgreSQL is successful.")
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL:", error)
        return None
#insert.py
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
       cursor.execute(query,row_values)
       connection.commit()
       cursor.close()
def insert_values(connection, data):
    try:
        cursor = connection.cursor()
        insert_query= "INSERT INTO products (brand, model, operating_system, internal_memory, RAM, performance, main_camera, selfie_camera, battery_size, screen_size, weight, price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
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
#purifier.py
from db import connect_online
import pandas as pd
def purification(p):
 conn = connect_online()
 command = [f"operating_system = '{p['os']}'",f"screen_size between {p['ss_min']} and {p['ss_max']}",f"internal_memory between {p['s_min']} and {p['s_max']}",f"price between {p['p_min']} and {p['p_max']}"]
 sand ='and'
 if p['os'] == 'Any':
     command[0] = ' '
 if p['ss_min'] == 'Any':
     command[1] = ' '
 if p['ss_min'] == 'Any':
     command[2] = ' '
 if p['p_min'] == 'Any':
     command[3] = ' '
 if p['use_case'] == 'Any':
     if command.count(' ') == 4:
         query= """"select brand || ' ' || model AS "Phone", internal_memory, ram, battery_size, screen_size, price from phonestable"""
     else:
        query = f"""select brand || ' ' || model AS "Phone", internal_memory, ram, battery_size, screen_size, price from phonestable where """
        c=0
        for i in command:
            if i != '':
                if c == 0:
                    query += f"{i} "
                    c+=1
                else:
                    if p['use_case'] == 'Gaming':
                        query = """"SELECT brand || ' ' || model AS "Phone", internal_memory, ram, battery_size, screen_size, price FROM phonestable WHERE (RAM >= 8 AND internal_memory >= 128) AND screen_size >= 6.0 AND battery_size >= 4000"""
                    elif p['use_case'] == 'Photography':
                        query = """SELECT brand || ' ' || model AS "Phone", internal_memory, ram, battery_size, screen_size, price FROM phonestable WHERE main_camera >= 48 AND selfie_camera >= 12"""
                    elif p['use_case'] == 'Large Screen':
                        query = """SELECT brand || ' ' || model AS "Phone", internal_memory, ram, battery_size, screen_size, price FROM phonestable WHERE screen_size >= 6.0"""
                    elif p['use_case'] == 'Great Battery Life':
                        query = """SELECT brand || ' ' || model AS "Phone", internal_memory, ram, battery_size, screen_size, price FROM phonestable WHERE battery_size >= 4500"""
                    if  p['os'] != 'Any':
                        query += " AND operating_system = '{}'".format(p['os'])
                        query += " ORDER BY"
                        if p['use_case'] == 'Gaming':
                            query += " performance DESC"
                        elif p['use_case'] == 'Photography':
                            query += " main_camera DESC, selfie_camera DESC"
                        elif p['use_case'] == 'Large Screen':
                            query += " screen_size DESC"
                        elif p['use_case'] == 'Great Battery Life':
                            query += " battery_size DESC"
                    def purification(purify):
                        conn = None
                        try:
                            # Connect to the database
                            conn = connect_to_database()
                            # Perform the purification
                            purify(conn)
                            # Close the connection
                            if conn is not None:
                                conn.close()
                        except Exception as e:
                            # Handle the exception
                            pass
#web.py
import streamlit as st
from purifier import purification
import streamlit as st
import pandas as pd
def create_phone_card(phone_name, internal_memory, ram, battery_size, screen_size, price):
    col1, col2 = st.columns([2, 1]) # Adjust the column ratios as needed
    with col1:
        st.subheader(f"{phone_name}")
        st.write(f"Internal Memory: {internal_memory} GB")
        st.write(f"RAM: {ram} GB")
        st.write(f"Battery Size: {battery_size} mAh")
        st.write(f"Screen Size: {screen_size} in")
    with col2:
        st.subheader("Price")
        st.write(f"${price:.2f}", font_size=24)
def main():
    st.title("Smartphone Finder")
    os_options = ['Any', 'Android', 'iOS']
    selected_os = st.selectbox("Select Operating System:", os_options)
    # Dropdown for Use Case
    use_case_options = ['Any', 'Gaming', 'Photography', 'Large Screen', 'Great Battery Life']
    selected_use_case = st.selectbox("Select Use Case:", use_case_options)
    # Create layout with 3 columns for sliders
    col1, col2, col3 = st.columns(3)
    # Integer Slider for Screen Size
    if selected_use_case != 'Any':
        check_screen = False
        check_storage = False
        check_price = False
        st.write("Filters for Screen Size, Storage, and Price are disabled when a specific use case is selected.")
    else:
        check_screen = col1.checkbox("Filter by Screen Size (inch)")
        check_storage = col2.checkbox("Filter by Storage (GB)")
        check_price = col3.checkbox("Filter by Price ($)")
    if check_screen:
        with col1:
            screen_size_min = col1.number_input("Minimum", value=4, min_value=2, max_value=10)
            screen_size_max = col1.number_input("Maximum", value=6, min_value=2, max_value=10)
            col1.write(f"Screen Size Range: {screen_size_min} in - {screen_size_max} in")
    else:
        screen_size_min = 'Any'
        screen_size_max = 'Any'
    if check_storage:
        with col2:
            storage_min = col2.number_input("Minimum", value=64, min_value=16, max_value=1024)
            storage_max = col2.number_input("Maximum", value=128, min_value=16, max_value=1024)
            col2.write(f"Storage Range: {storage_min} GB -{storage_max} GB")
    else:
        storage_min = 'Any'
        storage_max = 'Any'
    if check_price:
        with col3:
            price_min = col3.number_input("Minimum", value=500, min_value=100, max_value=50000)
            price_max = col3.number_input("Maximum", value=1000, min_value=100, max_value=50000)
            col3.write(f"Price Range: ${price_min} -${price_max}")
    else:
        price_min = 'Any'
        price_max = 'Any'
    search_button = st.button("Search")
    if search_button :
        purify ={'os':selected_os,'use_case':selected_use_case,'ss_min':screen_size_min,'ss_max':screen_size_max,'s_min':storage_min,'s_max':storage_max,'p_min':price_min,'p_max':price_max}
        # Perform filtering and display results
        filtered_results = purification(purify)
        filtered_rs = pd.DataFrame(filtered_results)
        for mytuple in filtered_rs.itertuples():
            phna = mytuple.Phone
            intm = mytuple.internal_memory
            ram = mytuple.ram
            bat = mytuple.battery_size
            scr = mytuple.screen_size
            pri = mytuple.price
    
            create_phone_card(phna, intm, ram, bat, scr, pri)

if __name__ == "__main__":
    main()