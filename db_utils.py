import os
import time
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

load_dotenv()
DB_HOST = os.getenv("DB_HOST", "35.224.65.167")  # Replace with your actual host
DB_NAME = os.getenv("DB_NAME", "postgres")  # Replace with your actual database name
DB_USER = os.getenv("DB_USER", "postgres")  # Replace with your username
DB_PASSWORD = os.getenv("DB_PASSWORD")  # Replace with your actual password
CERT_PATH = "certs/"  # Directory where your certificates are stored

def get_db_connection():
    """Create a secure database connection using SSL."""
    try:
        logging.info("Establishing secure database connection...")
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=5432,  # Default PostgreSQL port
            sslmode="verify-ca",
            sslrootcert=os.path.join(CERT_PATH, "server-ca.pem"),
            sslcert=os.path.join(CERT_PATH, "client-cert.pem"),
            sslkey=os.path.join(CERT_PATH, "client-key.pem")
        )
        logging.info("Database connection established successfully.")
        return connection
    except Exception as e:
        logging.error("Error establishing database connection.", exc_info=True)
        raise e
    
def get_all_data():
    """Retrieve all data from the database."""
    try:
        logging.info("Fetching all data from the database.")
        start_time = time.time()
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM raw_scores;")
        data = cursor.fetchall()
        logging.info("Data fetched successfully.")
        conn.close()
        end_time = time.time()
        logging.info(f"Data fetched successfully in {end_time - start_time:.2f} seconds.")
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
    try:
        logging.info("Converting data to pandas DataFrame.")
        df = pd.DataFrame(data)
        logging.info(f"DataFrame created with shape: {df.shape}")
        return df
    except Exception as e:
        logging.error("Error while converting data to DataFrame.", exc_info=True)
        raise e



if __name__ == '__main__':
    # df = pd.read_csv(r"C:\Users\aleksandra\Github\CanJimBeatAleksInRummy\data\cjbair_score_updates_endOfGame1.csv")
    # add_data(df)
    data = get_all_data()
    data = convert_fetched_data_to_df(data)
    print(data)
    # pass