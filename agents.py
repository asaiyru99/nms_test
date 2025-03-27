from camelot.cli import network
from crewai_tools import CSVSearchTool, FileReadTool, JSONSearchTool
import requests
from crewai import Crew, Agent, Task, LLM

import os


os.environ['OPENAI_API_KEY'] = "A"
os.environ['GROQ_API_KEY'] = "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"
os.environ['GOOGLE_API_KEY'] = "AIzaSyDvgA6YKSuZjNoiwit3ZlGLBz86_bR9kwU"

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


class DataSegment:
    def __init__(self):
        """


        self.llm =  LLM(
            api_key="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",
            model="groq/llama-3.3-70b-versatile",
        )

        self.llm = LLM(
            api_key="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",
            model="gpt-4o-mini",
        )

        """
        self.llm = LLM(api_key="AIzaSyDvgA6YKSuZjNoiwit3ZlGLBz86_bR9kwU", model="gemini/gemini-1.5-pro-latest",
                       temperature=0.1)

    def network_expert(self, query, data):
        return Agent(

            role=f"Network Monitoring System Expert",
            goal=f""" Go through the IP address provided in the {query} and check the Availability, Packet Loss, and Response Time in the {data}. If the availability, packet loss and response time seem to be normal, that is,
            if the availability is below 90%, or the packet loss is over 4% or the response time is close to 100ms, output a response stating that the metrics of the network are not normal. Otherwise, write an answer that says the network metrics are normal.
            
            **EXAMPLE**
            
            If the packet loss is 15%
            OUTPUT: Your network is operating with a high packet loss of 15%. 
        """,
            backstory=f"You are an expert in Network Monitoring and understand the how networks function along with their parameters (packet loss, latency etc)",
            verbose=True,
            llm=self.llm

        )

    def solver(self, solver_data, query):
        return Agent(

            role=f"Expert network analysis",
            goal=f""" 1) Understand the user's query/question: {query}.
        2)Understand the contents of the {solver_data} given. You are a helper bot that solves issues in network monitoring. 
        Formulate a proper response that helps the user solve their query augmented with the {solver_data}.""",
            backstory=f"You are excellent at going through JSON data and understanding its technical context",
            verbose=True,
            llm=self.llm

        )


class Call:

    def __init__(self, query, data):
        self.query = query
        self.data = data

    def run(self):

        agents = DataSegment()
        # context_agent = agents.context_extractor(csv_search, self.industry)
        network_agent = agents.network_expert(self.query, self.data)
        #solver_agent = agents.solver(self.data, self.query)

        '''
        fetch_data = Task(
            description=f""" 
                                **Task**: Please go through the CV and fetch relevant of all the headings.
                                **Description**: Please explain what you understand from each column and draw a relationship in the data.""",
            expected_output=f"""What you understand from each column in the CV. The geographical locations explain the locations where services are offered to. IMPORTANT: KEEP IT SHORT.""",
            agent=context_agent)

        basic = Crew(
            agents = [context_agent],
            tasks = [fetch_data]
        )
        data = basic.kickoff()
        '''

        network_task = Task(
            description=f""" 
                                       **Task**: Please go through the query given {self.query} and extract the IP Address. Match the IP address with the data {self.data} and extract the parameters.
                                       **Description**: Go through the IP address provided in the {query} and check the Availability, Packet Loss, and Response Time in the corresponding data given. If the availability, packet loss and response time seem to be normal, that is,
            if the availability is below 90%, or the packet loss is over 4% or the response time is close to 100ms, output a response stating that the metrics of the network are not normal. Otherwise, write an answer that says the network metrics are normal.
            
            **EXAMPLE**
            
            If the packet loss is 15%
            OUTPUT: Your network is operating with a high packet loss of 15%. 
            
                                        **Parameters** 
                                        -query = {self.query}""",
            expected_output=f""" An accurate answer to the user's query in a short paragraph. Keep it under 500 tokens""",
            agent=network_agent)

        IP_crew = Crew(
            agents=[network_agent],
            tasks=[network_task]
        )

        answer = IP_crew.kickoff()

        '''        # answer = f"{answer}"

        ner_agent = agents.use_eval_agent(self.data, self.query, answer)
        entity_checker = Task(
            description=f""" 
                                                               **Task**: Please go through the data given: {self.data} asses the user's query: {self.query} and the bot's response: {answer} and refine it.
                                                               **Description**: You are a Named Entity Recognition (NER) system that identifies named entities from a given text. You should detect entities such as person names, organization names, location names, and other relevant terms. For each identified entity in {answer}, rephrase such that the
                                                               entity is removed.
                                                                -query = {self.query}""",
            expected_output=f""" An refined answer to the user's query""",
            agent=eval_agent)

        eval = Crew(
            agents=[eval_agent],
            tasks=[evaluate]
        )

        final_answer = eval.kickoff()
        '''

        return f"{answer}"

query = "My IP is 1.6.14.238, help"

response = Call(query, rows).run()
print(response)







