import streamlit as st

pg = st.navigation([
    st.Page("pages/2_Read_lapsnapper_pdf_file.py"),
    st.Page("pages/3_Race_graph.py"),
])
pg.run()

# Define visible and invisible pages
#visible_page = st.Page("pages/2_Read_lapsnapper_pdf_file.py", title="Read lapsnapper pdf file")
#invisible_page = st.Page("pages/1_Test_db_connection_to_dreamhost.py", title=" ")  # Empty title hides it

# Create navigation with only visible pages
#page = st.navigation([visible_page])
#page.run()   

#from st_pages import show_pages, hide_pages, Page

#show_pages([
#    Page("home.py"),
#    Page("pages/1_Test_db_connection_to_dreamhost.py"),
#    Page("pages/2_Read_lapsnapper_pdf_file.py"),
#    Page("pages/3_Race_graph.py"),
#    Page("pages/4_Race_results.py"),
#    Page("pages/5_Graph_selector.py"),
#    Page("pages/5_Test.py"),
#    Page("pages/7_Aggregated_results.py"),
#    Page("pages/8_Disqualify_driver.py"),
#])

#hide_pages(
#    ["1_Test_db_connection_to_dreamhost.py"],
#    ["4_Race_results.py"],
#    ["5_Graph_selector.py"],
#    ["5_Test.py"],
#    ["8_Disqualify_driver.py"],
#) 


