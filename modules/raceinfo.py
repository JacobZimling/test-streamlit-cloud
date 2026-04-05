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
    query = f"""
		INSERT INTO race_graph (
				race_identifier, 
				driver_name,
				race_time_dt,
				lap
			)
		WITH 
			laps as (
				SELECT 
					wri.race_identifier, 
					rl.driver_id, 
					rl.race_time_dt, 
					rl.lap
				FROM race_laps as rl 
					JOIN w_race_identifier as wri 
						ON rl.race_id=wri.race_id 
			),
			racetime_laps as (
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
				LEFT JOIN laps as l 
					ON dt.race_identifier=l.race_identifier 
					and dt.driver_id = l.driver_id 
					AND dt.race_time_dt >= l.race_time_dt 
				WHERE dt.race_identifier='{race_identifier}' 
			)
			SELECT 
				rtl.race_identifier, 
				res_id.year_type_date_race,
				rtl.driver_id, */
				driver.driver_name,
				rtl.race_time_dt,
				CASE DSQ.DSQ
					WHEN 1 THEN 0
					ELSE coalesce(rtl.lap, 0) 
				END as lap
				FROM racetime_laps as rtl
					LEFT JOIN driver_name as driver
						ON rtl.driver_id=driver.driver_id
					LEFT JOIN w_race_identifier as wri
						ON rtl.race_identifier=wri.race_identifier
					LEFT JOIN w_result_identifier as res_id
						ON wri.race_id=res_id.race_id
					LEFT JOIN race_disqualified as DSQ
						ON res_id.year_type_date_race=DSQ.year_type_date_race
							and driver.driver_name=DSQ.driver_name
				WHERE rtl.rn = 1 
		;"""
    s.execute(text(query))
    s.commit()
  return
  
def get_lap_info(conn, date_venue, race_name):
  conn.reset()
  query = f'SELECT driver_name, race_time_dt, lap FROM race_graph WHERE race_identifier="{date_venue}{race_name}";'
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

def get_result_identifier(*args):
	return '¤'.join(list(map(str, args)))
	
def get_race_result_aggr(conn, *args):
	conn.reset()
	result_identifier = get_result_identifier(args)
	result_identifier = '¤'.join(list(map(str, args)))
	query = f'SELECT result_identifier, rank, driver_name, race_time_dt, lap, point, DNF_DSQ FROM race_result WHERE result_identifier="{result_identifier}" ORDER BY point DESC;'
	#st.write(query)
	race_result = conn.query(query, ttl=0)
	return race_result
	# return 

def set_dsq_flag(conn, result_identifier, driver_name):
	conn.reset()
	with conn.session as s:
		query = f"INSERT INTO race_disqualified (year_type_date_race, driver_name, DSQ) VALUES ('{result_identifier}', '{driver_name}', 1);"
		s.execute(text(query))
		s.commit()
	return

def update_race_result_data(conn, race_year):
	with conn.session as s:
	    query = f"DELETE FROM race_result WHERE result_identifier like '{race_year}¤%';"
	    s.execute(text(query))
	    query = f"""INSERT INTO race_result (
							result_identifier,
							rank,
							driver_name,
							race_time_dt,
							lap,
							point,
							DNF_DSQ
						)
					WITH 
						last_lap AS (
							SELECT
								year_type_date_race,
						    	year_type_date, 
						    	year_type,
							    race_identifier,
								elimination_race,
								ROW_NUMBER() OVER(
							        PARTITION BY year_type_date_race, race_identifier
									ORDER BY year_type_date_race, race_identifier, lap DESC, race_time_dt
								) AS rank,
								driver_name,
								race_time_dt,
								lap,
								DSQ
							FROM (
								SELECT
							    	result_id.year_type_date_race,
							    	result_id.year_type_date, 
							    	result_id.year_type,
							    	race_id.race_identifier,
							    	race_id.elimination_race,
							    	driver.driver_name,
									CASE dsq.DSQ
										WHEN 1 then '1900-01-01 00:00:00'
										else rl.race_time_dt
									END as race_time_dt,
									CASE dsq.DSQ
										WHEN 1 then 0
										else rl.lap
									END as lap,
									dsq.DSQ,
									ROW_NUMBER() OVER(
										PARTITION BY result_id.year_type_date_race, result_id.year_type_date, result_id.year_type, race_id.race_identifier, driver.driver_name
										ORDER BY result_id.year_type_date_race, race_id.race_identifier, driver.driver_name, rl.lap DESC
									) AS rn
								FROM `race_laps` as rl
							    	JOIN w_race_identifier as race_id
							    		ON rl.race_id=race_id.race_id
							    	JOIN w_result_identifier as result_id
							    		ON rl.race_id=result_id.race_id
							    	LEFT JOIN driver_name as driver
							    		ON rl.driver_id=driver.driver_id
							    	LEFT JOIN race_disqualified as dsq
							    		ON result_id.year_type_date_race=dsq.year_type_date_race
							    			and driver.driver_name=dsq.driver_name
									LEFT JOIN w_race_info as wri
										ON rl.race_id=wri.race_id
								WHERE wri.race_year={race_year}
							) sub
							WHERE rn = 1
						),
						point_info AS (
							SELECT 
							    ll.year_type_date_race,
						    	ll.year_type_date, 
						    	ll.year_type,
							    ll.rank,
							    ll.driver_name,
							    ll.race_time_dt,
							    ll.lap,
							    ll.DSQ,
							    max(ll.lap) OVER (
							    	partition by ll.year_type_date_race
							    )/2 as lap_point_limit,
							    ll.elimination_race,
							    p.point
							FROM last_lap as ll
								LEFT JOIN race_points as p
									ON ll.rank = p.rank
						    ORDER BY ll.year_type_date_race, p.point DESC
						),
						point_dnf as (
							SELECT 
							    year_type_date_race,
						    	year_type_date, 
						    	year_type,
							    rank,
							    driver_name,
							    race_time_dt,
							    lap,
							    lap_point_limit,
							    elimination_race,
							    point,
								CASE 
									WHEN DSQ=1 then 0
									WHEN elimination_race=1 and lap<3 THEN 0
									WHEN elimination_race=0 and lap<lap_point_limit THEN 0
									ELSE point
								END as result_point,
								CASE 
									WHEN DSQ=1 then 0
									WHEN elimination_race=1 and lap<3 THEN 0
									WHEN elimination_race=0 and race_time_dt<'1900-01-01 00:07:00' THEN 0
									WHEN elimination_race=0 and lap<lap_point_limit THEN 0
									ELSE point
								END as result_point_2,
								CASE 
									WHEN DSQ=1 then 'DSQ'
									WHEN elimination_race=1 and lap<3 THEN 'DNF'
									WHEN elimination_race=0 and lap<lap_point_limit THEN 'DNF'
									ELSE NULL
								END as DNF_DSQ
							FROM point_info
						),
						final_result AS (
							SELECT 
								year_type as race_identifier,
								ROW_NUMBER() OVER (
									PARTITION BY race_identifier
									ORDER BY race_identifier, point DESC
								) as rank,
								driver_name,
								NULL as race_time_dt,
								NULL as lap,
								sum(result_point) as point,
								sum(result_point_2) as point_2,
								NULL as DNF_DSQ
								FROM point_dnf 
								GROUP BY year_type, driver_name
							UNION ALL
							SELECT 
								year_type_date as race_identifier,
								ROW_NUMBER() OVER (
									PARTITION BY race_identifier
									ORDER BY race_identifier, point DESC
								) as rank,
								driver_name,
								NULL as race_time_dt,
								NULL as lap,
								sum(result_point) as point,
								sum(result_point_2) as point_2,
								NULL as DNF_DSQ
								FROM point_dnf 
								GROUP BY year_type_date, driver_name
							UNION ALL
							SELECT 
								year_type_date_race as race_identifier,
								ROW_NUMBER() OVER (
									PARTITION BY race_identifier
									ORDER BY race_identifier, lap DESC, point DESC, DNF_DSQ
								) as rank,
								driver_name,
								race_time_dt,
								lap,
								result_point as point,
								result_point_2 as point_2,
								DNF_DSQ
								FROM point_dnf 
								order by race_identifier, rank 
						)
						SELECT
							race_identifier,
							rank,
							driver_name,
							race_time_dt,
							lap,
							point,
							DNF_DSQ
							FROM final_result
 			;"""
	    s.execute(text(query))
	    s.commit()
	return

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
  
