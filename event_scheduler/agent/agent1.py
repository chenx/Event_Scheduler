# This agenst asks for user questions in a loop, finds the answer and post to a webhook API end point.
# X.C.
# Last updated: 3/11/2026

from langchain_openai import ChatOpenAI
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.tools import BaseTool
from langchain_classic.agents import AgentExecutor
from langchain_classic import hub
from langchain_core.prompts import PromptTemplate
from langchain_classic.agents import create_react_agent
from langchain_classic.memory import ConversationBufferMemory

import requests
from ddgs import DDGS
from datetime import datetime

WEBHOOK_URL = "http://127.0.0.1:8000/service/datastores/"


class WebhookCallbackHandler(BaseCallbackHandler):
    def __init__(self, webhook_url=WEBHOOK_URL):
        self.webhook_url = webhook_url
        self.last_input = None
        self.eventId = 1000

    def on_chain_start(
        self, serialized: dict[str, any], inputs: dict[str, any], **kwargs: any
    ) -> None:
        """Run when chain starts to capture the initial input."""
        # Typically the input is under a key like 'input' or 'question'
        # inputs: {'input': 'Who is obama?', 'chat_history': ''}
        # print(f"inputs: {inputs}, input: {inputs['input']}")
        self.last_input = inputs['input'] if 'input' in inputs else "(none)"
        print(f"Agent Input: {self.last_input}")

    def on_agent_finish(self, finish, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.eventId += 1
        payload = {
            "uid": self.eventId, 
            "title": self.last_input, 
            "description": finish.return_values["output"],
            "created_at": timestamp,
        }
        response = requests.post(self.webhook_url, json=payload)
        print(f"Webhook triggered: {payload}")
        if response.status_code == 201:
            print(f"Webhook triggerred successfully")
        else:
            print(f"Webhook trigger error: {response.text}")


class WeatherTool(BaseTool):
    name: str = "WeatherAPI"
    description: str = "Get current weather for a city"

    def _run(self, city: str) -> str:
        if not city:
            return "No input provided, stopping execution."
        # For business use only:
        # https://www.meteomatics.com/en/weather-api/how-to-get-weather-api-key/
        # url = f"https://api.weatherapi.com/v1/current.json?key=API_KEY&q={city}"
        # response = requests.get(url)
        # return response.json()
        response = {
            "location": {"name": city},
            "current": {
                "weather": [{"main": "Rain", "description": "moderate rain"}],
                "main": {"temp": 284.2, "feels_like": 282.93, "humidity": 60},
                "wind": {"speed": 4.09},
                "name": "Province of Turin"
            }
        }
        return response


class EventTool(BaseTool):
    name: str = "EventAPI"
    description: str = "Get events"

    def _run(self, event: str) -> str:
        url = f"http://127.0.0.1:8000/api/events/"
        response = requests.get(url)
        return response.json()


class SearchTool(BaseTool):
    name: str = "WebSearch"
    description: str = "Search the web for recent information"

    def _run(self, query: str) -> str:
        if not query:
            return "No input provided, stopping execution."
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=5)
            return [r["title"] for r in results]


class NoOpTool(BaseTool):
    name: str = "noop"
    description: str = "Fallback tool when LLM output is invalid"

    def _run(self, query: str) -> str:
        return "Final Answer: Stopped because no valid action was parsed."

    async def _arun(self, query: str) -> str:
        raise NotImplementedError()


llm = ChatOpenAI(
    # model="gpt-4",
    model="gpt-4o-mini",
    temperature=0
)

tools = [SearchTool(), EventTool(), WeatherTool(), NoOpTool()]

memory = ConversationBufferMemory(memory_key="chat_history")

# https://smith.langchain.com/hub/hwchase17/react
# prompt = hub.pull("hwchase17/react")

# Create a proper ReAct prompt
# Must include {input} and {agent_scratchpad}
react_prompt_template = """
You are a ReAct agent. Follow this format:

Thought: <what you are thinking>
Action: <tool name>
Action Input: <tool input>
Observation: <result from tool>

If you cannot proceed, stop and give:
Final Answer: <your answer>

Available tools:
{tools}
Tool names: {tool_names}

Question: {input}

{agent_scratchpad}
"""

prompt = PromptTemplate.from_template(react_prompt_template)

agent = create_react_agent(
    tools=tools,
    llm=llm,
    prompt=prompt
)

webhook_handler = WebhookCallbackHandler()

agent1_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    callbacks=[webhook_handler],
    memory=memory,
    verbose=False,
    handle_parsing_errors=True,
    stop_on_invalid_action=True,
)

if __name__ == "__main__":
    while True:
        question = input("Enter your question (type 'exit' to exit): ")
        if question == "exit":
            print("Bye")
            break
        elif question == "":
            question = "Who is obama?"
        agent1_executor.invoke({"input": question})
