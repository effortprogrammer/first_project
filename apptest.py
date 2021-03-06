# 앱 시작

import streamlit as st
import pandas as pd
import sqlite3
from typing import List
from sqlite3 import Connection
from datetime import datetime, timedelta
import yfinance as yf
import sqlalchemy
import pandas_datareader.data as web
import requests
import plotly.figure_factory as ff
import plotly.graph_objects as go
import numpy as np


Stock_sqlite_db = "stock.db"

def memoize(func):
    cache = dict()

    def memoized_func(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return memoized_func

def main():
    st.title('stock analysis')
    st.markdown("Search the history of the companies' stock data easily.")

    conn = get_connection(Stock_sqlite_db)
    conn = get_connection(Stock_sqlite_db)
    conn = get_connection(Stock_sqlite_db)
    conn = get_connection(Stock_sqlite_db)
    conn = get_connection(Stock_sqlite_db)
    conn = get_connection(Stock_sqlite_db)
    conn = get_connection(Stock_sqlite_db)
    conn = get_connection(Stock_sqlite_db)
    #init_db(conn)

    display_data(conn)



def display_data(conn: Connection):
    if st.checkbox("Display data in sqlite database"):
        #st.dataframe(get_data(conn))
        st.dataframe(get_data_demo(['AAPL', 'TSLA', 'BRK-B', 'DIS', 'AMZN', 'WMT', 'COST', 'AMAT']))
    val = st.selectbox("How would you like to be contacted?",
        ("Apple (AAPL)", "Tesla (TSLA)", "Berkshire Hathaway (BRK-B)", "Walt Disney (DIS)", "Amazon (AMZN)", "Walmart (WMT)", "Costco (COST)", "Applied Materials (AMAT)")
    )
    val = val.split('(')[1][:-1]
    df = get_price(conn, val)
    st.dataframe(df)
    st.line_chart(df)

def get_price(conn: Connection, company_names: str):
    companies = company_names.split(',')

    output = []
    start = datetime.now() - timedelta(days=730)
    end = datetime.now()
    for name in companies:
        ticker = yf.Ticker(name)
        df = ticker.history(start=start, end=end, interval='60m')
        output.append(df['Open'].rename(name))

    df_all = pd.DataFrame(output)
    return df_all.T

def get_price2(conn: Connection, company_name):
    curs = conn.cursor()
    a = curs.execute('''
        SELECT now_price FROM stock
        WHERE company_name = ? 
    ''', (company_name,))

    return pd.DataFrame(a, columns=['now_price'])


@st.cache
def get_data_demo(params: List[any]):
    df = pd.DataFrame(params)
    return df

def get_data(conn: Connection):
    df = pd.read_sql("SELECT company_name FROM stock", con=conn)
    return df

@memoize
def get_connection(path: str):
    """Put the connection in cache unless path does not change between streamlit returns"""
    print('create connection')
    return sqlite3.connect(path, check_same_thread=False)

# Set sample stock symbol to instrument variable

symbol = st.text_input('Enter Stock Symbol', 'QQQ')

API_URL = "https://www.alphavantage.co/query"

data = { "function": "TIME_SERIES_DAILY",
    "symbol": symbol,
    "outputsize" : "compact",
    "datatype": "json",
    "apikey": "XXXXXXXXXXXX" } #ENTER YOUR ALPHAVANTAGE KEY HERE

#https://www.alphavantage.co/query/
response = requests.get(API_URL, data).json()

data = pd.DataFrame.from_dict(response['Time Series (Daily)'], orient= 'index').sort_index(axis=1)
data = data.rename(columns={ '1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close', '5. volume': 'Volume'})
data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
data['Date'] = data.index

fig = go.Figure(data=[go.Candlestick(x=data['Date'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name=symbol)])

fig.update_layout(
    title=symbol+ ' Daily Chart',
    xaxis_title="Date",
    yaxis_title="Price ($)",
    font=dict(
        family="Courier New, monospace",
        size=12,
        color="black"
    )
)

st.plotly_chart(fig,  use_container_width=True)

if __name__ == "__main__":
    main()











