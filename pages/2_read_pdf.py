import streamlit as st
from pypdf import PdfReader
import re
from datetime import datetime
from sqlalchemy.sql import text

#st.pdf("https://pihl-zimling.dk/mlcrc/1308-Race-Slangerup-1a.pdf")

file = st.file_uploader("Upload a PDF file", type="pdf")

if file is not None:
    # Initialize DB connection.
    conn = st.connection('freesqldatabase', type='sql')
    
    # Read the PDF file
    pdf_reader = PdfReader(file)
    # Extract the content
    for page in range(len(pdf_reader.pages)):
        #st.write(page)
        page_text = pdf_reader.pages[page].extract_text()
        #st.write(page_text)

        if page == 0:
            st.write('extract race info')
            # st.write(page_text)

            race_info = re.findall(r'Session name: (.+) Session started: (\w{3} \d{2}, \d{4})', page_text)[0]
            race_date = datetime.strptime(race_info[1], "%b %d, %Y").date()
            # st.write(type(race_date))
            # st.write(race_info)

            # Check if race exist
            df = conn.query(f"SELECT race_id FROM race_info WHERE race_date='{race_date}' and race_name='{race_info[0]}';", ttl=0)
            #st.write(df.empty)
            #st.dataframe(df)

            # Add race info if race is new
            if df.empty:
                st.write('insert race info')
                with conn.session as s:
                    data = [(race_date.strftime('%Y-%m-%d'), race_info[0])]
                    st.write(data)
                    for k in data:
                        s.execute(
                            text('INSERT INTO race_info (race_date, race_name) VALUES (:date, :name);'),
                            params=dict(date=k[0], name=k[1])
                        )
                    s.commit()
                
                # Get race_id
                df = conn.query(f"SELECT race_id FROM race_info WHERE race_date='{race_date}' and race_name='{race_info[0]}';", ttl=0)
                st.dataframe(df)

            race_id = df['race_id'].iloc[0]
            st.write(race_id)
        
        elif page != 1:
            st.write('extract lap times')
            st.write(page_text)

            lap_info = re.findall(r'(\d+) (\w[\w ]+) (\d{2}:\d{2}.\d{3}) (\+.{5}) (\d{2}:\d{2}.\d{3}) (\d+)\.', page_text)
            # st.write(lap_info)

            st.write(lap_info[0][2])
            time = datetime.strptime(lap_info[0][2], '%M:%S.%f').time().strftime('%H:%M:%S.%f')
            st.write(time)
            # st.write(type(time))
            # st.write(type(lap_info[0][2]))

            with conn.session as s:
                query = f"DELETE FROM race_laps WHERE race_id={race_id} and driver_id='{lap_info[0][1]}';"
                st.write(query)
                s.execute(text(query))
                for lap in lap_info:
                    s.execute(
            #             text('INSERT INTO race_laps (race_id, lap, driver_id, lap_time, dif, rank) VALUES (:race_id, :lap, :driver_id, :lap_time, :dif, rank);'),
                        text('INSERT INTO race_laps (race_id, lap, driver_id, lap_time, dif, rank) VALUES (:race_id, :lap, :driver_id, :lap_time, :dif, rank);'),
                        params = dict(race_id=race_id, lap=lap[0], driver_id=lap[1], lap_time=datetime.strptime(lap[2], '%M:%S.%f').time().strftime('%H:%M:%S.%f'), dif=lap[3], rank=lap[5])
                    )
                s.commit()

            # # Get lap info
            df = conn.query(f"SELECT * FROM race_laps WHERE race_id='{race_id}' and driver_id='{lap_info[0][1]}';", ttl=0)
            st.dataframe(df)

