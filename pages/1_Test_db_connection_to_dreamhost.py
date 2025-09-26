# 1_Test_db_connection_to_dreamhost.py

import streamlit as st

# Initialize connection.
conn = st.connection('mysql', type='sql')

# Perform query.
df = conn.query('SELECT * from madklub_deltagere;', ttl=600)

# Print results.
for row in df.itertuples():
    st.write(f"{row.names}")
