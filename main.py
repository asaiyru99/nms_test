import streamlit as st
import random
import time
from agents_final import Call
from filtering import get_filters
import requests

if "first" not in st.session_state:
    st.session_state.first = False
if "data" not in st.session_state:
    st.session_state["data"] = True
if "theme" not in st.session_state:
    st.session_state["theme"] =  ""
if "button_list" not in st.session_state:
    st.session_state.button_list =  []
if "page_name" not in st.session_state:
    st.session_state.page_name =  ""
if "home" not in st.session_state:
    st.session_state.home = False

class Main:
    def __init__(self):
        self.home_page()

        #if st.session_state["uploaded_files"] and not st.session_state["confirmed"]:
        #if st.session_state["first"]:
            #self.dept()

        #if st.session_state["confirmed"]:
            #self.process_files()

        #if st.session_state["chat_active"]:
            #self.chat_interface()

        #self.reset_app()

    def home_page(self):
        st.sidebar.title("Dashboard")
        st.sidebar.image("LOGO.png", width=150)

        st.sidebar.subheader("Navigation")
        page = st.sidebar.selectbox(
            "Select Domain:",
            #["Home", "Automotive & Ancillary & Heavy", "CPG", "Energy and Power", "FMCG", "Hospitals and Healthcare", "Hotels & Hospitality", "Infrastructure and HeavyMachine", "Logistics,Warehousing and Trans", "Mining & Metals & Heavy Infrast", "Pharma & Chemicals", "Retail & E-Commerce", "Textile"]
            #[
            ['NMS Helper']

        )

        # Text Input
        #user_input = st.sidebar.text_input("Search something", "")

        # Checkbox
        #show_data = st.sidebar.checkbox("Show data")
        st.title("Network Monitoring System Helper")
        #st.write(f"You're currently on the **{page}** page.")

        if st.session_state["data"]:
        # Different behavior based on the page selected
            for st.session_state.page_name in page:
                if st.session_state.page_name:

                    st.session_state.button_list = ["Chat with me!"]
                elif page =="Home":
                    st.write("Welcome")
                    st.session_state.home = True


            #if page != "Home":
            with st.container():
                for button_name in st.session_state.button_list:
                    if st.button(button_name) :
                        st.write(f"You clicked: {button_name}")


                        st.session_state["first"] = True

            if st.session_state["first"]:
                #st.write(
                    #f"Generating data for **{button_name}** ...")
                #st.write("**Data**")
                #st.write(f"Data being used: {page}.csv")

                def response_generator(query):
                    import urllib3

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

                    import json

                    data = response.text
                    json_data = f'''{data}'''

                    data = json.loads(json_data)

                    rows = data.get("rows", [])

                    rows = str(rows)

                    solver_data = get_filters(query)


                    response = Call(query, rows, solver_data).run()





                    response = str(response)

                    #return st.markdown(response)

                    for word in response.split():
                        yield word + " "
                        time.sleep(0.05)


                #st.markdown()

                # Initialize chat history
                if "messages" not in st.session_state:
                    st.session_state.messages = []

                # Display chat messages from history on app rerun
                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

                if prompt := st.chat_input("Ask your question"):
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    with st.chat_message("user"):
                        st.markdown(prompt)

                    with st.chat_message("assistant"):
                        page_path = f"{page}.csv"
                        response = st.write_stream(response_generator(prompt))
                    st.session_state.messages.append({"role": "assistant", "content": response})




Main()