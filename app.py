import os
import logging
import base64
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

# Decode and save SSL certificates
CERT_PATH = "certs/"
os.makedirs(CERT_PATH, exist_ok=True)

# Verify that certificates were saved correctly
try:
    logging.info(f"Decoded certificates: {os.listdir(CERT_PATH)}")
except Exception as e:
    logging.error("Error listing decoded certificates.", exc_info=True)

    with open(os.path.join(CERT_PATH, "server-ca.pem"), "wb") as f:
        f.write(base64.b64decode(os.getenv("SERVER_CA")))
    logging.info(f"SERVER_CA length: {len(os.getenv('SERVER_CA'))}")
    logging.info(f"SERVER_CA: {os.getenv('SERVER_CA')}")

    with open(os.path.join(CERT_PATH, "client-cert.pem"), "wb") as f:
        f.write(base64.b64decode(os.getenv("CLIENT_CERT")))

    with open(os.path.join(CERT_PATH, "client-key.pem"), "wb") as f:
        f.write(base64.b64decode(os.getenv("CLIENT_KEY")))
        
    logging.info(f"SERVER_CA length: {len(os.getenv('SERVER_CA'))}")
    logging.info(f"SERVER_CA: {os.getenv('SERVER_CA')}")


    logging.info("SSL certificates decoded and saved successfully.")
    
except Exception as e:
    logging.critical("Failed to decode and save SSL certificates.", exc_info=True)
    raise e

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