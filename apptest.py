# 앱 시작

import streamlit as st
import pandas as pd
import sqlite3
from sqlite3 import Connection

Stock_sqlite_db = "stock.db"

def main():
    st.title('stock analysis')
    st.markdown("Enter company name in databse from sidebar, then run the app.")

    conn = get_connection(Stock_sqlite_db)
    init_db(conn)

    build_sidebar(conn)
    display_data(conn)


def init_db(conn: Connection):
    conn.execute(
        """CREATE TABLE company_name
            (
                # 여기다가 stock_db에서 company_name만 불러오는 건지
                #아니면 stock.db 전체를 다 끌어와야 하는 건지 
            
            
            )
        """
    )
    conn.commit()

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
        st.dataframe(get_data(conn))

def get_data(conn: Connection):
    df = pd.read_sql("SELECT * FROM stock", con=conn)
    return df

@st.cache
def get_connection(path: str):
    """Put the connection in cache unless path does not change between streamlit returns"""
    return sqlite3.connect(path, check_same_thread=False)


if __name__ == "__main__":
    main()











