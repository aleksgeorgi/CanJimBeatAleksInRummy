import matplotlib
matplotlib.use('Agg')  # Set the backend to non-interactive before importing pyplot
import matplotlib.pyplot as plt
from db_utils import get_all_data, convert_fetched_data_to_df
import os
from datetime import datetime
import json
import pandas as pd
import seaborn as sns
import numpy as np

def fetch_data():
    try:
        data = get_all_data()
        data = convert_fetched_data_to_df(data)
        return data
    except Exception as e:
        print(f"Error fetching or converting data: {str(e)}")
        return None

def get_data_hash(data):
    """Create a hash of the data to detect changes"""
    if data is None:
        return None
    return hash(data.to_json())

def should_update_plot(save_path='static/images/scores_scatter.png', hash_path='static/images/data_hash.json'):
    """Check if we need to regenerate the plot"""
    data = fetch_data()
    if data is None:
        return False
        
    current_hash = get_data_hash(data)
    
    # If image doesn't exist, we should update
    if not os.path.exists(save_path):
        return True
        
    # Check if we have a stored hash
    try:
        with open(hash_path, 'r') as f:
            stored_data = json.load(f)
            stored_hash = stored_data['hash']
            return current_hash != stored_hash
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return True

def create_scatter_plot(save_path='static/images/scores_scatter.png', hash_path='static/images/data_hash.json'):
    """Create scatter plot only if data has changed"""
    # Ensure directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    if not should_update_plot(save_path, hash_path):
        print("Data unchanged, using existing plot")
        return save_path

    sns.set_style("darkgrid")
        
    data = fetch_data()
    if data is None:
        print("Unable to create scatter plot due to data fetching error")
        return None
        
    plt.figure(figsize=(10, 6))
    # Plot Jim's scores in blue
    plt.scatter(range(1, len(data) + 1), data['jim_score'], 
            alpha=0.5, c='blue', label="Jim's scores")

    # Plot Aleks' scores in red
    plt.scatter(range(1, len(data) + 1), data['aleks_score'], 
            alpha=0.5, c='red', label="Aleks' scores")

    plt.xlabel('Game Number')
    plt.ylabel('Score')
    plt.title('Jim and Aleks Scores Over Time')
    plt.legend()
    
    # Save the plot
    plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close()
    
    # Save the data hash
    with open(hash_path, 'w') as f:
        json.dump({
            'hash': get_data_hash(data),
            'last_updated': datetime.now().isoformat()
        }, f)
    
    print("Generated new plot due to data changes")
    return save_path

def create_histogram(save_path='static/images/scores_hist.png', hash_path='static/images/data_hash.json'):
    """Create scatter plot only if data has changed"""
    # Ensure directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    if not should_update_plot(save_path, hash_path):
        print("Data unchanged, using existing plot")
        return save_path

    sns.set_style("darkgrid")
        
    data = fetch_data()
    if data is None:
        print("Unable to create scatter plot due to data fetching error")
        return None
        
    plt.figure(figsize=(10, 6))

    # Calculate optimal number of bins using Sturges' rule
    n_bins = int(1 + 3.322 * np.log10(len(data)))

    # Plot histograms with enhanced styling
    plt.hist(data['jim_score'], bins=n_bins, color='#3498db', alpha=0.6, 
            label="Jim's Scores", edgecolor='white', linewidth=1.2)
    plt.hist(data['aleks_score'], bins=n_bins, color='#e74c3c', alpha=0.6,
            label="Aleks' Scores", edgecolor='white', linewidth=1.2)

    # Enhance the plot appearance
    plt.title("Distribution of Scores", fontsize=14, pad=15)
    plt.xlabel('Score', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)

    # Add grid for better readability
    plt.grid(True, alpha=0.3, linestyle='--')

    # Customize legend
    plt.legend(frameon=True, fancybox=True, shadow=True)
    
    # Save the plot
    plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close()
    
    # Save the data hash
    with open(hash_path, 'w') as f:
        json.dump({
            'hash': get_data_hash(data),
            'last_updated': datetime.now().isoformat()
        }, f)
    
    print("Generated new plot due to data changes")
    return save_path

if __name__ == "__main__":
    create_scatter_plot()
    # create_histogram()