# 1_Test_db_connection_to_dreamhost.py

import streamlit as st
from sqlalchemy.sql import text
from datetime import datetime

# Initialize connection.
conn = st.connection('freesqldatabase', type='sql')

# Insert some data with conn.session.
with conn.session as s:
    race_date = datetime.strptime('Jan 01, 2025', "%b %d, %Y").date()
    data = [(race_date, 'Another race')]
    st.write(data)
    for k in data:
        s.execute(
            text('INSERT INTO race_info (race_date, race_name) VALUES (:date, :name);'),
            params=dict(date=k[0].strftime('%Y-%m-%d'), name=k[1])
        )
    s.commit()
    
    # data = [('Test1 & Test2', 7, 0)]
    # for k in data:
    #     s.execute(
    #         text('INSERT INTO madklub_deltagere (names, `order`, active) VALUES (:names, :order, :active);'),
    #         params=dict(names=k[0], order=k[1], active=k[2])
    #     )
    # s.commit()

# Perform query.
df = conn.query('SELECT * from race_info;', ttl=0)
# Print results.
for row in df.itertuples():
    st.write(f"{row.race_id} {row.race_date} {row.race_name}")

# Perform query.
#df = conn.query('SELECT * from madklub_deltagere;', ttl=0)
# Print results.
# for row in df.itertuples():
#     st.write(f"{row.names}")


# import mysql.connector as connection
# import pandas as pd
# try:
#     mydb = connection.connect(host=st.secrets["freesqldatabase"]["host"], database = st.secrets["freesqldatabase"]["database"], user=st.secrets["freesqldatabase"]["username"], passwd=st.secrets["freesqldatabase"]["password"], use_pure=True)
#     query = "Select * from madklub_deltagere;"
#     result_dataFrame = pd.read_sql(query,mydb)
#     mydb.close() #close the connection
# except Exception as e:
#     mydb.close()
#     print(str(e))
    
# st.write(result_dataFrame)
