# TODO: add logging 


import csv
import os
import psycopg2
import pandas as pd
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv


load_dotenv()
# Load environment variables
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def get_db_connection():
    """Establish and return a database connection."""
    return psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def setup_datbase():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        _create_raw_scores_table()
        _create_running_totals_trigger_function()
        _create_running_totals_trigger()
        _insert_data_into_raw_scores_table()
        
        # Commit changes
        conn.commit()
        print("Data inserted successfully and running totals updated dynamically!")
    except Exception as e:
        print(f"An error occured: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()
    
    def _create_raw_scores_table():
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

    def _create_running_totals_trigger_function():
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
    
    def _create_running_totals_trigger():
        # Create the trigger
        cursor.execute("""
        CREATE OR REPLACE TRIGGER calculate_running_totals
        AFTER INSERT ON raw_scores
        FOR EACH ROW
        EXECUTE FUNCTION update_running_totals();
        """)

    def _insert_data_into_raw_scores_table():
        # Insert original CSV data into the `raw_scores` table
        with open('raw_data.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for game_number, jim_score, aleks_score in reader:
                cursor.execute("""
                INSERT INTO raw_scores (game_number, jim_score, aleks_score)
                VALUES (%s, %s, %s)
                """, (int(game_number), int(jim_score), int(aleks_score)))

def get_all_data(): #TODO REFACTOR USING SQLALCHEMY
    """Retrieve all data from the database."""
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM raw_scores;")
    data = cursor.fetchall()
    conn.close()
    return data

def add_data(df): #TODO REFACTOR USING SQLALCHEMY
    """
    Add new rows to the raw_scores table from a DataFrame.

    Args:
        df (pd.DataFrame): DataFrame with two columns: 'jim_score' and 'aleks_score'.
    """
    # Ensure the DataFrame has the required columns
    if not {'jim_score', 'aleks_score'}.issubset(df.columns):
        raise ValueError("DataFrame must contain 'jim_score' and 'aleks_score' columns.")

    # Convert DataFrame to a list of tuples with Python native types
    rows_to_insert = df[['jim_score', 'aleks_score']].astype(int).values.tolist()

    # Connect to the database
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # Use executemany to insert all rows at once
        cursor.executemany(
            """
            INSERT INTO raw_scores (jim_score, aleks_score)
            VALUES (%s, %s)
            """,
            rows_to_insert
        )
        
        # Commit the transaction
        conn.commit()
        print("Data inserted successfully!")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()  # Rollback transaction in case of an error
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def convert_fetched_data_to_df(data):
    return pd.DataFrame.from_records(data, columns=data[0].keys())

if __name__ == '__main__':
    # df = pd.read_csv(r"C:\Users\aleksandra\Github\CanJimBeatAleksInRummy\data\cjbair_score_updates_endOfGame1.csv")
    # add_data(df)
    data = get_all_data()
    data = convert_fetched_data_to_df(data)
    print(data)