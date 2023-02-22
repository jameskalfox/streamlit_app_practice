import pandas
import streamlit
import requests
import snowflake.connector

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🍓 Build your own fruit smoothie 🥝🍇')

my_fruit_list = pandas.read_csv(
    'https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect(
    'Pick some fruits:', list(my_fruit_list.index))
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

fruit_choice = streamlit.text_input("Write Fruit:")
streamlit.write(fruit_choice + " selected.")

streamlit.header('Fruityvice Fruit Advice!')
fruityvice_response = requests.get(
    "https://fruityvice.com/api/fruit/" + fruit_choice)
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruityvice_normalized)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.dataframe(my_data_row)

fruit_add = streamlit.text_input("Add a fruit:")
my_cur.execute(
    "insert into pc_rivery_db.public.fruit_load_list values ('" + fruit_add + "')")
