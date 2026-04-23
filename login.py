import streamlit as st
import bcrypt
#import os

def check_login(username, password):
    if username in st.secrets:
        # Eksempel: Tjek mod et hashet password
        #hashed_password = b"$2b$12$..."  # Hent fra database/secrets
        #hashed_password = bcrypt.hashpw(st.secrets[username].password.encode(), bcrypt.gensalt())
        hashed_password = bcrypt.hashpw(st.secrets[username].password.encode(), bcrypt.gensalt())
        #hashed_password = st.secrets[username]['password'].encode()
        st.write(f'hashed_password: {hashed_password}')
        return bcrypt.checkpw(password.encode(), hashed_password)
    else:
        #st.error("Ukendt bruger")
        return False

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

#if "peter" in st.secrets:
    #st.write(st.secrets.peter.access_level)
#if "jacob" in st.secrets:
    #st.write(f'access_level: {st.secrets.jacob.access_level}')
    #st.write(f'access_level: {st.secrets['jacob']['access_level']}')
    #st.write(f'password: {st.secrets.jacob.password}')
    #st.write(f'password: {st.secrets['jacob']['password']}')
    #st.write(f'salt: {os.environ['salt']}')
    #st.write(f'salt: {st.secrets.salt}')

if not st.session_state.logged_in:
    with st.form("login_form"):
        user = st.text_input("Brugernavn")
        pwd = st.text_input("Adgangskode", type="password")
        submit = st.form_submit_button("Log ind")

    if submit:
        if check_login(user, pwd):
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Ugyldige oplysninger")
else:
    st.write("Du er nu logget ind!")
