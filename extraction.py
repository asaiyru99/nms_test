import pandas as pd

print("Data Report")

print("\n======================================================")

# Load the CSV file
df = pd.read_csv('DA.csv')


for j in range(len(df[df.columns[0]])):

    print("\n")
    for i in range(len(df.columns)):
        print(f"{df.columns[i]} : {df[df.columns[i]][j]}")







