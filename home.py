import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    admin_pages = [
        st.Page(
            "pages/2_Read_lapsnapper_pdf_file.py",
            title="Indlæs resultater fra Lapsnapper PDF fil",
            url_path="read_results",
        ),
        st.Page(
            "pages/7_Aggregated_results.py",
            title="Diskvalificering",
            url_path="Aggregated_results?mode=DSQ",
        ),
        st.Page(
            "logout.py",
            title="Log ud",
        )
    ]
else:
    admin_pages = [
        st.Page(
            "login.py",
            title="Log ind",
        )
    ]

pg = st.navigation({
    "Resultatvisning": [
    st.Page(
        "pages/7_Aggregated_results.py",
        title="Resultater",
        url_path="Aggregated_results?mode="
    ),
    st.Page(
        "pages/3_Race_graph.py",
        title="Race graf"
    ),
],
"Administration": admin_pages})
pg.run()

