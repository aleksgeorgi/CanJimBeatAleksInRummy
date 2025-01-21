import os
import logging
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()  # Log to console
    ]
)

# Load environment variables
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def get_db_connection():
    """Create a database connection."""
    try:
        logging.info("Creating a database connection.")
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            sslmode="require"  # Enforces encrypted TLS connections
        )
        logging.info("Database connection established successfully.")
        return connection
    except psycopg2.Error as e:
        logging.error("Error while connecting to the database.", exc_info=True)
        raise e  # Re-raise the exception after logging it

def get_all_data():
    """Retrieve all data from the database."""
    try:
        logging.info("Fetching all data from the database.")
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM raw_scores;")
        data = cursor.fetchall()
        logging.info("Data fetched successfully.")
        conn.close()
        return data
    except psycopg2.Error as e:
        logging.error("Error while retrieving data from the database.", exc_info=True)
        raise e  # Re-raise the exception after logging it
    except Exception as e:
        logging.error("Unexpected error occurred while fetching data.", exc_info=True)
        raise e  # Re-raise the exception after logging it
    finally:
        if 'conn' in locals() and conn:
            conn.close()
            logging.info("Database connection closed.")

def convert_fetched_data_to_df(data):
    """Convert fetched database records to pandas DataFrame."""
    try:
        logging.info("Converting fetched data to pandas DataFrame.")
        df = pd.DataFrame(data)
        logging.info("Data converted to DataFrame successfully.")
        return df
    except Exception as e:
        logging.error("Error while converting data to DataFrame.", exc_info=True)
        raise e  # Re-raise the exception after logging it


if __name__ == '__main__':
    # df = pd.read_csv(r"C:\Users\aleksandra\Github\CanJimBeatAleksInRummy\data\cjbair_score_updates_endOfGame1.csv")
    # add_data(df)
    data = get_all_data()
    data = convert_fetched_data_to_df(data)
    print(data)
    # pass