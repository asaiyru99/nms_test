from langchain_google_genai import GoogleGenerativeAIEmbeddings
import json
import numpy as np
model = GoogleGenerativeAIEmbeddings(model="models/embedding-001",
                                     google_api_key="AIzaSyDHSRbIV78C0d9dYsoOS0vKC9vod4ql_Vs")
from sklearn.metrics.pairwise import cosine_similarity



def get_filters(question):
    print("'GETTING REQUIRED FILTERS---")

    # question = state["question"]
    # metadata = state["metadata"]

    # question = "Do you offer print verification?"
    ##Getting the metadata
    #   grouped_data = group_values_by_keys("metadata.json")
    #   grouped_data = group_values_by_forward_slash("metadata.json")
    #   print("Grouped Metadata: ")
    #   print(f"{grouped_data}\n")
    ##Getting the metadata
    #   response = filtering_chain.invoke({"metadata": grouped_data, "question": question})

    ####Filtering the proper metadata based on similarity
    with open("output.json", "r") as json_file:
        data = json.load(json_file)

        # model = OpenAIEmbeddings()
    # model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    ##Preprocessing the data to get relevant text (Change these to the actual keys in the json file)
    corpus = [
        f"{d.get('use_case', '')} {d.get('problem', '')} {d.get('solution', '')} {d.get('product', '')} {d.get('technology', '')} {d.get('hardware', '')}".strip()

        for d in data
    ]
    ##Creating embeddings of all the preprocessed text
    corpus_embeddings = model.embed_documents(corpus)

    ##Creating embeddings for the user query
    query_embedding = model.embed_query(question)

    ##Finding cosine similarity
    similarities = cosine_similarity([query_embedding], corpus_embeddings)[0]

    print(similarities)

    # Getting the most similar index
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

    print("---FILTERS---")
    print("User Question:", question)
    print("\n Top 5 Metadata Filters \n")
    for dict_ in top_3_similar_dicts:
        print("\n")
        print(dict_)

        # return {"question": question, "metadata": most_similar_index}
    return top_3_similar_dicts


top_5 = get_filters("Do you count shrimp?")