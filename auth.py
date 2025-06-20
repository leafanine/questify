import streamlit as st
import bcrypt
from firebase_config import db
from datetime import datetime, timedelta

def signup_ui():
    st.subheader("🔐 Signup")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        if not username or not password:
            st.error("Username and Password can not be empty!")
            return
        if len(password) < 6:
            st.error("Password must be at least 6 characters long.")
            return

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
        if not username or not password:
            st.error("Username and Password can not be empty!")
            return 
        
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

            user_ref = db.collection("users").document(user_doc.id)

            today = datetime.now().date()

            last_login_str = user_data.get("last_login")
            if last_login_str:
                last_login = datetime.strptime(last_login_str, "%Y-%m-%d").date()
                diff = (today - last_login).days

                if diff == 1:
                    new_streak = user_data.get("streak", 0) + 1

                elif diff == 0:
                    new_streak=user_data.get("streak", 0)

                else:
                    new_streak=1
            
            else:
                new_streak=1

            user_ref.update({
                "streak": new_streak,
                "last_login": today.strftime("%Y-%m-%d")
            })
        
        else:
            st.error("Incorrect password.")
