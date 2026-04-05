import streamlit as st
from modules import raceinfo as race

# Initialize DB connection.
conn = race.db_connect()

# Read race information for select boxes from DB
races = race.get_race_info(conn)
st.write(races)

