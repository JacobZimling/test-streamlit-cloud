import streamlit as st
from modules import raceinfo as race
from modules import race_selector as rs

# Initialize DB connection.
conn = race.db_connect()

# Read race information for select boxes from DB
races = race.get_race_info(conn)
st.write(races)

race_year = rs.selector(races['race_year'])
st.write(race_year)
if race_year:

    # Select race type (2wd/4wd)
    race_type = rs.selector(races[races['race_year']==race_year]['race_type'])
