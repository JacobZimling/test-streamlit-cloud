import streamlit as st

def cascading_selectbox(key_prefix, primary_options, get_sub_options):
    """
    Reusable function for cascading selectboxes.
    key_prefix: Unique string for this page (e.g., 'page1', 'page2').
    primary_options: List of primary options (e.g., ['Cars', 'Food']).
    get_sub_options: Function that returns sub-options based on primary selection.
    """
    # Initialize session state if not present
    if f'{key_prefix}_primary' not in st.session_state:
        st.session_state[f'{key_prefix}_primary'] = None
    if f'{key_prefix}_secondary' not in st.session_state:
        st.session_state[f'{key_prefix}_secondary'] = None

    # Primary Selectbox
    def save_primary():
        st.session_state[f'{key_prefix}_primary'] = st.session_state[f'{key_prefix}_primary_key']
    
    primary_val = st.selectbox(
        "Select Category",
        primary_options,
        key=f'{key_prefix}_primary_key',
        on_change=save_primary
    )
    
    # Update secondary options based on primary selection
    sub_options = get_sub_options(primary_val) if primary_val else []
    
    # Ensure secondary state matches current options
    if primary_val and st.session_state[f'{key_prefix}_secondary'] not in sub_options:
        st.session_state[f'{key_prefix}_secondary'] = None

    # Secondary Selectbox
    def save_secondary():
        st.session_state[f'{key_prefix}_secondary'] = st.session_state[f'{key_prefix}_secondary_key']

    secondary_val = st.selectbox(
        "Select Item",
        sub_options,
        key=f'{key_prefix}_secondary_key',
        on_change=save_secondary
    )

    return primary_val, secondary_val

# Example Usage in a Page
def get_sub_options(primary):
    if primary == 'Cars':
        return ['Honda', 'Tesla']
    elif primary == 'Food':
        return ['Rice', 'Meat']
    return []

# Page 1 Logic
primary_1, secondary_1 = cascading_selectbox("page1", ["Cars", "Food"], get_sub_options)
st.write(f"Page 1 Selection: {primary_1}, {secondary_1}")

# Page 2 Logic (Same function, different key)
primary_2, secondary_2 = cascading_selectbox("page2", ["Cars", "Food"], get_sub_options)
st.write(f"Page 2 Selection: {primary_2}, {secondary_2}")   
