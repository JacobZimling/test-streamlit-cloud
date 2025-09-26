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

        match page:
            case 0:
                #race_info = re.findall(r'(Session name): (.+) (Session started): (.+) Session time: .+ (Session ended): (.+) Pos', page_text)
                race_info = re.findall(r'(Session name): (.+) (Session started): (.+ PM) ', page_text)
                st.write(race_info)

    # Display the content
    #st.write(content)
