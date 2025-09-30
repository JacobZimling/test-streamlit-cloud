# 3_Race_graph.py

import streamlit as st

# Initialize DB connection.
conn = st.connection('freesqldatabase', type='sql')

# Get lap data
df = conn.query(f"SELECT * FROM race_laps WHERE race_id in (14, 15);", ttl=0)
st.write(df.empty)
st.dataframe(df)
