# Import python packages
import streamlit as st

from snowflake.snowpark.functions import col


st.title(":Cup_with_straw: Customize Your Smoothies! :cup_with_straw:")
st.write(
    """ Choose the fruits you want in your smoothie!"""
)

name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your smoothies will be: ', name_on_order )
#option = st.selectbox('What is your favorite fruit?',
 #   ('Banana', 'Strawberries', 'Peaches'))
# Write directly to the app
#st.title(f"Customize Your Smoothine :balloon: {st.__version__}")


#option = st.selectbox("How would you like to becontacted",
#   ('Email', 'Home phone', 'Mobile Phone'))
    
#st.write('You favorite fruit is', option)

cnx = st.connection("snowflake")
session=cnx.session()

#my_dataframe = session.table("smoothies.public.fruit_options")
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
ingredients_list = st.multiselect( 'Choose up to 5 ingredients:', my_dataframe, max_selections=5)
if ingredients_list:
   # st.write(ingredients_list)
   # st.text(ingredients_list)
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    st.write(ingredients_string)

    my_insert_stmt = """insert into smoothies.public.ORDERS(ingredients, name_on_order) 
        values('""" + ingredients_string + """','""" + name_on_order  + """' )"""
#st.write(my_insert_stmt)

#if ingredients_string:
 #   session.sql(my_insert_stmt).collect()
 #   st.success('Your Smoothies is ordered')
 
    time_to_insert = st.button("Submit ordrs")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothies is ordered')
    
