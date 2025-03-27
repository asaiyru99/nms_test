import json
import pandas as pd
import numpy as np

model = GoogleGenerativeAIEmbeddings(model="models/embedding-001",
                                     google_api_key="AIzaSyDHSRbIV78C0d9dYsoOS0vKC9vod4ql_Vs")
from sklearn.metrics.pairwise import cosine_similarity

import streamlit as st


def get_filters(question):
    print("'GETTING REQUIRED FILTERS---")

    with open("output.json", "r") as json_file:
        data = json.load(json_file)

    corpus = [
        f"{d.get('SL. No.', '')} {d.get('Incident ID', '')} {d.get('Caller', '')} {d.get('Location', '')} {d.get('Customer', '')} {d.get('Status', '')} {d.get('Classification', '')} {d.get('Category', '')} {d.get('Priority', '')} {d.get('Symptom', '')} {d.get('Workgroup', '')} {d.get('Analyst', '')} {d.get('Escalated To', '')} {d.get('Partner Incident', '')} {d.get('Incident Start', '')} {d.get('Solution', '')} {d.get('TTO', '')} {d.get('TTR', '')} {d.get('Closure Code', '')} {d.get('Resolve Time (24/7)', '')}".strip()

        for d in data
    ]

    corpus_embeddings = model.embed_documents(corpus)

    ##Creating embeddings for the user query
    query_embedding = model.embed_query(question)

    ##Finding cosine similarity
    similarities = cosine_similarity([query_embedding], corpus_embeddings)[0]

    print(similarities)

    most_similar_index = np.argmax(similarities)
    print(most_similar_index)

    # Getting the most similar metadata dictionary out of the list
    most_similar_dict = data[most_similar_index]

    ####Update
    ##Getting the top 5 most metadata filters based on similarity with User's Question
    # top_5_indices = np.argsort(similarities)[-5:][::-1]  # Sort in descending order

    ##Getting only top 2 because now the pages are processed in the batches of 4
    top_3_indices = np.argsort(similarities)[-1:][::-1]
    print("\n Top 3 indices: \n")
    print(top_3_indices)

    # Fetch the top 5 dictionaries
    top_3_similar_dicts = [data[i] for i in top_3_indices]

    # print("---FILTERS---")
    # print("User Question:", question)
    # print("\n Top 5 Metadata Filters \n")
    for dict_ in top_3_similar_dicts:
        print("\n")
        # print(dict_)

        # return {"question": question, "metadata": most_similar_index}
    return top_3_similar_dicts


