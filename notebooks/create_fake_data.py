from faker import Faker
import pandas as pd
import random

fake = Faker()
data = []

for _ in range(50):
    data.append({
        'StudentID': fake.unique.random_number(digits=5),
        'Name': fake.first_name(),
        'Class': random.choice([6, 7, 8, 9, 10]),
        'Math_Marks': random.randint(20, 100),
        'Science_Marks': random.randint(20, 100),
        'Attendance': round(random.uniform(60, 100), 2),
        'Behavior': random.choice(['Attentive', 'Distracted', 'Quiet', 'Aggressive']),
        'Parent_Income': random.randint(10000, 50000)
    })

df = pd.DataFrame(data)
df.to_csv("Students_insight\\data\\sample_school_data.csv", index=False)