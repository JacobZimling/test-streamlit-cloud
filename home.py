import streamlit as st

pg = st.navigation([
    st.Page(
        "pages/7_Aggregated_results.py",
        title="Resultater",
        url_path="Aggregated_results?mode="
    ),
    st.Page(
        "pages/2_Read_lapsnapper_pdf_file.py", 
        title="Indlæs resultater fra Lapsnapper PDF fil",
        url_path="read_results",
        visibility="hidden"
    ),
    st.Page(
        "pages/3_Race_graph.py",
        title="Race graf"
    ),
    st.Page(
        "pages/7_Aggregated_results.py",
        title="Diskvalificering",
        url_path="Aggregated_results?mode=DSQ",
        visibility="hidden"
    ),
])
pg.run()

