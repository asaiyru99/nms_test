import os
import pandas as pd
import streamlit as st
import requests
import urllib3

import json
import re

from filtering import get_filters
from filtering_ip import get_filters_ip
from agents_final import Call
from dotenv import load_dotenv

#from langchain_pinecone import PineconeVectorStore
#from langchain_google_genai import GoogleGenerativeAIEmbeddings
import chromadb

# Force ChromaDB to use DuckDB instead of SQLite
chroma_client = chromadb.PersistentClient(path=":memory:", database="duckdb")

#load_dotenv()

# Only for prototype, The vector Store is refreshed .
# If there are any indexing errors run after uncommenting both of these cells.
# vectorize('data.csv',True)
# vectorize('data.csv',False)

#df = pd.read_csv('data.csv')

from pyngrok import ngrok
import streamlit as st

# Start ngrok tunnel
public_url = ngrok.connect(8501).public_url
print(f"Public URL: {public_url}")

# Your Streamlit app
st.write(f"Access this app at: {public_url}")


def extract_ip(question):
    match = re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', question)
    return match.group(0) if match else None

st.markdown("<h1 style='text-align: center; color: blue;'>NMS Helper Bot</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.image('LOGO.png')


def run(query: str):

    url = "https://119.235.57.160:9090/api/json/reports/getAdvancedReportData"
    params = {
        "fetchFromRowNumber": 1,
        "rowsToFetch": 1000,
        "reportID": 10201,
        "apiKey": "a706e10cc5b8137749233a59f3480ef9"
    }
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    response = requests.get(url, params=params, verify=False)

    print(response.status_code)
    print(response.text)

    data = response.text
    json_data = f'''{data}'''

    data = json.loads(json_data)

    rows = data.get("rows", [])

    data = data.pop('rows', None)

    with open('output_ip.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    ip_extracted = extract_ip(query)



    #rows = data.get("rows", [])

    rows = str(rows)

    solver_data = get_filters(query)

    category = [data.get("Category", "N/A") for data in solver_data]

    answer, check, priority = Call(query, rows, solver_data, category).run()

    if check and ip_extracted is None and priority == "okay":
        output = answer

        return output

    if check and ip_extracted and priority == "okay":
        output = answer

        correct_ip = get_filters_ip(ip_extracted)

        df_ip = pd.DataFrame(correct_ip)

        df_ip = df_ip.drop(columns=["moid", "Group Name", "name", "moName"])

        df_str = df_ip.to_markdown(index=False)

        # print(output)

        return "\n" + df_str

    if not check and ip_extracted and priority == "okay":
        output = answer

        correct_ip = get_filters_ip(ip_extracted)


        df_ip = pd.DataFrame(correct_ip)

        df_ip = df_ip.drop(columns=["moid", "Group Name", "name", "moName"])

        df_str = df_ip.to_markdown(index=False)

        # print(output)

        return "\n" + df_str




    if not check and ip_extracted and priority == "yes":
        correct_ip = get_filters_ip(ip_extracted)

        df_ip = pd.DataFrame(correct_ip)

        df_ip = df_ip.drop(columns=["moid", "Group Name", "name", "moName"])


        df_str = df_ip.to_markdown(index=False)

    #print(output)

        return  "This a not a new type of issue, so this is how I can help you: \n\n"  + df_str + answer

    if not check and ip_extracted and priority == "no":
        correct_ip = get_filters_ip(ip_extracted)

        df_ip = pd.DataFrame(correct_ip)

        df_ip = df_ip.drop(columns=["moid", "Group Name", "name", "moName"])

        df_str = df_ip.to_markdown(index=False)

        # print(output)

        return  df_str + "\n\n" + answer







# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What are the symptoms that you are facing ?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            # generate response

            res = run(prompt)

        st.success("Done!")

        response = st.markdown(res)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": str(res)})
