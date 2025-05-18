import pandas as pd
from app.db.database import get_connection

def load_students():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM students", conn)
    conn.close()
    return df

# def load_and_clean_csv(filepath):
#     df = pd.read_csv(filepath)
#     df.columns = df.columns.str.strip().str.lower()
#     df.dropna(inplace=True)
#     df['studentid'] = df['studentid'].astype(str)
#     df = df.rename(columns={'studentid':'Student ID','name':'Student Name',
#                             'class':'Class','math_marks':'Math','attendance':'Attendance(%)',
#                             'science_marks':'Science','behavior':'Behavior','parent_income':'Parents Income'})
    
#     return df