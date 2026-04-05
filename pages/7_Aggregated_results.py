import streamlit as st
from modules import raceinfo as race

if 'mode' in st.query_params:
    mode = st.query_params.mode
else:
    mode = ''
    
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
            columns = ('rank', 'driver_name', 'race_time_dt', 'lap', 'point')
            if mode=='DSQ':
                on_select = "rerun"
            else:
                on_select = "ignore"
        elif race_date:
            # st.write('year_type_date')
            # st.write(race.result_identifier(race_year, race_type, race_date))
            race_result = race.get_race_result_aggr(conn, race_year, race_type, race_date)
            columns = ('rank', 'driver_name', 'point')
            on_select = "ignore"
        else:
            # st.write('year_type')
            # st.write(race.result_identifier(race_year, race_type))
            race_result = race.get_race_result_aggr(conn, race_year, race_type)
            columns = ('rank', 'driver_name', 'point')
            on_select = "ignore"

        #st.write('display result')
        # df.filter(items=['rank', 'driver_id', 'point']),
        import numpy as np
        #race_result['p'] = np.where(race_result['DNF_DSQ'] != [], race_result['DNF_DSQ'], race_result['point'])
        race_result['point'] = race_result[['DNF_DSQ', 'point']].bfill(axis=1).iloc[:, 0]
        driver = st.dataframe(
            race_result, 
            hide_index=True,
            height="content",
            width="content",
            column_order=columns,
            on_select=on_select,
            selection_mode="single-cell",
            #column_order=(),
            #placeholder="--",
            column_config={
                "rank": st.column_config.NumberColumn("Placering"),
                "driver_name": st.column_config.TextColumn("Kører"),
                "race_time_dt": st.column_config.TimeColumn("Total tid", format='m:ss.SSS'),
                "lap": st.column_config.NumberColumn("Omgange"),
                #"point": st.column_config.NumberColumn("Point"),
                "point": st.column_config.TextColumn("Point"),
            }
        )

        if mode=='DSQ':
            if driver:
                if len(driver.selection.cells) > 0:
                    #st.write(race_result.iloc[driver.selection.cells[0][0]])
                    #st.write(race_result.iloc[driver.selection.cells[0][0]]['result_identifier'])
                    if race_result.iloc[driver.selection.cells[0][0]]['DNF_DSQ'] != 'DSQ':
                        st.write(f'Er du sikker på at {race_result.iloc[driver.selection.cells[0][0]]['driver_name']} skal diskvalificeres i dette løb?')
                        if st.button('Ja', icon=":material/check:"):
                            st.write('set DSQ flag')
                        
