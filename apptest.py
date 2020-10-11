# 앱 시작

import streamlit as st
import pandas as pd
import sqlite3
from typing import List
from sqlite3 import Connection
from datetime import datetime, timedelta
import yfinance as yf

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
    st.markdown("Enter company name in databse from sidebar, then run the app.")

    conn = get_connection(Stock_sqlite_db)
    conn = get_connection(Stock_sqlite_db)
    conn = get_connection(Stock_sqlite_db)
    conn = get_connection(Stock_sqlite_db)
    conn = get_connection(Stock_sqlite_db)
    conn = get_connection(Stock_sqlite_db)
    conn = get_connection(Stock_sqlite_db)
    conn = get_connection(Stock_sqlite_db)
    #init_db(conn)

    build_sidebar(conn)
    display_data(conn)

def build_sidebar(conn: Connection):
    st.sidebar.header("Configuration")
    input1 = st.sidebar.slider("company_name", 0, 51)
    input2 = st.sidebar.slider("Price", 0, 51)

    input1 = input2

    if st.sidebar.button("Save"):
        conn.execute("INSERT INTO stock (input1, input2) VALUES ({input1}, {input2})")
        conn.commit()


def display_data(conn: Connection):
    if st.checkbox("Display data in sqlite database"):
        #st.dataframe(get_data(conn))
        st.dataframe(get_data_demo([1,2,3]))
    val = st.text_input(label="input params")
    val = st.selectbox(
        "How would you like to be contacted?",
        ("Apple (AAPL)", "Tesla (TSLA)", "Mobile phone")
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


if __name__ == "__main__":
    main()











