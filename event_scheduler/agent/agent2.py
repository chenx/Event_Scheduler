# This agenst asks for user questions in a loop, finds the answer and post to a webhook API end point.
# This removed the use of deprecated ConversationBufferMemory from langchain_classic.agents,
# and uses create_agent from langchain instead of create_react_agent from langchain_classic.
# X.C.
# Last updated: 3/12/2026

from langchain_openai import ChatOpenAI
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.tools import BaseTool
from langchain_core.prompts import PromptTemplate
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.globals import set_verbose, set_debug

import json
import requests
from ddgs import DDGS
from datetime import datetime

set_verbose(True)
# set_debug(True)

WEBHOOK_URL = "http://127.0.0.1:8000/service/datastores/"

class WebhookCallbackHandler(BaseCallbackHandler):
    def __init__(self, webhook_url=WEBHOOK_URL):
        self.webhook_url = webhook_url
        self.last_input = None
        self.eventId = 1000
    
    def on_chain_start(
        self, serialized: dict[str, any], inputs: dict[str, any], run_id, parent_run_id, **kwargs: any
    ) -> None:
        """Run when chain starts to capture the initial input."""
        if not parent_run_id == None:
            # {'messages': [HumanMessage(content='...', additional_kwargs={}, response_metadata={}, id='...')]}
            return
        
        try:
            self.last_input = inputs['messages'][0]['content']
        except Exception as e:
            self.last_input = f"(error: {e})"
            # print(f"Agent Input: {self.last_input}")

    def on_chain_end(self, outputs, parent_run_id=None, **kwargs):
        if not parent_run_id is None:
            # {'messages': [HumanMessage(content='...', additional_kwargs={}, response_metadata={}, id='...')]}
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.eventId += 1
        # print(outputs)
        payload = {
            "uid": self.eventId, 
            "title": self.last_input, 
            "description": outputs["messages"][-1].content,
            "created_at": timestamp,
        }
        response = requests.post(self.webhook_url, json=payload)
        # print(f"Webhook triggered: {payload}")
        if response.status_code == 201:
            # print(f"Webhook triggerred successfully")
            pass
        else:
            print(f"Webhook trigger error: {response.text}")


class WeatherTool(BaseTool):
    """
    Check the weather of a city.
    """
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
    """
    Get events in local database.
    """
    name: str = "EventAPI"
    description: str = "Get events"

    def _run(self, event: str) -> str:
        url = f"http://127.0.0.1:8000/api/events/"
        response = requests.get(url)
        return response.json()


class SearchTool(BaseTool):
    """
    Search online for information.
    """
    name: str = "WebSearch"
    description: str = "Search the web for recent information"

    def _run(self, query: str) -> str:
        if not query:
            return "No input provided, stopping execution."
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=5)
            return [r["title"] for r in results]


class NoOpTool(BaseTool):
    """
    The fallback tool when other tools cannot be used.
    """
    name: str = "noop"
    description: str = "Fallback tool when LLM output is invalid"

    def _run(self, query: str) -> str:
        return "Final Answer: Stopped because no valid action was parsed."

    async def _arun(self, query: str) -> str:
        raise NotImplementedError()


tools = [SearchTool(), EventTool(),WeatherTool(), NoOpTool()]

# Create a proper ReAct prompt
# Must include {input} and {agent_scratchpad}
react_prompt_template = """
You are a ReAct agent. Follow this format and convert it into a JSON message:

Thought: <what you are thinking>
Action: <tool name>
Action Input: <tool input>
Observation: <result from tool as a single string>

If you cannot proceed, stop and give this as a JSON message:

Final Answer: <your answer>

Available tools:
{tools}
Tool names: {tool_names}

Question: {input}

{agent_scratchpad}
"""

llm = ChatOpenAI(
    model="gpt-4o-mini",
    # model="gpt-4.1",
    temperature=0.7
)

agent = create_agent(
    tools=tools,
    # model="gpt-4o-mini",
    # model="gpt-4",
    model=llm,
    system_prompt=react_prompt_template,
    checkpointer=InMemorySaver()
)

agent = agent.with_config(
    {"callbacks": [WebhookCallbackHandler()]}
)


class AgentExecutor():
    def invoke(self, input) -> str:
        try:
            question = input['input']
            result = agent.invoke(
                        {"messages": [{"role": "user", "content": question}]},
                        {"configurable": {"thread_id": "1"}},
                    )
            # print(result)
            outputs = result["messages"][-1].content if result.get("messages") else None
            # print(response)
            if outputs is None:
                return "(none)"
            else:
                data = json.loads(outputs)
                if 'Final Answer' in data:
                    return data['Final Answer']

                if 'Observation' in data:            
                    return data['Observation']

                return '(no data is returned)'

        except Exception as e:
            # print(f"execute_agent error: {e}")
            return f"execute_agent error: {e}"

agent2_executor = AgentExecutor()


def execute_agent():
    try:
        result = agent.invoke(
                    {"messages": [{"role": "user", "content": question}]},
                    {"configurable": {"thread_id": "1"}},
                )
        # print(result)
        outputs = result["messages"][-1].content if result.get("messages") else None
        # print(response)
        if outputs is None:
            print("\n(None)")
        else:
            data = json.loads(outputs)
            if 'Final Answer' in data:
                print(f"\n{data['Final Answer']}")
            elif 'Observation' in data:            
                print(f"\n{data['Observation']}")
            else:
                print(f"\n(null)")

    except Exception as e:
        print(f"execute_agent error: {e}")


if __name__ == "__main__":
    while True:
        question = input("\n==> Enter your question (type 'exit' to exit): ")
        if question == "exit":
            break
        elif question != "": 
            # e.g., "Who is obama?", "What's the weather at San Jose today?"
            execute_agent()
