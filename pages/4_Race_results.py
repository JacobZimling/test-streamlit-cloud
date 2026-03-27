import streamlit as st
from modules import raceinfo as race

# Initialize DB connection.
# conn = st.connection('heliohost', type='sql')
conn = race.db_connect()

# https://search.brave.com/search?q=streamlit+scascading+selectboxes+from+dataframe&summary=1&conversation=76d7adeeee7a87c717e6d4
# https://discuss.streamlit.io/t/format-func-function-examples-please/11295/4

# Read race information from DB
races = race.get_race_info(conn)
# st.write(races)

# Select year
race_year = st.selectbox('År', options=races['race_year'].unique(), index=None, placeholder='Vælg år', width=300)

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
  
    race_heat = st.selectbox('Løb', options=heat_selector['race_name'].unique(), index=None, placeholder='Vælg løb', format_func=lambda x: heat_label.get(x), width=300)

    if race_heat:
      st.write(f'Show results {date_venue}, {race_heat}')
      df = race.get_race_result(conn, date_venue, race_heat)
      # st.write(type(df))
      st.dataframe(
        df, 
        hide_index=True,
        column_config={
            "rank": st.column_config.NumberColumn("Placering"),
            "driver_id": st.column_config.NumberColumn("Kører"),
            "race_time": st.column_config.NumberColumn("Tid"),
            "lap": st.column_config.NumberColumn("Omgange"),
            "point": st.column_config.NumberColumn("Point"),
        }
      )

