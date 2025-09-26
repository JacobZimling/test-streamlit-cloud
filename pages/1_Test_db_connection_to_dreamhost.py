# 1_Test_db_connection_to_dreamhost.py


import streamlit as st

# Initialize connection.
conn = st.connection('mysql', type='sql')

# Perform query.
df = conn.query('SELECT * from madklub_deltagere;', ttl=600)

# Print results.
for row in df.itertuples():
    st.write(f"{row.names}")


import mysql.connector as connection
import pandas as pd
try:
    mydb = connection.connect(host=st.secrets.connections.freesqldatabase.com.host, database = st.secrets.connections.freesqldatabase.com.database, user=st.secrets.connections.freesqldatabase.com.username, passwd=st.secrets.connections.freesqldatabase.com.password, use_pure=True)
    query = "Select * from madklub_deltagere;"
    result_dataFrame = pd.read_sql(query,mydb)
    mydb.close() #close the connection
except Exception as e:
    mydb.close()
    print(str(e))
    
st.write(result_dataFrame)
