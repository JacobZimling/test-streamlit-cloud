import streamlit as st
from pypdf import PdfReader
import re
from datetime import datetime
from sqlalchemy.sql import text
from modules import raceinfo as race

#st.pdf("https://pihl-zimling.dk/mlcrc/1308-Race-Slangerup-1a.pdf")

file = st.file_uploader("Upload a PDF file", type="pdf")

if file is not None:
    # Initialize DB connection.
    conn = st.connection('heliohost', type='sql')
    
    with st.spinner('Reading race information...', show_time=True):
        # Read the PDF file
        pdf_reader = PdfReader(file)
        # Extract the content
        for page in range(len(pdf_reader.pages)):
            page_text = pdf_reader.pages[page].extract_text()
    
            if page == 0:
                # Extract race info
                race_info = re.findall(r'Session name: ([\włæøåÆØÅ]+) ((\d)([abe])|(2wd))\.? Session started: (\w{3} \d{2}, \d{4})', page_text, re.IGNORECASE)[0]
                race_name = race_info[2] or race_info[4]
                race_date = datetime.strptime(race_info[5], "%b %d, %Y").date()
    
                # Check if race exist
                df = conn.query(f"SELECT race_id, CONCAT(race_date, race_venue, race_name) AS race_identifier FROM race_info WHERE race_date='{race_date}' and race_venue='{race_info[0]}' and race_name='{race_name}' and race_heat='{race_info[3]}';", ttl=0)
    
                # Add race info if race is new
                if df.empty:
                    with conn.session as s:
                        data = [(race_date.strftime('%Y-%m-%d'), race_info[0], race_name, race_info[3])]
                        for k in data:
                            s.execute(
                                text('INSERT INTO race_info (race_date, race_venue, race_name, race_heat) VALUES (:date, :venue, :name, :heat);'),
                                params=dict(date=k[0], venue=k[1], name=k[2], heat=k[3])
                            )
                        s.commit()
                    
                    # Get race_id
                    st.write(f"SELECT race_id, CONCAT(race_date, race_venue, race_name) AS race_identifier FROM race_info WHERE race_date='{race_date}' and race_venue='{race_info[0]}' and race_name='{race_name}' and race_heat='{race_info[3]}';")
                    df = conn.query(f"SELECT race_id, CONCAT(race_date, race_venue, race_name) AS race_identifier FROM race_info WHERE race_date='{race_date}' and race_venue='{race_info[0]}' and race_name='{race_name}' and race_heat='{race_info[3]}';", ttl=0)
    
                race_id = df['race_id'].iloc[0]
                race_identifier = df['race_identifier'].iloc[0]

                # Extract race totals
                racetime_info = re.findall(r'(\d+)\. (\w[\w ]+)\.? (\d{2}:\d{2}.\d{3})', page_text)
                race_result = {}
                for r in racetime_info:
                    race_result[r[1]] = r[2]
            
            elif page != 1:
                # Extract lap times
                lap_info = re.findall(r'(\d+) (\w[\w ]+)\.? (\d{2}:\d{2}.\d{3}) (\+.{5,6}) (\d{2}:\d{2}.\d{3}) (\d+)\.', page_text)

                with conn.session as s:
                    # Delete lap times if exist i DB
                    query = f"DELETE FROM race_laps WHERE race_id={race_id} and driver_id='{lap_info[0][1]}';"
                    s.execute(text(query))

                    # Write lap times to DB
                    race_time = datetime.strptime("00:00:00", "%H:%M:%S")
                    s.execute(
                        text('INSERT INTO race_laps (race_id, lap, driver_id) VALUES (:race_id, :lap, :driver_id);'),
                        params = dict(race_id=race_id, lap=0, driver_id=lap_info[0][1])
                    )
                    for lap in lap_info:
                        race_time += datetime.strptime(lap[2], '%M:%S.%f') - datetime.strptime("00:00:00", "%H:%M:%S")
                        s.execute(
                            text('INSERT INTO race_laps (race_id, lap, driver_id, lap_time, dif, rank, race_time, lap_time_dt, race_time_dt) VALUES (:race_id, :lap, :driver_id, :lap_time, :dif, :rank, :race_time, :lap_time_dt, :race_time_dt);'),
                            params = dict(
                                race_id=race_id, 
                                lap=lap[0], 
                                driver_id=lap[1], 
                                lap_time=datetime.strptime(lap[2], '%M:%S.%f').time().strftime('%H:%M:%S.%f'), 
                                dif=lap[3], 
                                rank=lap[5], 
                                race_time=race_time.time().strftime('%H:%M:%S.%f'), 
                                lap_time_dt=datetime.strptime(lap[2], '%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S.%f'), 
                                race_time_dt=race_time.strftime("%Y-%m-%d %H:%M:%S.%f")
                            )
                        )
                    race_time_corr = datetime.strptime(race_result[lap_info[0][1]], '%M:%S.%f')-race_time
                    query = f"UPDATE race_laps SET race_time=ADDTIME(race_time, '{race_time_corr}'), race_time_dt=ADDTIME(race_time_dt, '{race_time_corr}') WHERE race_id={race_id} and driver_id='{lap_info[0][1]}';"
                    s.execute(text(query))
                    s.commit()
    
                # Get lap info - for verification purposes
                # df = conn.query(f"SELECT * FROM race_laps WHERE race_id='{race_id}' and driver_id='{lap_info[0][1]}';", ttl=0)
                # st.dataframe(df)
    st.success('Race information processed')

    # Update race graph data
    with st.spinner('Updating race graph data...', show_time=True):
        race.update_race_graph_data(conn, race_identifier)
    st.success('Race graph data updated')
    
