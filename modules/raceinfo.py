# raceinfo.py

import streamlit as st

class Race:
  def __init__(self):
    self.conn = st.connection('heliohost', type='sql')
    
# Initialize DB connection.
# def db_connect():
#   return st.connection('heliohost', type='sql')
  
