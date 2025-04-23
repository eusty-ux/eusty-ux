import streamlit as st
from datetime import datetime
import time

# Initialize session state for tasks
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# Title
st.title("📝 To-Do List with Reminders")

# Task input form
with st.form("task_form", clear_on_submit=True):
    task_desc = st.text_input("Task Description")
    task_time = st.time_input("Time to start the task")
    submitted = st.form_submit_button("Add Task")
    if submitted and task_desc:
        st.session_state.tasks.append({
            "desc": task_desc,
            "time": task_time.strftime("%H:%M"),
            "done": False,
            "notified": False
        })

# Show tasks
st.subheader("Your Tasks")

if not st.session_state.tasks:
    st.info("No tasks added yet.")
else:
    current_time = datetime.now().strftime("%H:%M")
    for i, task in enumerate(st.session_state.tasks):
        col1, col2, col3 = st.columns([4, 2, 2])
        with col1:
            status = "✅" if task["done"] else "⏳"
            st.write(f"{status} **{task['desc']}** at {task['time']}")
        with col2:
            if not task["done"]:
                if st.button(f"Mark Done {i}"):
                    st.session_state.tasks[i]["done"] = True
                    st.balloons()
        with col3:
            # Check if it's time for reminder
            if not task["notified"] and not task["done"] and task["time"] == current_time:
                st.warning(f"⏰ It's time to start: {task['desc']}")
                st.session_state.tasks[i]["notified"] = True

# Auto-refresh every 30 seconds to keep time-checks alive
st.experimental_rerun()
