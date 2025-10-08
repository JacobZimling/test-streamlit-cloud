# raceinfo.py

import streamlit as st

class Race:
  def __init__(self):
    self.conn = st.connection('heliohost', type='sql')
    self.races = self.conn.query('SELECT race_date, race_venue, race_name FROM race_info')
    return

  def select_race_year():
    st.write('Select year')
    return

  def show_races(self):
    st.dataframe(self.races)

# Initialize DB connection.
# def db_connect():
#   return st.connection('heliohost', type='sql')
  
