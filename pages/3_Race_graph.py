# 3_Race_graph.py

import streamlit as st
# from modules.raceinfo import Race
from modules import raceinfo as race

# Initialize DB connection.
# conn = st.connection('heliohost', type='sql')
conn = race.db_connect()

# race = Race()

# race.select_race_year
# years = race.get_race_years
# st.write(type(years))
# st.write(years)
# st.dataframe(race.get_race_years)

years = race.get_race_years(conn)
# st.write(type(years))
st.write(years)
race_year = st.selectbox('År', years['race_year'], index=None, placeholder='Vælg år')

if race_year:
  st.write('get races for the selected year')
  races = race.get_races(conn, race_year)
  st.write(races)
  st.write(races.loc[races['race_date'] == '2025-06-15'])
  st.write(races.loc[races['race_date'] == '2025-06-15']['race_venue'])
  date = '2025-06-15'
  st.write(races.query(f"race_date == '{date}'"))
  st.selectbox('Løbsdag', races['race_date'], index=None, placeholder='Vælg løbsdag', format_func=lambda x: races.loc[races['race_date'] == x])

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
