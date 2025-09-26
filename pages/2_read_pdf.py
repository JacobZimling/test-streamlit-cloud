import streamlit as st
import PyPDF2

#st.pdf("https://pihl-zimling.dk/mlcrc/1308-Race-Slangerup-1a.pdf")

file = st.file_uploader("Upload a PDF file", type="pdf")

if file is not None:
    # Read the PDF file
    pdf_reader = PyPDF2.PdfReader(file)
    # Extract the content
    content = ""
    for page in range(len(pdf_reader.pages)):
        content += pdf_reader.pages[page].extractText()
    # Display the content
    st.write(content)
