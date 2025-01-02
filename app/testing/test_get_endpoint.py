import requests

BASE_URL = 'http://127.0.0.1:5000'

def test_get_data():
    response = requests.get(f"{BASE_URL}/data")
    if response.status_code == 200:
        print("GET /data succeeded:", response.json())
    else:
        print("GET /data failed:", response.status_code, response.text)

if __name__ == "__main__":
    test_get_data()
