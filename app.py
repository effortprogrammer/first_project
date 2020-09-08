import streamlit as st
st.write("Here's our first attempt at using data to create a table:")

import pandas as pd
import sqlalchemy

engine = sqlalchemy.create_engine('sqlite:///stock.db')

df = pd.read_sql_table('stock', engine)
st.write(df)