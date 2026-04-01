import streamlit as st
from modules import raceinfo as race

# Initialize DB connection.
conn = race.db_connect()

# Read race information for exlect boxes from DB
races = race.get_race_info(conn)
st.write(races)

# Select year
race_year = st.selectbox('År', options=races['race_year'].unique(), index=None, placeholder='Vælg år', width=300)

if race_year:

    # Select race type (2wd/4wd)
    race_type = st.segmented_control(
        'Løbstype',
        races[races['race_year']==race_year]['race_type'].unique()
    )

    venue_label = {}
    for index, venue_row in races[races['race_year']==race_year].iterrows():
        venue_label[venue_row['date_venue']] = venue_row['venue_label']
        
    date_venue = st.segmented_control(
        'Løbsdag',
        races[races['race_year']==race_year]['date_venue'].unique(),
        format_func=lambda x: venue_label.get(x)
    )

    if race_type != '2wd':
        race_label = {}
        for index, race_row in races[races['race_year']==race_year].iterrows():
          if race_row['race_name'] == '2wd':
            race_name = race_row['race_name']
          else:
            race_name = f'4wd løb {heat_row['race_name']}'
          race_label[race_row['race_name']] = race_name
        # st.write(heat_label)
      
        race_name = st.segmented_control(
            'Løb', 
            races[races['race_year']==race_year]['race_name'].unique(), 
            format_func=lambda x: race_label.get(x)
        )
    
    st.write(f'{race_type} {date_venue} {race_name}')

    # if race_type:
    #     race_result = race.get_race_result_aggr(conn, race_year, race_type)
    
    #     st.dataframe(
    #         race_result, 
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
    
