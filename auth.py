import streamlit as st
import bcrypt
import db

def signup__ui():
    st.subheader("🔐 Signup")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        users = db.collection("users")
        existing = users.where("username", "==", username).stream()

        if any(existing):
            st.error("Username already taken.")
            return
        
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        doc_ref = users.document()
        doc_ref.set({
            "username": username,
            "password_hash": hashed_pw,
            "total_xp": 0,
            "streak": 0,
            "level": 1
        })

        st.success("Account created.")

def login_ui():
    st.subheader("🔑 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users = db.collection("users").where("username", "==", username).stream()

        user_doc = None
        for doc in users:
            user_doc = doc
            break

        if not user_doc:
            st.error("Username not found.")
            return

        user_data = user_doc.to_dict()
        if bcrypt.checkpw(password.encode(), user_data["password_hash"].encode()):
            st.session_state.logged_in = True
            st.session_state.user_id = user_doc.id
            st.success("Login successful.")
        else:
            st.error("Incorrect password.")
