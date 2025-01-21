import os
import logging
from flask import Flask, render_template
from db_utils import get_all_data
from visualizations import create_scatter_plot

# Initialize Flask app
app = Flask(__name__)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()  # Log to console
    ]
)

@app.route('/')
def index():
    try:
        logging.info("Fetching data from the database.")
        data = get_all_data()  # Fetch your data

        logging.info("Ensuring static/images directory exists.")
        os.makedirs('static/images', exist_ok=True)

        logging.info("Creating scatter plot.")
        create_scatter_plot()

        logging.info("Rendering index.html with data.")
        return render_template('index.html', data=data)
    
    except Exception as e:
        logging.error("An error occurred in the index route.", exc_info=True)
        return "An error occurred while processing your request. Please try again later.", 500


if __name__ == '__main__':
    try:
        logging.info("Starting the Flask application.")
        app.run(debug=True)
    except Exception as e:
        logging.critical("Failed to start the Flask application.", exc_info=True)



'''
Testing the get request:

    curl http://127.0.0.1:5000/data


Testing POST requests can also be requested programmatically using Python's requests library:

    import requests

    data = [
        {"jim_score": 10, "aleks_score": 15},
        {"jim_score": 20, "aleks_score": 25}
    ]

    response = requests.post("http://127.0.0.1:5000/data", json=data)

    print(response.status_code)  # Should print 201
    print(response.json())       # Should print {"message": "Data added successfully!"}
    
Example of Payload:
[
    {"jim_score": 10, "aleks_score": 15},
    {"jim_score": 20, "aleks_score": 25}
]

'''