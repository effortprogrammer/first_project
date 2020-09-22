import sqlite3
from sqlite3 import Error
import csv
import numpy as np
import tempfile
import streamlit as st
import io

uploaded_file = st.file_uploader(...)
text.io = io.TestIOWrapper(uploaded_file)

conn = None
db = st.file_uploader("stock.db", type="db")

if db:
    with tempfile.NamedTemporaryFile() as fp:
        fp.write(db.getvalue())
        conn = sqlite3.connect(fp.name)

if conn:

    def create_connection(db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None

        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)
        return conn

    def create_project(conn, project):
        """
        Create a new project into the projects table
        :param conn:
        :param project:
        :return: project id
        """

        sql = ''' INSERT INTO projects(compamy_name,begin_price,end_price)
                  Values(?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, project)
        conn.commit()
        return cur.lastrowid

    def create_task(conn, task):
        """
        Create a new task
        :param conn:
        :param task:
        :return:
        """


        sql = ''' INSERT INTO tasks(name,priority,status_id,project_id,begin_date,end_date)
                  VALUES(?,?,?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, task)
        conn.commit()
        return cur.lastrowid

    def main():
        database = r"./stock.db"

        conn = create_connection(database)

        with conn:
            try:
                curs = conn.cursor()
                curs.execute('''CREATE TABLE IF NOT EXISTS stock (
                    id INT PRIMARY KEY,
                    company_name VARCHAR(200),
                    now_price INT
                )''')
                curs.close()
            except:
                import traceback
                print(traceback.format_exc())

            from csv import DictReader
            with open('data.csv', encoding='utf-8-sig') as file:
                data = DictReader(file)
                curs = conn.cursor()
                for row in data:
                    print(row)
                    ins = 'INSERT INTO stock (id, company_name, now_price) VALUES (?, ?, ?)'
                    curs.execute(ins, (
                        row['id'],
                        row['company_name'],
                        int(row['now_price'])
                    ))




if __name__ == '__main__':
    main()
