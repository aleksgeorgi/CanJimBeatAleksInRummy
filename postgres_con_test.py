import psycopg2
import csv
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Database connection details from environment variables
host = os.getenv('DB_HOST')
database = os.getenv('DB_NAME')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')

# Connect to the database
try:
    conn = psycopg2.connect(host=host, database=database, user=user, password=password)
    cursor = conn.cursor()

    # Create the `raw_scores` table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS raw_scores (
        id SERIAL PRIMARY KEY,
        game_number INT NOT NULL,
        jim_score INT NOT NULL,
        aleks_score INT NOT NULL,
        jim_running_sum INT,  -- This will be dynamically updated
        aleks_running_sum INT -- This will be dynamically updated
    )
    """)

    # Create the trigger function to update running totals
    cursor.execute("""
    CREATE OR REPLACE FUNCTION update_running_totals() RETURNS TRIGGER AS $$
    BEGIN
        UPDATE raw_scores
        SET
            jim_running_sum = (SELECT SUM(jim_score) FROM raw_scores WHERE game_number <= NEW.game_number),
            aleks_running_sum = (SELECT SUM(aleks_score) FROM raw_scores WHERE game_number <= NEW.game_number)
        WHERE id = NEW.id;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)

    # Create the trigger
    cursor.execute("""
    CREATE OR REPLACE TRIGGER calculate_running_totals
    AFTER INSERT ON raw_scores
    FOR EACH ROW
    EXECUTE FUNCTION update_running_totals();
    """)

    # Insert CSV data into the `raw_scores` table
    with open('raw_data.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for game_number, jim_score, aleks_score in reader:
            cursor.execute("""
            INSERT INTO raw_scores (game_number, jim_score, aleks_score)
            VALUES (%s, %s, %s)
            """, (int(game_number), int(jim_score), int(aleks_score)))

    # Commit changes
    conn.commit()
    print("Data inserted successfully and running totals updated dynamically!")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'conn' in locals() and conn:
        conn.close()
