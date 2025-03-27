import requests

api_url = "https://119.235.57.160:9090/api/json/performanceMetrics"
params = {
    "resourceid": "113.193.226.242",  # Replace with actual device ID
    "attributeid": "latency, packet_loss",
    "apikey": "dabc4deafee2c6ca9bde9e825729b4e4"
}

response = requests.get(api_url, params=params)

if response.status_code == 200:
    print("Success:", response.json())
else:
    print("Error:", response.status_code, response.text)