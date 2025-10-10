import streamlit as st

# Example data structure
hierarchical_data = {
    "Asia": {
        "China": ["Beijing", "Shanghai"],
        "Japan": ["Tokyo", "Osaka"]
    },
    "Europe": {
        "United Kingdom": ["London", "Manchester"],
        "France": ["Paris", "Lyon"]
    }
}

# First select box for region
region = st.selectbox("Select Region", options=list(hierarchical_data.keys()))

# Second select box for country, options depend on the selected region
if region:
    country = st.selectbox("Select Country", options=list(hierarchical_data[region].keys()))

# Third select box for city, options depend on the selected country
if country:
    city = st.selectbox("Select City", options=hierarchical_data[region][country])   
