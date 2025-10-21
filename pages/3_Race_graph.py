# 3_Race_graph.py

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
race_year = st.selectbox('År', options=races['race_year'].unique(), index=None, placeholder='Vælg år')

if race_year:
  # st.write(f'get races for {race_year}')

  # Limit venue list based on race_year
  venue_selector = races[races['race_year'] == race_year]
  # st.write(venue_selector)
  # st.write(type(venue_selector))

  # Create data for venue labels
  venue_label = {}
  for index, venue_row in venue_selector.iterrows():
    venue_label[venue_row['race_date']] = venue_row['venue_label']
  # st.write(venue_label)

  race_venue = st.selectbox('Løbsdag', options=venue_selector['race_date'].unique(), index=None, placeholder='Vælg løbsdag', format_func=lambda x: venue_label.get(x))

  if race_venue:
    st.write(f'get races for {race_venue}')

    # Limit heat list based on race_venue
    heat_selector = venue_selector[venue_selector['race_date'] == race_venue]
    st.write(heat_selector)
    
    # Create data for heat labels
    heat_label = {}
    for index, heat_row in heat_selector.iterrows():
      if heat_row['race_name'] == '2wd':
        heat_name = heat_row['race_name']
      else:
        heat_name = f'4wd løb {heat_row['race_name']}'
      heat_label[heat_row['race_name']] = heat_name
    # st.write(heat_label)
  
  race_heat = st.selectbox('Heat', options=heat_selector['race_name'].unique(), index=None, placeholder='Vælg heat', format_func=lambda x: heat_label.get(x))

# Get lap data
#df = conn.query(f"SELECT lap, driver_id, lap_time, sum(lap_time) OVER (PARTITION BY driver_id ORDER BY lap) FROM race_laps WHERE race_id in (14, 15);", ttl=0)
# df = conn.query(
# df = race.conn.query(
#   'SELECT \
#       c.driver_id as driver_id, \
#       c.lap as lap, \
#       c.lap_time AS lap_time, \
#       IF(@prev_driver_id = c.driver_id, \
#          @race_time := addtime(@race_time, c.lap_time), \
#          @race_time := c.lap_time) AS race_time, \
#       @prev_driver_id := c.driver_id AS id \
#   FROM ( \
#       SELECT @prev_driver_id := NULL, \
#              @race_time := 0 \
#   ) i \
#   JOIN ( \
#       SELECT driver_id, lap, lap_time \
#       FROM race_laps \
#       WHERE race_id in (4,5) \
#       ORDER BY driver_id, lap \
#   ) c;',
#   ttl=0)
# st.dataframe(df)

# # st.line_chart(df, x='lap_time', y='lap')
# st.bar_chart(df, x='driver_id', y='lap', sort='driver_id', color='driver_id', stack=False)

# import plotly.express as px
# # st.write(px.bar(df, x="driver_id", y="lap", animation_frame="race_time", hover_name="driver_id"))
# st.write(px.bar(df, x="driver_id", y="lap", hover_name="driver_id", color='driver_id'))

# st.write(df['driver_id'])
# st.write(df['lap'])
# import plotly.graph_objects as go
# fig = go.Figure([go.Bar(x=df['driver_id'], y=df['lap'])])
# fig.update_layout(xaxis={'categoryorder':'total descending'})
# # st.write(fig.show())
# st.plotly_chart(fig, use_container_width=True)
