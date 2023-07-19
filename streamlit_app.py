#created the main python file
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("My Mom's new Healthy Dinner")
streamlit.header('Breakfast Menu')
streamlit.text('🥣 omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 kale , spinach & Rocket Smoothi')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include
fruit_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
show_fruits = my_fruit_list.loc[fruit_selected]
streamlit.dataframe(show_fruits)

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Please select a fruit to get information.')
  else:
    from_func = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(from_func)
except URLError as e:
  streamlit.error()

#streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.text("The Fruit Load List Contains:")
streamlit.dataframe(my_data_rows)

def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("INSERT INTO fruit_load_list values ('"+new_fruit+"')")
    return "Thanks for Adding "+new_fruit
                  
add_my_fruit = streamlit.text_input('What Fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  from_function = insert_row_snowflake(add_my_fruit)
  streamlit.text(from_function)
