import os
from flask import Flask, render_template
from db_utils import get_all_data
from visualizations import create_scatter_plot

app = Flask(__name__)

@app.route('/')
def index():
    data = get_all_data()  # Fetch your data
    os.makedirs('static/images', exist_ok=True)
    
    # generate the scatter plot
    create_scatter_plot()
    
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)


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