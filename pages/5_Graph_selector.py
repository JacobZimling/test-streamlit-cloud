# 3_Race_graph.py

import streamlit as st
from modules import raceinfo as race

# Initialize DB connection.
# conn = st.connection('heliohost', type='sql')
conn = race.db_connect()

# https://search.brave.com/search?q=streamlit+scascading+selectboxes+from+dataframe&summary=1&conversation=76d7adeeee7a87c717e6d4
# https://discuss.streamlit.io/t/format-func-function-examples-please/11295/4

date_venue, race_heat = race.race_selector(conn)
st.write(f'date_venue: {date_venue} race_heat: {race_heat}')
# Get lap data for selected heat
# st.write(f'race_heat {race_heat}')
# df = race.get_lap_info(conn, date_venue, race_heat)
# st.dataframe(df)

# import plotly.express as px
# import plotly.graph_objects as go
# import math
# fig = px.bar(df, x="driver_id", y="lap", animation_frame="race_time", hover_name="driver_id", range_y=[0, math.ceil(df['lap'].max() / 5) * 5])
# fig.update_layout(xaxis={'categoryorder':'total descending'}, xaxis_title='Kører', yaxis_title='Omgange')
# st.write(fig)

