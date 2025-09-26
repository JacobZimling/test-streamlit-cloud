import streamlit as st
from pypdf import PdfReader
import re
from datetime import datetime

#st.pdf("https://pihl-zimling.dk/mlcrc/1308-Race-Slangerup-1a.pdf")

file = st.file_uploader("Upload a PDF file", type="pdf")

if file is not None:
    # Initialize connection.
    #conn = st.connection('freesqldatabase', type='sql')
    
    # Read the PDF file
    pdf_reader = PdfReader(file)
    # Extract the content
    content = ""
    for page in range(len(pdf_reader.pages)):
        st.write(page)
        page_text = pdf_reader.pages[page].extract_text()
        #st.write(page_text)
        #content += page_text

        if page == 0:
            st.write('extract race info')
            st.write(page_text)
            #race_info = re.findall(r'(Session name): (.+) (Session started): (.+)', page_text)
            #st.write(race_info)
            #race_info = re.findall(r'(Session time): (.+) (Session ended): (.+)', page_text)
            #st.write(race_info)

            #race_info = re.findall(r'(\w[\w ]+) (\d\d:\d\d.\d\d\d) (.+) (\d\d:\d\d.\d\d\d) (\d+)', page_text)
            #st.write(race_info)

            race_info = re.findall(r'Session name: (.+) Session started: (\w{3} \d{2}, \d{4})', page_text)[0]

            race_date = datetime.strptime(race_info[1], "%b %d, %Y").date()
            #st.write(race_date)
            #st.write(race_info)
            query = f"INSERT INTO race_info (race_date, race_name) VALUES ('{race_date}', '{race_info[0]}')"
            st.write(query)

        elif page != 1:
            st.write('extract lap times')
            st.write(page_text)

            lap_info = re.findall(r'(\d+) (\w[\w ]+) (\d{2}:\d{2}.\d{3}) (\+.{5}) (\d{2}:\d{2}.\d{3}) (\d+)\.', page_text)
            st.write(type(lap_info))

    # Display the content
    #st.write(content)
