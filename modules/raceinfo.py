# raceinfo.py

import streamlit as st

# Initialize DB connection.
def db_connect():
  return st.connection('heliohost', type='sql')
  
