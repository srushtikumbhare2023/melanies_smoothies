# Import python packages
import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col
import requests
import hashlib

# App title and description
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Step 1: Get name input
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Step 2: Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Step 3: Load fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(
    col("FRUIT_NAME"), col("SEARCH_ON")
)

# Convert Snowpark DataFrame → Pandas DataFrame
pd_df = my_dataframe.to_pandas()

# Step 4: Let user select fruits
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    pd_df["FRUIT_NAME"],
    max_selections=5
)

# Step 5: Proceed only if both name and ingredients are provided
if ingredients_list and name_on_order:
    # Combine selected fruits into one string
    ingredients_string = " ".join(ingredients_list).strip()

    # Show nutrition info for each selected fruit
    for fruit_chosen in ingredients_list:
        search_on = pd_df.loc[pd_df["FRUIT_NAME"] == fruit_chosen, "SEARCH_ON"].iloc[0]
        st.subheader(f"{fruit_chosen} Nutrition Information")
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    # Compute ORDER_UID (as required in DABW challenge)
    order_uid = hash(name_on_order + ingredients_string)

    # Prepare SQL insert for one smoothie order
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order, order_uid)
        VALUES ('{ingredients_string}', '{name_on_order}', {order_uid})
    """

    # Show SQL preview
    st.write("SQL Query Preview:", my_insert_stmt)

    # Step 6: Submit order
    if st.button("Submit Order"):
        session.sql(my_insert_stmt).collect()
        st.success(f"✅ Your Smoothie is ordered, {name_on_order}!")
        st.balloons()

else:
    st.info("👉 Please enter your name and select ingredients to create your smoothie.")
