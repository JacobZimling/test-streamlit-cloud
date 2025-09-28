# 1_Test_db_connection_to_dreamhost.py


import streamlit as st

# Initialize connection.
conn = st.connection('freesqldatabase', type='sql')

# Insert some data with conn.session.
with conn.session as s:
    data = {1: {'Test1 & Test2', 7, 0}
    for k in pet_owners:
        s.execute(
            'INSERT INTO madklub_deltagere (names, `order`, active) VALUES (:names, :order, :active);',
            params=dict(names=k[0], order=k[1], active=k[2])
        )
    s.commit()

# Perform query.
df = conn.query('SELECT * from madklub_deltagere;', ttl=0)

# Print results.
for row in df.itertuples():
    st.write(f"{row.names}")


import mysql.connector as connection
import pandas as pd
try:
    mydb = connection.connect(host=st.secrets["freesqldatabase"]["host"], database = st.secrets["freesqldatabase"]["database"], user=st.secrets["freesqldatabase"]["username"], passwd=st.secrets["freesqldatabase"]["password"], use_pure=True)
    query = "Select * from madklub_deltagere;"
    result_dataFrame = pd.read_sql(query,mydb)
    mydb.close() #close the connection
except Exception as e:
    mydb.close()
    print(str(e))
    
st.write(result_dataFrame)
