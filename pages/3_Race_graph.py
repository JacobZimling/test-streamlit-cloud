# 3_Race_graph.py

import streamlit as st

# Initialize DB connection.
conn = st.connection('freesqldatabase', type='sql')

# Get lap data
df = conn.query(f"SELECT lap, driver_id, lap_time, sum(lap_time) OVER (PARTITION BY driver_id ORDER BY lap) FROM race_laps WHERE race_id in (14, 15);", ttl=0)
st.dataframe(df)

# st.line_chart(df, x='lap_time', y='lap')
st.bar_chart(df, x='driver_id', y='lap', sort='driver_id', color='driver_id', stack=False)

import plotly.express as px
#st.write(px.bar(df, x="driver_id", y="lap", animation_frame="lap_time", hover_name="driver_id"))
