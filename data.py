import pandas as pd
import json

# Load the Excel file
df = pd.read_excel("ITSM.xlsx", engine="openpyxl")

# Convert each row to a JSON object
json_data = []

for _, row in df.iterrows():
    row_dict = row.to_dict()
    json_data.append(row_dict)

print(json_data)

with open('output.json', 'w') as json_file:
    json.dump(json_data, json_file, indent=4)

print("Each row saved as a JSON object in 'output.json' successfully!")
