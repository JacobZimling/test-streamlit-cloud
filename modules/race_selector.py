import streamlit as st

def year_selector(values):
  race_year = st.segmented_control(
      'År',
      values.unique()
      ,label_visibility = 'collapsed'
  )
  return race_year
