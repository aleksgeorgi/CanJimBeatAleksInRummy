import psycopg2
import csv

# Database connection details
host = 'your-instance-public-ip'
database = 'portfolio_data'
user = 'postgres'
password = 'your-password'

# Connect to the database
conn = psycopg2.connect(host=host, database=database, user=user, password=password)
cursor = conn.cursor()

# Create a table
cursor.execute("""
CREATE TABLE IF NOT EXISTS performance_data (
    id SERIAL PRIMARY KEY,
    player_name VARCHAR(50),
    score INTEGER,
    outcome VARCHAR(50)
)
""")

# Insert CSV data into the table
with open('data.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header row
    for row in reader:
        cursor.execute("""
        INSERT INTO performance_data (player_name, score, outcome)
        VALUES (%s, %s, %s)
        """, row)

conn.commit()
cursor.close()
conn.close()
