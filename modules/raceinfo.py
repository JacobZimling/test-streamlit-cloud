# raceinfo.py

import streamlit as st

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
  return conn.query('SELECT race_id, year(race_date) as race_year, date_format(race_date, "%Y-%m-%d") as race_date, race_venue, concat(race_venue, " (", date_format(race_date, "%e. %M"), ")") as venue_label, race_name FROM race_info')
  # return conn.query('SELECT race_id, year(race_date) as race_year, date_format(race_date, '%Y-%m-%d') as race_date, race_venue, concat(race_venue, " (", race_date, ")") as venue_label, race_name FROM race_info')
  
def get_lap_info(conn, race_date, race_name):
  return conn.query(
    f'SELECT \
        c.driver_id as driver_id, \
        c.lap as lap, \
        c.lap_time AS lap_time, \
        IF(@prev_driver_id = c.driver_id, \
           @race_time := addtime(@race_time, c.lap_time), \
           @race_time := c.lap_time) AS race_time, \
        @prev_driver_id := c.driver_id AS id \
    FROM ( \
        SELECT @prev_driver_id := NULL, \
               @race_time := 0 \
    ) i \
    JOIN ( \
        SELECT driver_id, lap, lap_time \
        FROM race_laps \
        WHERE race_id in (SELECT race_id FROM race_info WHERE race_date="{race_date}" and race_name="{race_name}") \
        ORDER BY driver_id, lap \
    ) c;',
    ttl=0)
