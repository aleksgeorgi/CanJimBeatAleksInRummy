import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd

load_dotenv()
# Load environment variables
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")



def get_db_connection():
    """Create a database connection."""
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        sslmode="require"  # Enforces encrypted TLS connections
    )


def get_all_data(): 
    """Retrieve all data from the database."""
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM raw_scores;")
    data = cursor.fetchall()
    conn.close()
    return data


def convert_fetched_data_to_df(data):
    """Convert fetched database records to pandas DataFrame."""
    return pd.DataFrame(data)


if __name__ == '__main__':
    # df = pd.read_csv(r"C:\Users\aleksandra\Github\CanJimBeatAleksInRummy\data\cjbair_score_updates_endOfGame1.csv")
    # add_data(df)
    data = get_all_data()
    data = convert_fetched_data_to_df(data)
    print(data)
    # pass