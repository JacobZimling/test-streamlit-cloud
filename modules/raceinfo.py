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
  return conn.query(
	  '''SELECT race_id, 
	  			case race_name 
					when "2wd" then race_name 
					else "4wd" 
				end as race_type, 
				year(race_date) as race_year, 
				date_format(race_date, "%Y-%m-%d") as race_date, 
				race_venue, 
				concat(date_format(race_date, "%Y-%m-%d"), race_venue) as date_venue, 
				concat(race_venue, " (", date_format(race_date, "%e. %M"), ")") as venue_label, 
				race_name, 
				case (race_name) 
					when "2wd" then "0" 
					else race_name 
				end as race_order 
			FROM race_info 
			ORDER BY race_date, race_order''', ttl=0)

def update_race_graph_data(conn, race_identifier):
  with conn.session as s:
    query = f"DELETE FROM race_graph WHERE race_identifier='{race_identifier}';"
    s.execute(text(query))
    query = f"""INSERT INTO race_graph (race_identifier, driver_id, race_time_dt, lap) 
		SELECT race_identifier, driver_id, race_time_dt, coalesce(lap, 0) as lap 
		FROM ( 
			SELECT 
				dt.race_identifier, 
				dt.driver_id,  
				dt.race_time_dt, 
				l.lap, 
				ROW_NUMBER() OVER ( 
					PARTITION BY dt.race_identifier, dt.driver_id, dt.race_time_dt 
					ORDER BY dt.race_time_dt - l.race_time_dt 
				) AS rn 
			FROM w_driver_times as dt 
			LEFT JOIN ( 
				SELECT wri.race_identifier, rl.driver_id, rl.race_time_dt, rl.lap 
				FROM race_laps as rl 
					JOIN w_race_identifier as wri 
						ON rl.race_id=wri.race_id 
			   ) as l 
				ON dt.race_identifier=l.race_identifier 
				and dt.driver_id = l.driver_id 
				AND dt.race_time_dt >= l.race_time_dt 
			WHERE dt.race_identifier='{race_identifier}' 
		) sub 
		WHERE rn = 1 
		;"""
    s.execute(text(query))
    s.commit()
  return
  
def get_lap_info(conn, date_venue, race_name):
  conn.reset()
  query = f'SELECT driver_id, race_time_dt, lap FROM race_graph WHERE race_identifier="{date_venue}{race_name}";'
  return conn.query(query, ttl=0)

def format_time(td):
  st.write(type(td))
  return ''

def get_race_result(conn, date_venue, race_name):
  conn.reset()
  query = f'SELECT rank, driver_id, race_time_dt, lap, point FROM w_race_result WHERE race_identifier="{date_venue}{race_name}";'
  race_result = conn.query(query, ttl=0)
  # st.wrtie(type(race_result['race_time']))
  # race_result['race_time_formated'] = race_result['race_time'].apply(format_time)
  # return conn.query(query, ttl=0)
  return race_result

def result_identifier(*args):
	# result_id = ''
	# for id in args:
	# 	result_id += f'¤{id}'
	# return result_id
	# st.write(args)
	# st.write(list(str(args)))
	for id in args:
		result.append(id)
	st.write(result)
	return '¤'.join(result)
	# return '¤'.join(list(str(args)))
	# return ''
	
def get_race_result_aggr(conn, race_year, race_type):
	conn.reset()
	query = f'SELECT rank, driver_id, race_time_dt, lap, point FROM w_race_result WHERE race_identifier="{date_venue}{race_name}";'
	race_result = conn.query(query, ttl=0)
	return race_result

def race_selector(conn):
  # Read race information from DB
  races = get_race_info(conn)
  # st.write(races)
  
  # Select year
  race_year = st.selectbox('År', options=races['race_year'].unique(), index=None, placeholder='Vælg år', width=300)
  return 'date_venue', 'race_heat'  
  
  if race_year:
    # st.write(f'get races for {race_year}')
  
    # Limit venue list based on race_year
    venue_selector = races[races['race_year'] == race_year]
    # st.write(venue_selector)
    # st.write(type(venue_selector))
  
    # Create data for venue labels
    venue_label = {}
    for index, venue_row in venue_selector.iterrows():
      # venue_label[venue_row['race_date']] = venue_row['venue_label']
      venue_label[venue_row['date_venue']] = venue_row['venue_label']
      # venue_label[venue_row['race_date']] = f"{venue_row['race_venue']} ({venue_row['race_date'].strfdate('%Y-%m-%d')})"
    # st.write(venue_label)
  
    # race_venue = st.selectbox('Løbsdag', options=venue_selector['race_date'].unique(), index=None, placeholder='Vælg løbsdag', format_func=lambda x: venue_label.get(x), width=300)
    date_venue = st.selectbox('Løbsdag', options=venue_selector['date_venue'].unique(), index=None, placeholder='Vælg løbsdag', format_func=lambda x: venue_label.get(x), width=300)
  
    if date_venue:
      # st.write(f'get races for {date_venue}')
  
      # Limit heat list based on race_venue
      heat_selector = venue_selector[venue_selector['date_venue'] == date_venue]
      # st.write(heat_selector)
      
      # Create data for heat labels
      heat_label = {}
      for index, heat_row in heat_selector.iterrows():
        if heat_row['race_name'] == '2wd':
          heat_name = heat_row['race_name']
        else:
          heat_name = f'4wd løb {heat_row['race_name']}'
        heat_label[heat_row['race_name']] = heat_name
      # st.write(heat_label)
    
      race_heat = st.selectbox('Løb', options=heat_selector['race_name'].unique(), index=None, placeholder='Vælg heat', format_func=lambda x: heat_label.get(x), width=300)
  
  return date_venue, race_heat
  
