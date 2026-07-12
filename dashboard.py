import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="SmartAttend AI",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 SmartAttend AI Dashboard")
st.write("AI Based Face Recognition Attendance System")

# ---------------------------------------------------
# File Paths
# ---------------------------------------------------

ATTENDANCE_FILE = "attendance/attendance.xlsx"
STUDENT_FILE = "database/students.csv"

# ---------------------------------------------------
# Load Attendance
# ---------------------------------------------------

if os.path.exists(ATTENDANCE_FILE):
    attendance_df = pd.read_excel(ATTENDANCE_FILE)
else:
    attendance_df = pd.DataFrame(
        columns=["Student ID", "Name", "Date", "Time"]
    )

# ---------------------------------------------------
# Load Registered Students
# ---------------------------------------------------

if os.path.exists(STUDENT_FILE):
    students_df = pd.read_csv(STUDENT_FILE)
else:
    students_df = pd.DataFrame(
        columns=["ID", "Name"]
    )

# Convert IDs to string for matching
if not attendance_df.empty:
    attendance_df["Student ID"] = attendance_df["Student ID"].astype(str)

if not students_df.empty:
    students_df["ID"] = students_df["ID"].astype(str)

# ---------------------------------------------------
# Dashboard Metrics
# ---------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "👨‍🎓 Total Registered Students",
        len(students_df)
    )

with col2:

    today = datetime.now().strftime("%Y-%m-%d")

    today_count = len(
        attendance_df[
            attendance_df["Date"] == today
        ]
    )

    st.metric(
        "📅 Today's Attendance",
        today_count
    )

with col3:

    st.metric(
        "📖 Total Attendance Records",
        len(attendance_df)
    )

# ---------------------------------------------------
# Current Students Attendance
# ---------------------------------------------------

st.subheader("✅ Current Students Attendance")

if not students_df.empty:

    current_attendance = attendance_df[
        attendance_df["Student ID"].isin(
            students_df["ID"]
        )
    ]

    if current_attendance.empty:
        st.info("No attendance available for registered students.")
    else:
        st.dataframe(
            current_attendance,
            use_container_width=True
        )

else:

    st.warning("No students are registered.")

# ---------------------------------------------------
# Search Student
# ---------------------------------------------------

st.subheader("🔍 Search Registered Student")

if not students_df.empty:

    student_id = st.selectbox(
        "Select Student ID",
        students_df["ID"]
    )

    student_name = students_df[
        students_df["ID"] == student_id
    ]["Name"].values[0]

    st.write(f"### 👤 Student Name: {student_name}")

    student_records = attendance_df[
        attendance_df["Student ID"] == student_id
    ]

    if student_records.empty:

        st.info("No attendance records found.")

    else:

        st.dataframe(
            student_records,
            use_container_width=True
        )

# ---------------------------------------------------
# Attendance History
# ---------------------------------------------------

st.subheader("📜 Complete Attendance History")

if attendance_df.empty:

    st.info("No attendance history available.")

else:

    st.dataframe(
        attendance_df,
        use_container_width=True
    )

# ---------------------------------------------------
# Download Report
# ---------------------------------------------------

st.subheader("⬇️ Download Attendance Report")

if os.path.exists(ATTENDANCE_FILE):

    with open(
        ATTENDANCE_FILE,
        "rb"
    ) as file:

        st.download_button(
            label="📥 Download Excel Report",
            data=file,
            file_name="attendance_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )