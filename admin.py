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
        RAM = st.number_input("RAM", min_value=0, key="RAM")
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
