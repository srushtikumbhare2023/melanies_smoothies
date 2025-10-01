# Import python packages
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
import streamlit as st

st.title("Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom smoothie.")

# User name input
name_on_order = st.text_input("Enter your name for the order:")

# Snowflake connection parameters
connection_parameters = {
    "account": "CIGBIEV-FIB48928",
    "user": "SRUSHTIKUMBHARE2023",
    "password": "Srush@0987654321",
    "warehouse": "COMPUTE_WH",
    "database": "SMOOTHIES",
    "schema": "PUBLIC"
}

# Create Snowflake session
session = Session.builder.configs(connection_parameters).create()
st.success("Snowflake session created!")

# Get fruits list from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
fruits_list = [row['FRUIT_NAME'] for row in my_dataframe.collect()]

# Multiselect for ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruits_list,
    max_selections=5
)

# Insert order when button is clicked
if st.button('Submit Order') and ingredients_list and name_on_order:
    ingredients_string = ', '.join(ingredients_list)  # better formatting
    
    insert_stmt = """
        INSERT INTO smoothies.public.orders(ingredients, name_on_order)
        VALUES (%s, %s)
    """
    session.sql(insert_stmt, [ingredients_string, name_on_order]).collect()
    
    st.success('Your Smoothie is ordered! ✅')
