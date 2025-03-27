import requests

api_url = "http://119.235.57.160/api/json/performanceMetrics"

params = {
    "resourceid": "115.242.159.238",  # Replace with actual device ID
    "attributeid": "latency, packet_loss",
    "apikey": "b158496cf1772bfcf0c738154d38e4ec"  # Replace with your API key
}

response = requests.get(api_url, params=params, verify=False)  # Set verify=True if the server has a valid SSL cert

print("Status Code:", response.status_code)
print("Response:", response.json())
