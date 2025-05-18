import streamlit as st
import pandas as pd
from app.services.root_analysis import analyze_student
from app.services.recommendations import recommend_actions
from app.services.session_manager import init_session
from app.services.data_cleaning import load_students

init_session()

if not st.session_state.get("logged_in"):
    st.warning("Please log in first.")
    st.stop()


st.title("📊 Student Performance Dashboard")


 # Load data
df = load_students()
# df = load_and_clean_csv("data//sample_school_data.csv")

if st.session_state["role"] == "principal":
    # Show raw data
    if st.checkbox("Show Raw Data"):
        st.dataframe(df)

    # Step 1: Create a label column for dropdown
    df['label'] = df['studentid'].astype(str) + " - " + df['name']

    # Step 2: Create a mapping from label → Student ID
    label_to_id = dict(zip(df['label'], df['studentid'].astype(str)))

    # Step 3: Dropdown with student names + IDs
    selected_label = st.selectbox("Select Student: ", df['label'],index=None,placeholder="Student ID or Name")

    if selected_label is not None:
        # Step 4: Get student record using mapped ID
        selected_id = label_to_id[selected_label]

        # Analyze selected student
        student = df[df['studentid'] == selected_id].iloc[0]
        causes = analyze_student(student)
        actions = recommend_actions(causes)

        if len(causes)!=0:
            st.subheader(f"Root Cause Analysis for {student['name']}")
            st.write(", ".join(causes))
        else:
            st.write("Doing Excellent, keep it up!")
        if len(actions)!=0:
            st.subheader("Recommended Actions")
            st.write(", ".join(actions))

# Show data for student
elif st.session_state["role"] == "student":
    student = df[df['studentid'] == st.session_state['username']].iloc[0]
    causes = analyze_student(student)
    actions = recommend_actions(causes)
    st.subheader("Your Performance Analysis")
    st.write(f"Hello, {student['name']}")
    st.write("Issues Identified:", causes)
    st.write("Recommended Actions:", actions)