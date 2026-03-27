import streamlit as st
from pypdf import PdfReader
import re
from datetime import datetime
from sqlalchemy.sql import text

#st.pdf("https://pihl-zimling.dk/mlcrc/1308-Race-Slangerup-1a.pdf")

file = st.file_uploader("Upload a PDF file", type="pdf")

if file is not None:
    # Initialize DB connection.
    conn = st.connection('heliohost', type='sql')
    
    # Read the PDF file
    pdf_reader = PdfReader(file)
    # Extract the content
    for page in range(len(pdf_reader.pages)):
        #st.write(page)
        page_text = pdf_reader.pages[page].extract_text()
        # st.write(page_text)

        if page == 0:
            st.write('extract race info')
            # st.write(page_text)

            race_info = re.findall(r'Session name: ([\włæøåÆØÅ]+) ((\d)([abe])|(2wd))\.? Session started: (\w{3} \d{2}, \d{4})', page_text, re.IGNORECASE)[0]
            st.write(race_info)
            race_name = race_info[2] or race_info[4]
            # st.write(f'Venue: {race_info[0]} Race name: {race_name} Heat: {race_info[3]}')
            race_date = datetime.strptime(race_info[5], "%b %d, %Y").date()
            # st.write(type(race_date))

            # Check if race exist
            # st.write(f"SELECT race_id FROM race_info WHERE race_date='{race_date}' and race_venue='{race_info[0]}' and race_name='{race_name}' and race_heat='{race_info[3]}';")
            df = conn.query(f"SELECT race_id FROM race_info WHERE race_date='{race_date}' and race_venue='{race_info[0]}' and race_name='{race_name}' and race_heat='{race_info[3]}';", ttl=0)
            #st.write(df.empty)
            #st.dataframe(df)

            # Add race info if race is new
            if df.empty:
                # st.write('insert race info')
                with conn.session as s:
                    data = [(race_date.strftime('%Y-%m-%d'), race_info[0], race_name, race_info[3])]
                    # st.write(data)
                    for k in data:
                        s.execute(
                            text('INSERT INTO race_info (race_date, race_venue, race_name, race_heat) VALUES (:date, :venue, :name, :heat);'),
                            params=dict(date=k[0], venue=k[1], name=k[2], heat=k[3])
                        )
                    s.commit()
                
                # Get race_id
                df = conn.query(f"SELECT * FROM race_info WHERE race_date='{race_date}' and race_venue='{race_info[0]}' and race_name='{race_name}' and race_heat='{race_info[3]}';", ttl=0)
                # st.dataframe(df)

            race_id = df['race_id'].iloc[0]
            # st.write(race_id)
            # st.dataframe(df)

            st.write('extract race times')
            racetime_info = re.findall(r'(\d+)\. (\w[\w ]+)\.? (\d{2}:\d{2}.\d{3})', page_text)
            #st.write(racetime_info)
            race_result = {}
            for r in racetime_info:
                race_result[r[1]] = r[2]
            # st.write(race_result)
        
        elif page != 1:
            st.write('extract lap times')
            # st.write(page_text)

            lap_info = re.findall(r'(\d+) (\w[\w ]+)\.? (\d{2}:\d{2}.\d{3}) (\+.{5,6}) (\d{2}:\d{2}.\d{3}) (\d+)\.', page_text)
            # st.write(lap_info)

            # st.write(lap_info[0][2])
            # time = datetime.strptime(lap_info[0][2], '%M:%S.%f').time().strftime('%H:%M:%S.%f')
            # st.write(time)
            # st.write(type(time))
            # st.write(type(lap_info[0][2]))

            with conn.session as s:
                query = f"DELETE FROM race_laps WHERE race_id={race_id} and driver_id='{lap_info[0][1]}';"
                # st.write(query)
                s.execute(text(query))
                race_time = datetime.strptime("00:00:00", "%H:%M:%S")
                # st.write(type(race_time))
                st.write(race_time)
                s.execute(
                    text('INSERT INTO race_laps (race_id, lap, driver_id) VALUES (:race_id, :lap, :driver_id);'),
                    params = dict(race_id=race_id, lap=0, driver_id=lap_info[0][1])
                )
                for lap in lap_info:
                    race_time += datetime.strptime(lap[2], '%M:%S.%f') - datetime.strptime("00:00:00", "%H:%M:%S")
                    # st.write(f'{race_time.strftime("0000-00-00 %H:%M:%S.%f")} # {datetime.strptime(race_result[lap_info[0][1]], '%M:%S.%f')-race_time}')
                    # st.write(f"{datetime.strptime(lap[2], '%M:%S.%f').strftime('0000-00-00 %H:%M:%S.%f')}, {race_time_dt=race_time.strftime('%H:%M:%S.%f')}")
                    # st.write(f'{datetime.strptime(lap[2], '%M:%S.%f').time().strftime('%H:%M:%S.%f')} {race_time.time().strftime('%H:%M:%S.%f')}')
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
                            lap_time_dt=datetime.strptime(lap[2], '%M:%S.%f').strftime('0000-00-00 %H:%M:%S.%f'), 
                            race_time_dt=race_time.strftime("0000-00-00 %H:%M:%S.%f")
                        )
                    )
                rt = datetime.strptime(race_result[lap_info[0][1]], '%M:%S.%f')
                race_time_corr = (datetime.min + (rt-race_time)).time()
                st.write(race_time_corr)
                st.write(type(race_time_corr))
                # st.write(f'{datetime.strptime(race_result[lap_info[0][1]], '%M:%S.%f')-race_time}')
                st.write(f'{rt} {race_time} {rt-race_time} {race_time_corr}')
                # query = f"UPDATE race_laps SET race_time=ADDTIME(race_time, '{datetime.strptime(race_result[lap_info[0][1]], '%M:%S.%f')-race_time}') WHERE race_id={race_id} and driver_id='{lap_info[0][1]}';"
                # query = f"UPDATE race_laps SET race_time=ADDTIME(race_time, '{datetime.strptime(race_result[lap_info[0][1]], '%M:%S.%f')-race_time}'), race_time_dt=ADDTIME(race_time_dt, '{datetime.strptime(race_result[lap_info[0][1]], '%M:%S.%f')-race_time}') WHERE race_id={race_id} and driver_id='{lap_info[0][1]}';"
                query = f"UPDATE race_laps SET race_time=ADDTIME(race_time, '{datetime.strptime(race_result[lap_info[0][1]], '%M:%S.%f')-race_time}') WHERE race_id={race_id} and driver_id='{lap_info[0][1]}';"
                st.write(query)
                s.execute(text(query))
                # query = f"UPDATE race_laps SET race_time_dt=DATE_ADD(race_time_dt, INTERVAL '{datetime.strptime(race_result[lap_info[0][1]], '%S.%f')-race_time}') WHERE race_id={race_id} and driver_id='{lap_info[0][1]}';"
                # st.write(query)
                # s.execute(text(query))
                s.commit()
                

            # # Get lap info
            df = conn.query(f"SELECT * FROM race_laps WHERE race_id='{race_id}' and driver_id='{lap_info[0][1]}';", ttl=0)
            st.dataframe(df)
            # df['lap_time_f'] = df['lap_time'].dt.strftime('%M:%S.%f')
            # df['race_time_f'] = df['race_time'].dt.strftime('%M:%S.%f')
            # st.dataframe(df)
