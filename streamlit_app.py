#created the main python file
import streamlit
streamlit.title('My Parents new Healthy Dinner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 omega 3, oats, milk, pomogranet')
streamlit.text('🥗 spinach, fish, fruits')
streamlit.text('🐔 Boild egg, Chicken')
streamlit.text('🥑🍞 avacado toasting')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fruit_list)
