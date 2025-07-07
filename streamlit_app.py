import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

st.title(f":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom smoothie!
  """
)
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)
ingredient_list = st.multiselect(
   "Choose up to 5 options:",
    my_dataframe,
    max_selections=5
)
if ingredient_list:
  ingredients_string = '' 

  for ingredient in ingredient_list:
    ingredients_string += ingredient + ' '
    
    search_on=pd_df.loc[pd_df['FRUIT_NAME'] == ingredient, 'SEARCH_ON'].iloc[0]    
    st.subheader(ingredient + 'Nutrition Information')
    smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
    
    df_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)#evtl container entf.
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

  time_to_insert = st.button('Submit Order')
  if time_to_insert:
      session.sql(my_insert_stmt).collect()
      st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")



