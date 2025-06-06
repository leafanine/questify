import streamlit as st
from auth import login_ui, signup_ui
from goal_logic import dashboard_ui

if 'logged_in' not in st.session_state:
    st.session_state.logged_in= False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

st.sidebar.title(" - Questify - ")
menu = st.sidebar.radio("Navigate", ["Login", "Signup", "Dashboard"])

if menu == "Login":
    login_ui()
elif menu == "Signup":
    signup_ui()
elif menu == "Dashboard":
    if st.session_state.logged_in():
        dashboard_ui()
    else:
        st.warning("Please log in to Questify first!")