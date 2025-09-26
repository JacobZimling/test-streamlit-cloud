import streamlit as st
from pypdf import PdfReader

#st.pdf("https://pihl-zimling.dk/mlcrc/1308-Race-Slangerup-1a.pdf")

file = st.file_uploader("Upload a PDF file", type="pdf")

if file is not None:
    # Read the PDF file
    pdf_reader = PdfReader(file)
    # Extract the content
    content = ""
    for page in range(len(pdf_reader.pages)):
        st.write(page)
        st.write(pdf_reader.pages[page].extract_text())
    #    content += pdf_reader.pages[page].extract_text()
    # Display the content
    #st.write(content)
