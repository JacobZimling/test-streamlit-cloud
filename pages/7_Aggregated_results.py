import streamlit as st
from modules import raceinfo as race
#from modules.raceinfo import race_selector

if 'mode' in st.query_params:
    mode = st.query_params.mode
else:
    mode = ''
    
# Initialize DB connection.
conn = race.db_connect()

# Read race information for exlect boxes from DB
races = race.get_race_info(conn)

# Select year
race_year = st.segmented_control(
    'År',
    races['race_year'].unique()[::-1]
    ,label_visibility = 'collapsed'
    ,default = races['race_year'].max()
)

if race_year:

    # Select race type (2wd/4wd)
    race_type = st.segmented_control(
        'Løbstype',
        races[races['race_year']==race_year]['race_type'].unique()
        ,label_visibility = 'collapsed'
        ,default = '4wd'
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
        if race_date:
            if race_type == '4wd':
                race_label = {}
                for index, race_row in races[(races['race_year']==race_year) & (races['race_name']!='2wd')].iterrows():
                  if race_row['race_name'] == '2wd':
                    _race_name = race_row['race_name']
                  else:
                    _race_name = f'4wd løb {race_row['race_name']}'
                  race_label[race_row['race_name']] = _race_name

                race_name = st.segmented_control(
                    'Løb', 
                    races[(races['race_year']==race_year) & (races['race_name']!='2wd')]['race_name'].unique(), 
                    format_func=lambda x: race_label.get(x)
                    ,label_visibility = 'collapsed'
                )
            else:
                race_name = '2wd'

        if race_date and race_name:
            race_result = race.get_race_result_aggr(conn, race_year, race_type, race_date, race_name)
            columns = ('rank', 'driver_name', 'race_time_dt', 'lap', 'point')
            on_select = "rerun"
        elif race_date:
            race_result = race.get_race_result_aggr(conn, race_year, race_type, race_date)
            columns = ('rank', 'driver_name', 'point')
            on_select = "rerun"
        else:
            race_result = race.get_race_result_aggr(conn, race_year, race_type)
            columns = ('rank', 'driver_name', 'point')
            on_select = "ignore"

        race_result['point'] = race_result['point'].astype(str)
        race_result.loc[race_result['DNF_DSQ'].notna(), 'point'] = race_result['DNF_DSQ']
        driver = st.dataframe(
            race_result, 
            hide_index=True,
            height="content",
            width="content",
            column_order=columns,
            on_select=on_select,
            selection_mode="single-cell",
            column_config={
                "rank": st.column_config.NumberColumn("Placering"),
                "driver_name": st.column_config.TextColumn("Kører"),
                "race_time_dt": st.column_config.TimeColumn("Total tid", format='m:ss.SSS'),
                "lap": st.column_config.NumberColumn("Omgange"),
                "point": st.column_config.TextColumn("Point"),
            }
        )

        if race_name and driver:
            if mode=='DSQ':
                if len(driver.selection.cells) > 0:
                    if race_result.iloc[driver.selection.cells[0][0]]['DNF_DSQ'] != 'DSQ':
                        result_identifier = race_result.iloc[driver.selection.cells[0][0]]['result_identifier']
                        driver_name = race_result.iloc[driver.selection.cells[0][0]]['driver_name']
                        st.write(f'Er du sikker på at {driver_name} skal diskvalificeres i dette løb?')
                        if st.button('Ja', icon=":material/check:", type="primary"):
                            race.set_dsq_flag(conn, result_identifier, driver_name)
                            with st.spinner('Updating race result data...', show_time=True):
                                race.update_race_result_data(conn, result_identifier.split('¤', 1)[0])
                            st.success('Race result data updated')
            else:
                if len(driver.selection.cells) > 0:
                    st.write(f"Omgangstider for {race_result.iloc[driver.selection.cells[0][0]]['driver_name']}")
                    lap_times = race.get_lap_times(conn,
                                                   race_result.iloc[driver.selection.cells[0][0]]['result_identifier'],
                                                   race_result.iloc[driver.selection.cells[0][0]]['driver_name'])
                    st.dataframe(
                        lap_times,
                        hide_index = True,
                        height="content",
                        column_config={
                            "lap": st.column_config.NumberColumn("Omgang"),
                            "driver_name": st.column_config.TextColumn("Kører"),
                            "lap_time_dt": st.column_config.TimeColumn("Omgangstid", format='m:ss.SSS'),
                            "rank": st.column_config.NumberColumn("Rank"),
                        }
                    )

        elif race_date and driver:
            if len(driver.selection.cells) > 0:
                st.write(f'Dagens resultater for {race_result.iloc[driver.selection.cells[0][0]]['driver_name']}')
                driver_results = race.get_all_races_driver(conn, race_result.iloc[driver.selection.cells[0][0]]['result_identifier'], race_result.iloc[driver.selection.cells[0][0]]['driver_name'])
                st.dataframe(
                    driver_results,
                    hide_index=True,
                    height="content",
                    column_config={
                        "race_number": st.column_config.TextColumn("Løb"),
                        "rank": st.column_config.NumberColumn("Placering"),
                        "driver_name": st.column_config.TextColumn("Kører"),
                        "race_time_dt": st.column_config.TimeColumn("Total tid", format='m:ss.SSS'),
                        "lap": st.column_config.NumberColumn("Omgange"),
                        "point": st.column_config.TextColumn("Point"),
                    }
                )
