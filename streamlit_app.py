# Import Python packages
from snowflake.snowpark import Session
import streamlit as st
from snowflake.snowpark.functions import col

# Streamlit App UI
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie.")

# User Input
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name of your Smoothie will be:', name_on_order)

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Fetch fruit options
my_dataframe = session.table(
    "smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)

# Ingredient Selection
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe.collect(),  # Convert Snowpark DataFrame to list
    max_selections=5,
)

# Handle Order Submission
if ingredients_list:
    ingredients_string = ", ".join(
        [row['FRUIT_NAME'] for row in ingredients_list])
    st.write("You selected:", ingredients_string)

    if st.button('Submit Order'):
        insert_stmt = f"""
            INSERT INTO smoothies.public.orders (ingredients, name_on_order)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """
        session.sql(insert_stmt).collect()
        st.success('✅ Your Smoothie is ordered!', icon="🥤")
