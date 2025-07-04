# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
  """Choose the fruits you wnat in your custom Smoothie!
  """
)

cnx = st.connection("snowflake")
session = cnx.session()

name_input = st.text_input("Name on Smoothie:")
st.write('The name on your Smoothie will be:', name_input)

#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_Name'),col('search_on'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()


ingredient_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections= 5
)


if ingredient_list:
    ingredients_string = ''
    for fruit_chosen in ingredient_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
      
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + str(search_on))
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        
    
    

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """', '""" + name_input + """')"""
    
    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    #st.write(my_insert_stmt)
    #st.stop
  
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

