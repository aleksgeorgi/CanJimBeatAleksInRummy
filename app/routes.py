# TODO: add logging 

from flask import Blueprint, jsonify, request, render_template
from .db_utils import get_all_data, add_data
from .prediction.prediction_logic import make_prediction
import pandas as pd

# Create a Blueprint
routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    """Route to serve the home page."""
    return render_template('index.html')

@routes.route('/data', methods=['GET'])
def get_data():
    """Endpoint to retrieve all data from the raw_scores table."""
    try:
        data = get_all_data()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@routes.route('/data', methods=['POST'])
def add_new_data():
    """Endpoint to add new data to the raw_scores table."""
    try:
        # Parse the JSON request body
        request_data = request.get_json()
        if not request_data or not isinstance(request_data, list):
            return jsonify({"error": "Request body must be a JSON array of objects."}), 400

        # Convert the JSON data into a DataFrame
        df = pd.DataFrame(request_data)

        # Validate and insert data
        add_data(df)
        return jsonify({"message": "Data added successfully!"}), 201

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@routes.route('/predict', methods=['POST'])
def predict():
    """ TODO this is a temp endpoint to make predictions."""
    try:
        data = request.json
        prediction = make_prediction(data)
        return jsonify({"prediction": prediction}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



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