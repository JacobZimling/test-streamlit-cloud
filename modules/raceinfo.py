# raceinfo.py

import streamlit as st
from sqlalchemy.sql import text

# class Race:
  # def __init__(self):
  #   self.conn = st.connection('heliohost', type='sql')
  #   # self.races = self.conn.query('SELECT race_date, race_venue, race_name FROM race_info')
  #   return

  # def select_race_year():
  #   st.write('Select year')
  #   return
  
  # def show_races(self):
  #   st.dataframe(self.races)
  #   return
  
  # def get_race_years(self):
  #   return self.conn.query('SELECT distinct year(race_date) as race_year FROM race_info')

def db_connect():
  return st.connection('heliohost', type='sql')

# def get_race_years(conn):
#   return conn.query('SELECT distinct year(race_date) as race_year FROM race_info')

# def get_races(conn, race_year):
#   return conn.query(f'SELECT distinct race_date, race_venue FROM race_info WHERE year(race_date)={race_year}')

def get_race_info(conn):
  # return conn.query('SELECT race_id, year(race_date) as race_year, date_format(race_date, "%Y-%m-%d") as race_date, race_venue, concat(race_venue, " (", race_date, ")") as venue_label, race_name FROM race_info')
  return conn.query('SELECT race_id, year(race_date) as race_year, date_format(race_date, "%Y-%m-%d") as race_date, race_venue, concat(date_format(race_date, "%Y-%m-%d"), race_venue) as date_venue, concat(race_venue, " (", date_format(race_date, "%e. %M"), ")") as venue_label, race_name FROM race_info', ttl=0)
  
def get_lap_info(conn, date_venue, race_name):
  conn.reset()
  query = f'SELECT * FROM w_race_graph WHERE race_identifier="{date_venue}{race_name}";'
  return conn.query(query, ttl=0)
