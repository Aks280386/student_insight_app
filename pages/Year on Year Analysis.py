import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_1samp
from app.db.database import get_connection

st.subheader("📈 Year-on-Year Analysis")

# Load student data from database
@st.cache_data

def load_data():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM students", conn)
    conn.close()
    df['class'] = df['class'].astype(int)  # Ensure 'class' is treated as a number
    return df

df = load_data()

# Combine student ID and name for dropdown labels
df['label'] = df['studentid'].astype(str) + " - " + df['name']

# Dropdown for student selection
col1, col2 = st.columns(2)

with col1:
    selected_student = st.selectbox("Select Student:", sorted(df['label'].unique()), index=None, placeholder="Student ID or Name")

if selected_student:
    # Filter data for the selected student
    student_id = selected_student.split(" - ")[0]
    student_df = df[df['studentid'] == student_id].sort_values('academic_year')

    # Dropdown for subject selection
    subject_options = ['Overall', 'math_marks', 'science_marks']  # Extend if more subjects exist
    subject_display = {'math_marks': 'Math', 'science_marks': 'Science'}
    with col2:
        selected_subject = st.selectbox("Select Subject:", subject_options, index=0)

    def plot_overall(student_df, df):
        st.text("📊 Overall Performance")

        subjects = ['math_marks', 'science_marks']  # Add more subjects here if needed
        df['total_marks'] = df[subjects].sum(axis=1)
        student_df['total_marks'] = student_df[subjects].sum(axis=1)

        # Class-level statistics
        class_stats = df.groupby(['academic_year', 'class'])['total_marks'].agg(class_avg='mean', class_max='max').reset_index()

        merged = pd.merge(student_df[['academic_year', 'class', 'total_marks']], class_stats, on=['academic_year', 'class'], how='left')

        # Plotting
        plt.figure(figsize=(10, 4))
        sns.lineplot(data=merged, x='academic_year', y='total_marks', label='Student Total', marker='o', color='royalblue')
        sns.lineplot(data=merged, x='academic_year', y='class_avg', label='Class Avg Total', linestyle='--', marker='s', color='orange')
        sns.lineplot(data=merged, x='academic_year', y='class_max', label='Class Highest Total', linestyle=':', marker='^', color='green')

        plt.xlabel("Academic Year")
        plt.ylabel("Total Marks")
        plt.title("Total Marks vs Class Performance")
        plt.xticks(rotation=45)
        plt.legend()
        st.pyplot(plt.gcf())
        plt.clf()

        # Hypothesis Testing
        student_mean = student_df['total_marks'].mean()
        class_mean = class_stats['class_avg'].mean()
        t_stat, p_val = ttest_1samp(class_stats['class_avg'], student_mean)

        with st.expander("📊 Statistical Insights"):
            st.markdown(f"**Student Average Marks**: {student_mean:.2f}")
            st.markdown(f"**Class Average Marks**: {class_mean:.2f}")
            if p_val < 0.05:
                if student_mean > class_mean:
                    st.success("✅ Student's performance is significantly above class average.")
                else:
                    st.warning("🔎 Student's performance is significantly below class average.")
            else:
                st.info("✅ Student's performance is similar to class average.")

    def plot_subject(student_df, df, subject):
        st.text(f"📚{subject_display.get(subject, subject.title())} performance")

        class_stats = df.groupby(['academic_year', 'class'])[subject].agg(class_avg='mean', class_max='max').reset_index()

        merged = pd.merge(student_df[['academic_year', 'class', subject]], class_stats, on=['academic_year', 'class'], how='left')

        # Plotting
        plt.figure(figsize=(10, 4))
        sns.lineplot(data=merged, x='academic_year', y=subject, label='Student', marker='o', color='royalblue')
        sns.lineplot(data=merged, x='academic_year', y='class_avg', label='Class Avg', linestyle='--', marker='s', color='orange')
        sns.lineplot(data=merged, x='academic_year', y='class_max', label='Class Highest', linestyle=':', marker='^', color='green')

        plt.xlabel("Academic Year")
        plt.ylabel("Marks")
        plt.title(f"{subject_display.get(subject, subject.title())} Marks vs Class")
        plt.xticks(rotation=45)
        plt.legend()
        st.pyplot(plt.gcf())
        plt.clf()

        # Hypothesis Testing
        student_mean = student_df[subject].mean()
        class_mean = class_stats['class_avg'].mean()
        t_stat, p_val = ttest_1samp(class_stats['class_avg'], student_mean)

        with st.expander("📊 Statistical Insights"):
            st.markdown(f"**Student Average in {subject_display.get(subject, subject.title())}**: {student_mean:.2f}")
            st.markdown(f"**Class Average in {subject_display.get(subject, subject.title())}**: {class_mean:.2f}")
            if p_val < 0.05:
                if student_mean > class_mean:
                    st.success("✅ Student's performance is significantly above class average.")
                else:
                    st.warning("🔎 Student's performance is significantly below class average.")
            else:
                st.info("✅ Student's performance is similar to class average.")

    # Show appropriate graph
    if selected_subject == 'Overall':
        plot_overall(student_df, df)
    else:
        plot_subject(student_df, df, selected_subject)
