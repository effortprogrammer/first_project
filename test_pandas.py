import pandas as pd
import sqlalchemy

engine = sqlalchemy.create_engine('sqlite:///stock.db')

df = pd.read_sql_table('stock', engine)
df