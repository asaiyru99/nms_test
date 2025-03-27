import requests
from crewai import Crew, Agent, Task, LLM
from torch.backends import flags_frozen

from filtering import get_filters
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
        self.llm = LLM(
            api_key="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",
            model="gpt-4o-mini",
        )

    """

        self.llm =  LLM(
            api_key="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",
            model="groq/llama-3.3-70b-versatile",
        )
    
    

        

        self.llm = LLM(
            api_key="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",
            model="gpt-4o-mini",
        )
    

        
        self.llm = LLM(api_key="AIzaSyDvgA6YKSuZjNoiwit3ZlGLBz86_bR9kwU", model="gemini/gemini-1.5-pro-latest",
                       temperature=0.1)
                       
    """
    def is_it_casual(self, query):
        return Agent(

            role=f"Check the {query} and if it is conversational or not",
            goal=f""" Only respond with YES or NO
        Example: 
        
        User Input: Hi

Thought: I need to check the relevance of the user input to the network monitoring systems and network concepts.


Observation: The User Input is not relevant.

Thought: It is not relevant. Now I need to output either YES or NO.

Action: Output NO

Output: NO.

User Input: What's up?

Thought: I need to check the relevance of the user input to the network monitoring systems and network concepts.


Observation: The User Input is not relevant.

Thought: It is not relevant. Now I need to output either YES or NO.

Action: Output NO

Output: NO.

User Input: My IP is 1.6.14.238

Thought: I need to check the relevance of the user input to the network monitoring systems and network concepts.


Observation: The User Input is relevant.

Thought: It is relevant. Now I need to output either YES or NO.

Action: Output YES

Output: YES
        """,
            backstory=f"You are an expert in Network Monitoring and understand the how networks function along with their parameters (packet loss, latency etc)",
            verbose=True,
            llm=self.llm

        )

    def is_prior(self, query, data):
            return Agent(

                role=f"Check the {query} and {data} check if they are similar or not",
                goal=f""" Only respond with YES or NO
            Example: 

            User Input: My video game is broken.

    Thought: I need to check the relevance of the user input to the {data}


    Observation: The User Input is not relevant.

    Thought: It is not relevant. Now I need to output either YES or NO.

    Action: Output NO

    Output: NO.

    User Input: What's up?

    Thought: I need to check the relevance of the user input to the {data}.


    Observation: The User Input is not relevant.

    Thought: It is not relevant. Now I need to output either YES or NO.

    Action: Output NO

    Output: NO.

    User Input: My IP is 1.6.14.238, and my VPN is not connecting

    Thought: I need to check the relevance of the user input to the {data}


    Observation: The User Input is relevant.

    Thought: It is relevant. Now I need to output either YES or NO.

    Action: Output YES

    Output: YES
            """,
                backstory=f"You are an expert in Network Monitoring and understand the how networks function along with their parameters (packet loss, latency etc)",
                verbose=True,
                llm=self.llm

            )

    def network_expert(self, query, data):
        return Agent(

            role=f"Network Monitoring System Expert",
            goal=f""" Go through the IP address provided in the {query} and check the Availability, Packet Loss, and Response Time in the {data}. If the availability, packet loss and response time seem to be normal, that is,
            if the availability is below 90%, or the packet loss is over 4% or the response time is close to 100ms, output a response stating that the metrics of the network are not normal. Otherwise, write an answer that says the network metrics are normal.

            **EXAMPLE**

            If the packet loss is 15%
            OUTPUT: Your network is operating with a high packet loss of 15%. 
            If the input is unrelated to packet loss or network data, reply like a normal friendly helper bot
            **VERY IMPORTANT** ONLY COMMENT ON THE METRICS, NOTHING ELSE.    
        """,
            backstory=f"You are an expert in Network Monitoring and understand the how networks function along with their parameters (packet loss, latency etc)",
            verbose=True,
            llm=self.llm

        )

    def helper_bot(self, query):
        return Agent(

            role=f"You are a friendly helper bot",
            goal=f""" Go through the {query}, and respond in a friendly helper as a helper bot. Offer help as a network monitoring bot, and keep the responses
            short and friendly.
        """,
            backstory=f"You are an expert in Network Monitoring and are a friendly helper bot.",
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

    def __init__(self, query, data, solver_data, cat_list: list):
        self.query = query
        self.data = data
        self.solver_data = solver_data
        self.cat_data = cat_list
    def run(self):
        agents = DataSegment()
        # context_agent = agents.context_extractor(csv_search, self.industry)
        network_agent = agents.network_expert(self.query, self.data)
        solver_agent = agents.solver(self.data, self.query)
        casual_agent = agents.is_it_casual(self.query)
        helper_agent = agents.helper_bot(self.query)
        prior_agent = agents.is_prior(self.query, self.cat_data)

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
        casual_task = Task(
            description=f""" 
                                               **Task**: Only respond with YES or NO. Check the relevance of the input {self.query} with monitoring systems and network concepts.
        Example: 
        
        User Input: Hi

Thought: I need to check the relevance of the user input to the network monitoring systems and network concepts.


Observation: The User Input is not relevant.

Thought: It is not relevant. Now I need to output either YES or NO.

Action: Output NO

Output: NO

User Input: What's up?

Thought: I need to check the relevance of the user input to the network monitoring systems and network concepts.


Observation: The User Input is not similar.

Thought: It is not relevant. Now I need to output either YES or NO.

Action: Output NO

Output: NO

User Input: My IP is 1.6.14.238

Thought: I need to check the relevance of the user input to the network monitoring systems and network concepts.


Observation: The User Input is similar.

Thought: It is relevant. Now I need to output either YES or NO.

Action: Output YES

Output: YES


            
    """,
            expected_output=f""" A 'Yes.' or 'No.' """,
            agent=casual_agent)

        IP_crew = Crew(
            agents=[casual_agent],
            tasks=[casual_task]
        )

        yes_no_answer = IP_crew.kickoff()

        yes_no_answer = str(yes_no_answer)

        if yes_no_answer == "YES" or yes_no_answer == "YES." or yes_no_answer == "Yes." or yes_no_answer == "Yes":

            prior_task = Task(
                description=f""" 
                                                       **Task**: Comparing between {self.query} and {self.data} and to check relevance.
                                                       **Description**: Only respond with YES or NO
            Example: 

            User Input: My video game is broken.

    Thought: I need to check the relevance of the user input to the {self.cat_data}. Even if it is a little similar output YES


    Observation: The User Input is not relevant or similar.

    Thought: It is not relevant. Now I need to output either YES or NO.

    Action: Output NO

    Output: NO

    User Input: What's up?

    Thought: I need to check the relevance of the user input to the {self.cat_data}.


    Observation: The User Input is not similar.

    Thought: It is not relevant. Now I need to output either YES or NO

    Action: Output NO

    Output: NO

    User Input: My IP is 1.6.14.238, and my VPN is not connecting

    Thought: I need to check the relevance of the user input to the {self.cat_data}

    Observation: The User Input has some similarity.

    Thought: It is relevant. Now I need to output either YES or NO.

    Action: Output YES

    Output: YES 
    
    User Input: My IP is 1.6.14.238, and my VPN is not connecting

    Thought: I need to check the relevance of the user input to the {self.cat_data}

    Observation: The User Input has SOME SIMILARITY.

    Thought: It is a little similar. . Now I need to output either YES or NO.

    Action: Output YES

    Output: YES 

                                                        **Parameters** 
                                                        -query = {self.query}""",
                expected_output=f""" An accurate answer to the user's query in a short paragraph. Keep it under 500 tokens""",
                agent=network_agent)

            prior_crew = Crew(
                agents=[prior_agent],
                tasks=[prior_task]
            )

            answer_prior = prior_crew.kickoff()
            answer_prior = str(answer_prior)

            if answer_prior == "YES" or answer_prior == "YES." or answer_prior == "Yes." or answer_prior == "Yes":

                prior_flag = "yes"
            else:
                prior_flag = "no"


            network_task = Task(
                description=f""" 
                                           **Task**: Please go through the query given {self.query} and extract the IP Address. Match the IP address with the data {self.data} and extract the parameters.
                                           **Description**: Go through the IP address provided in the {self.query} and check the Availability, Packet Loss, and Response Time in the corresponding data given. If the availability, packet loss and response time seem to be normal, that is,
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

            solver_task = Task(
                description=f""" 
                                                   **Task**: Please go through the query given {self.query} and understand the issue that the user is facing.
                                                   **Description**: Understand the user's query/question: {self.query}. Check if the metrics of the network IP is okay with {answer}
            2)Understand the contents of the {self.solver_data} given. You are a helper bot that solves issues in network monitoring. 
            
            Study the 'Symptom' and the 'Solution' keys from {self.solver_data} and PLEASE use/augment it to formulate a response to solve the query. Use the resolved time column from {self.solver_data}
    
            
            **EXAMPLE**
            
            Query: My IP is 1.6.14.238, and im having issues connecting to my VPN
            
            Response: 
            I see you're having trouble connecting to your VPN from IP address 1.6.14.238.  Our network monitoring shows no issues with this IP address: availability is 100%, packet loss is 0%, and response time is a healthy 27ms.  This indicates the problem likely lies with your VPN client configuration rather than the network itself.
    
    A previous incident with similar symptoms ("reset mac of instasafe") was resolved by ensuring the user's device MAC address was approved for VPN access with a ticket raised with resolved time was 1 d:17 h:12 m.  Please check the following:
    
    1. **MAC Address Registration:** Ensure your device's MAC address is registered and approved for VPN access.  Your IT department or network administrator can assist with this.  You may need to provide them with your device's MAC address.
    
    2. **VPN Client Configuration:** Double-check your VPN client settings to ensure they are correct. This includes the server address, login credentials, and any required certificates.  If necessary, try reinstalling your VPN client software.
    
    3. **Firewall/Antivirus:** Temporarily disable any firewall or antivirus software on your device to see if it's interfering with the VPN connection. If this resolves the issue, configure your firewall/antivirus to allow the VPN connection.
    
    Regardless, we will raise a ticket so an engineer can look into the issue as soon as possible.
    
    Query: My IP is 1.6.14.238, give me status
    
    
    Response:
    
    Your IP address 1.6.14.238 is showing a status of 100% availability, with a packet loss of 3% and a response time of 12 milliseconds. All these values indicate that the network performance is normal: the availability is well above the acceptable threshold of 90%, the packet loss remains below the problematic level of 4%, and the response time is comfortably below 100 milliseconds.


    
    
 
    
    
    

    
    """,

                expected_output=f""" A helpful answer to the user's query that solves the issue""",
                agent=solver_agent)

            solver_crew = Crew(
                agents=[solver_agent],
                tasks=[solver_task]
            )

            #answer = IP_crew.kickoff()
            solver_answer =  solver_crew.kickoff()
            flag = False

            return f"{solver_answer}", flag, prior_flag

        else:


            helper_task = Task(
                description=f""" 
                                                       Go through the {self.query}, and respond in a friendly helper as a helper bot. Offer help as a network monitoring bot, and keep the response short and friendly!
            short and friendly. 

                                                        **Parameters** 
                                                        -query = {self.query}""",
                expected_output=f""" A friendly answer to the query, be friendly!""",
                agent=network_agent)

            helper_crew = Crew(
                agents=[helper_agent],
                tasks=[helper_task]
            )

            helper_answer = helper_crew.kickoff()

            flag = True

            prior_flag = "okay"

            return f"{helper_answer}", flag, prior_flag

'''
query = "whats up"

solver_data = get_filters(query)

response = Call(query, rows, solver_data).run()
print(response)
'''

