import streamlit as st
from firebase_config import db
from datetime import datetime

# Add a new goal
def add_goal(user_id, title, description):
    goal = {
        "user_id": user_id,
        "title": title,
        "description": description,
        "completed": False,
        "timestamp": datetime.now()
    }
    db.collection("goals").add(goal)

# Retrieve all goals for the user
def get_goals(user_id):
    goals_ref = db.collection("goals").where("user_id", "==", user_id).order_by("timestamp", direction="DESCENDING")
    return list(goals_ref.stream())

# Toggle completion status
def toggle_goal_status(goal_id, current_status):
    db.collection("goals").document(goal_id).update({"completed": not current_status})

# Delete a goal
def delete_goal(goal_id):
    db.collection("goals").document(goal_id).delete()

# UI dashboard
def dashboard_ui(user_id):
    st.subheader("🎯 Your Goals")

    # --- Add new goal form ---
    with st.form("add_goal_form"):
        title = st.text_input("Goal Title")
        description = st.text_area("Goal Description")
        submitted = st.form_submit_button("Add Goal")
        if submitted and title.strip():
            add_goal(user_id, title.strip(), description.strip())
            st.success("✅ Goal added.")
            st.rerun()

    # --- Display existing goals ---
    goals = get_goals(user_id)
    if not goals:
        st.info("You haven't added any goals yet.")
        return

    for doc in goals:
        goal = doc.to_dict()
        goal_id = doc.id

        with st.container():
            cols = st.columns([0.05, 0.7, 0.1, 0.1, 0.05])
            # Checkbox for completed
            checked = cols[0].checkbox("", value=goal["completed"], key=goal_id)
            if checked != goal["completed"]:
                toggle_goal_status(goal_id, goal["completed"])
                st.rerun()

            # Title + description
            with cols[1]:
                st.markdown(f"**{goal['title']}**")
                st.caption(goal["description"])

            # Status label
            cols[2].markdown("✅" if goal["completed"] else "⏳")

            # Delete button
            if cols[3].button("🗑️", key=f"del_{goal_id}"):
                delete_goal(goal_id)
                st.rerun()
