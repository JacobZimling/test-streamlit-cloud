import streamlit as st
from pypdf import PdfReader
import re

#st.pdf("https://pihl-zimling.dk/mlcrc/1308-Race-Slangerup-1a.pdf")

file = st.file_uploader("Upload a PDF file", type="pdf")

if file is not None:
    # Read the PDF file
    pdf_reader = PdfReader(file)
    # Extract the content
    content = ""
    for page in range(len(pdf_reader.pages)):
        st.write(page)
        page_text = pdf_reader.pages[page].extract_text()
        st.write(page_text)
        #content += page_text

        if page == 0:
            #race_info = re.findall(r'(Session name): (.+) (Session started): (.+)', page_text)
            #st.write(race_info)
            #race_info = re.findall(r'(Session time): (.+) (Session ended): (.+)', page_text)
            #st.write(race_info)

            #race_info = re.findall(r'(\w[\w ]+) (\d\d:\d\d.\d\d\d) (.+) (\d\d:\d\d.\d\d\d) (\d+)', page_text)
            #st.write(race_info)

            race_info = re.findall(r'Session name: (.+) Session started: (\w{3} \d{2}, \d{4})', page_text)[0]
            st.write(race_info)

        elif page != 1:
            st.write('extract lap times')

    # Display the content
    #st.write(content)
