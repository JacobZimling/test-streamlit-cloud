import streamlit as st
from modules import raceinfo as race

# Initialize DB connection.
conn = race.db_connect()

# Read race information for exlect boxes from DB
races = race.get_race_info(conn)
# st.write(races)

# Select year
# race_year = st.selectbox('År', options=races['race_year'].unique(), index=None, placeholder='Vælg år', width=300)
race_year = st.segmented_control(
    'År',
    races['race_year'].unique()
    ,label_visibility = 'collapsed'
)

if race_year:

    # Select race type (2wd/4wd)
    race_type = st.segmented_control(
        'Løbstype',
        races[races['race_year']==race_year]['race_type'].unique()
        ,label_visibility = 'collapsed'
    )

    if race_type:
        venue_label = {}
        for index, venue_row in races[races['race_year']==race_year].iterrows():
            venue_label[venue_row['race_date']] = venue_row['venue_label']
            
        race_date = st.segmented_control(
            'Løbsdag',
            races[races['race_year']==race_year]['race_date'].unique(),
            format_func=lambda x: venue_label.get(x)
            ,label_visibility = 'collapsed'
        )
    
        race_name = None
        if race_date and race_type == '4wd':
            race_label = {}
            for index, race_row in races[(races['race_year']==race_year) & (races['race_name']!='2wd')].iterrows():
              if race_row['race_name'] == '2wd':
                _race_name = race_row['race_name']
              else:
                _race_name = f'4wd løb {race_row['race_name']}'
              race_label[race_row['race_name']] = _race_name
            # st.write(race_label)
          
            race_name = st.segmented_control(
                'Løb', 
                races[(races['race_year']==race_year) & (races['race_name']!='2wd')]['race_name'].unique(), 
                format_func=lambda x: race_label.get(x)
                ,label_visibility = 'collapsed'
            )
        else:
            race_name = '2wd'
        
        # st.write('Selections')
        # st.write(f'race: {race_type}')
        # st.write(f'date: {race_date}')
        # st.write(f' name: {race_name}')

        if race_date and race_name:
            # st.write('year_type_date_race')
            # st.write(race.result_identifier(race_year, race_type, race_date, race_name))
            race_result = race.get_race_result_aggr(conn, race_year, race_type, race_date, race_name)
        elif race_date:
            # st.write('year_type_date')
            # st.write(race.result_identifier(race_year, race_type, race_date))
            race_result = race.get_race_result_aggr(conn, race_year, race_type, race_date)
        else:
            # st.write('year_type')
            # st.write(race.result_identifier(race_year, race_type))
            race_result = race.get_race_result_aggr(conn, race_year, race_type)

        #st.write('display result')
        # df.filter(items=['rank', 'driver_id', 'point']), 
        st.dataframe(
            race_result, 
            hide_index=True,
            #height="content",
            #column_order=(),
            #placeholder="--",
            column_config={
                "rank": st.column_config.NumberColumn("Placering"),
                "driver_id": st.column_config.TextColumn("Kører"),
                # "race_time": st.column_config.NumberColumn("Tid", format='%m:%s.%SSS'),
                #"race_time": st.column_config.TimeColumn("Tid", format='DD-MM-YYYY HH.mm:ss.SSS'),
                # "race_time": st.column_config.NumberColumn("Tid", format='%f'),
                # "race_time": st.column_config.TimeColumn("Tid"),
                "race_time_dt": st.column_config.TimeColumn("Total tid", format='m:ss.SSS'),
                "lap": st.column_config.NumberColumn("Omgange"),
                "point": st.column_config.NumberColumn("Point"),
            }
        )
    
