import streamlit as st
from modules import raceinfo as race

# Initialize DB connection.
conn = race.db_connect()

# Read race information for exlect boxes from DB
races = race.get_race_info(conn)
# st.write(type(races))

# Select year
race_year = st.selectbox('År', options=races['race_year'].unique(), index=None, placeholder='Vælg år', width=300)

if race_year:

    # Select race type (2wd/4wd)
    race_type = st.selectbox('Løbstype', options=races[races['race_year']=race_year]['race_type'].unique(), index=None, placeholder='Vælg løbstype', width=300)

    # if race_type:
    

#     df = race.get_race_result_aggr(conn, race_year, date_venue, race_heat)
    
#     st.dataframe(
#         df, 
#         hide_index=True,
#         column_config={
#             "rank": st.column_config.NumberColumn("Placering"),
#             "driver_id": st.column_config.TextColumn("Kører"),
#             # "race_time": st.column_config.NumberColumn("Tid", format='%m:%s.%SSS'),
#             #"race_time": st.column_config.TimeColumn("Tid", format='DD-MM-YYYY HH.mm:ss.SSS'),
#             # "race_time": st.column_config.NumberColumn("Tid", format='%f'),
#             # "race_time": st.column_config.TimeColumn("Tid"),
#             "race_time_dt": st.column_config.TimeColumn("Total tid", format='m:ss.SSS'),
#             "lap": st.column_config.NumberColumn("Omgange"),
#             "point": st.column_config.NumberColumn("Point"),
#         }
#     )
    
