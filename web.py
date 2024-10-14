import streamlit as st
from purifier import purification


def create_phone_card(phone_name, internal_memory, ram, battery_size, screen_size, price):
    col1, col2 = st.columns([2, 1])  # Adjust the column ratios as needed
    
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
            col2.write(f"Storage Range: {storage_min} GB - {storage_max} GB")
    else:
        storage_min = 'Any'
        storage_max = 'Any'
    if check_price:
        with col3:
            price_min = col3.number_input("Minimum", value=500, min_value=100, max_value=50000)
            price_max = col3.number_input("Maximum", value=1000, min_value=100, max_value=50000)
            col3.write(f"Price Range: ${price_min} - ${price_max}")
    else:
        price_min = 'Any'
        price_max = 'Any'  
    search_button = st.button("Search")
    if search_button:
        purify = {'os':selected_os,'use_case':selected_use_case,'ss_min':screen_size_min,'ss_max':screen_size_max,'s_min':storage_min,'s_max':storage_max,'p_min':price_min,'p_max':price_max}
        # Perform filtering and display results
        filtered_results = purification(purify)
        
        for tuple in filtered_results.itertuples():
            phna = tuple.Phone
            intm = tuple.internal_memory
            ram = tuple.ram
            bat = tuple.battery_size
            scr = tuple.screen_size
            pri = tuple.price
            
            create_phone_card(phna, intm, ram, bat, scr, pri)
                

if __name__ == "__main__":
    main()
