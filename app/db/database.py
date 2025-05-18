import sqlite3
import pandas as pd

def get_connection():
    return sqlite3.connect("D:/Akanksha/Python/Students_insight/data/school.db", check_same_thread=False)

def validate_login(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    return None

# def create_students_table():
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS students (
#             student_id TEXT PRIMARY KEY,
#             name TEXT,
#             class INTEGER,
#             math_marks INTEGER,
#             science_marks INTEGER,
#             attendance REAL,
#             behavior TEXT,
#             parent_income INTEGER
#         )
#     """)
#     conn.commit()
#     conn.close()

# def insert_csv_to_db(csv_path="data/sample_school_data.csv"):
#     df = pd.read_csv(csv_path, dtype={"StudentID": str})
#     df.columns = [c.lower() for c in df.columns]  # normalize column names

#     conn = get_connection()
#     df.to_sql("students", conn, if_exists="replace", index=False)
#     conn.close()
