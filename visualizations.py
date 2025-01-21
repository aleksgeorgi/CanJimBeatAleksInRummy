import os
import logging
import matplotlib
matplotlib.use('Agg')  # Set the backend to non-interactive before importing pyplot
import matplotlib.pyplot as plt
from db_utils import get_all_data, convert_fetched_data_to_df
from datetime import datetime
import json
import pandas as pd
import seaborn as sns
import numpy as np

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()  # Log to console
    ]
)

def fetch_data():
    try:
        logging.info("Fetching and converting data.")
        data = get_all_data()
        data = convert_fetched_data_to_df(data)
        logging.info("Data fetched and converted successfully.")
        return data
    except Exception as e:
        logging.error("Error fetching or converting data.", exc_info=True)
        return None

def get_data_hash(data):
    """Create a hash of the data to detect changes."""
    try:
        if data is None:
            return None
        return hash(data.to_json())
    except Exception as e:
        logging.error("Error creating data hash.", exc_info=True)
        return None

def should_update_plot(save_path='static/images/scores_scatter.png', hash_path='static/images/data_hash.json'):
    """Check if we need to regenerate the plot."""
    try:
        data = fetch_data()
        if data is None:
            logging.warning("No data available to check for updates.")
            return False
        
        current_hash = get_data_hash(data)
        
        # If image doesn't exist, we should update
        if not os.path.exists(save_path):
            logging.info("Plot file does not exist. Updating plot.")
            return True
        
        # Check if we have a stored hash
        try:
            with open(hash_path, 'r') as f:
                stored_data = json.load(f)
                stored_hash = stored_data['hash']
                return current_hash != stored_hash
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            logging.warning("Hash file not found or corrupted. Updating plot.")
            return True
    except Exception as e:
        logging.error("Error determining whether to update plot.", exc_info=True)
        return False

def create_scatter_plot(save_path='static/images/scores_scatter.png', hash_path='static/images/data_hash.json'):
    """Create scatter plot only if data has changed."""
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        if not should_update_plot(save_path, hash_path):
            logging.info("Data unchanged. Using existing plot.")
            return save_path

        sns.set_style("darkgrid")
        data = fetch_data()
        if data is None:
            logging.error("Unable to create scatter plot due to data fetching error.")
            return None

        plt.figure(figsize=(10, 6))
        plt.scatter(range(1, len(data) + 1), data['jim_score'], alpha=0.5, c='blue', label="Jim's scores")
        plt.scatter(range(1, len(data) + 1), data['aleks_score'], alpha=0.5, c='red', label="Aleks' scores")
        plt.xlabel('Game Number')
        plt.ylabel('Score')
        plt.title('Jim and Aleks Scores Over Time')
        plt.legend()

        # Save the plot
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
        plt.close()

        # Save the data hash
        with open(hash_path, 'w') as f:
            json.dump({'hash': get_data_hash(data), 'last_updated': datetime.now().isoformat()}, f)

        logging.info("Scatter plot created and saved successfully.")
        return save_path
    except Exception as e:
        logging.error("Error creating scatter plot.", exc_info=True)
        return None

def create_histogram(save_path='static/images/scores_hist.png', hash_path='static/images/data_hash.json'):
    """Create histogram plot only if data has changed."""
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        if not should_update_plot(save_path, hash_path):
            logging.info("Data unchanged. Using existing plot.")
            return save_path

        sns.set_style("darkgrid")
        data = fetch_data()
        if data is None:
            logging.error("Unable to create histogram due to data fetching error.")
            return None

        plt.figure(figsize=(10, 6))
        n_bins = int(1 + 3.322 * np.log10(len(data)))  # Calculate optimal bins using Sturges' rule
        plt.hist(data['jim_score'], bins=n_bins, color='#3498db', alpha=0.6, label="Jim's Scores", edgecolor='white', linewidth=1.2)
        plt.hist(data['aleks_score'], bins=n_bins, color='#e74c3c', alpha=0.6, label="Aleks' Scores", edgecolor='white', linewidth=1.2)
        plt.title("Distribution of Scores", fontsize=14, pad=15)
        plt.xlabel('Score', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.grid(True, alpha=0.3, linestyle='--')
        plt.legend(frameon=True, fancybox=True, shadow=True)

        # Save the plot
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
        plt.close()

        # Save the data hash
        with open(hash_path, 'w') as f:
            json.dump({'hash': get_data_hash(data), 'last_updated': datetime.now().isoformat()}, f)

        logging.info("Histogram created and saved successfully.")
        return save_path
    except Exception as e:
        logging.error("Error creating histogram plot.", exc_info=True)
        return None


if __name__ == "__main__":
    create_scatter_plot()
    # create_histogram()