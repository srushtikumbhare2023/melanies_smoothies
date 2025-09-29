import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

st.title("Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom smoothie.")

# Snowflake connection
connection_parameters = {
    "account": "your_account",
    "user": "your_username",
    "private_key_file": "./keys/snowflake_key.p8",
    "role": "SYSADMIN",
    "warehouse": "COMPUTE_WH",
    "database": "SMOOTHIES",
    "schema": "PUBLIC"
}

session = Session.builder.configs(connection_parameters).create()

# Fetch fruit options
my_dataframe = session.table("FRUIT_OPTIONS").select(col("FRUIT_NAME")).collect()
fruit_list = [row["FRUIT_NAME"] for row in my_dataframe]

# Streamlit widgets
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:', fruit_list, max_selections=5
)
name_on_order = st.text_input("Enter your name for the order:")

if ingredients_list and name_on_order:
    ingredients_string = ", ".join(ingredients_list)
    
    if st.button('Submit Order'):
        session.sql(
            "INSERT INTO ORDERS (ingredients, name_on_order) VALUES (?, ?)",
            [ingredients_string, name_on_order]
        ).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
