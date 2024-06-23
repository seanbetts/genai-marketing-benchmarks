import sqlite3
import pandas as pd

# Load data from Excel file
file_path = '../../Test_Questions.xlsx'
df = pd.read_excel(file_path)

# Sanitize column names
df.columns = [col.replace(' ', '_').replace('-', '_') for col in df.columns]

# Convert all data to string format to ensure compatibility with SQLite
df = df.astype(str)

# Connect to SQLite database
conn = sqlite3.connect('../../results_database.sqlite')
cursor = conn.cursor()

# Define table name
table_name = 'questions'

# Drop table if it exists
cursor.execute(f'DROP TABLE IF EXISTS {table_name}')

# Create table
cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        {', '.join([f'{col} TEXT' for col in df.columns])}
    )
''')

# Insert data into table
for index, row in df.iterrows():
    cursor.execute(f'''
    INSERT INTO {table_name} ({', '.join(df.columns)})
    VALUES ({', '.join(['?' for _ in df.columns])})
    ''', tuple(row))

# Commit and close connection
conn.commit()
conn.close()

print("Excel sheet added to Questions table")
