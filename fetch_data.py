import requests

url = "https://119.235.57.160:9090/api/json/reports/getAdvancedReportData"
params = {
    "fetchFromRowNumber": 1,
    "rowsToFetch": 1000,
    "reportID": 10201,
    "apiKey": "a706e10cc5b8137749233a59f3480ef9"
}

# Disable SSL verification warnings (optional)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Make the request
response = requests.get(url, params=params, verify=False)

# Print the response
print(response.status_code)
print(response.text)

import json

data = response.text
json_data = f'''{data}'''

data = json.loads(json_data)

#rows = data.get("rows", [])

data = data.pop('rows', None)

#print(data)

with open('output_ip.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

print("Each row saved as a JSON object in 'output_ip.json' successfully!")


'''

for entry in rows:
    ip = entry.get("IP Address")
    availability = entry.get("Availability (%)")
    packet_loss = entry.get("Packet Loss - Percentage")
    response_time = entry.get("Response Time - MilliSeconds")
    device_name = entry.get("Device Name")

    print(
        f"IP: {ip}, Availability: {availability}%, Packet Loss: {packet_loss}%, Response Time: {response_time} ms, Device: {device_name}")


'''