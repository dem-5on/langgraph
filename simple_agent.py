from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage
from typing import TypedDict, List
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

class AgentInput(TypedDict):
    messages: List[HumanMessage]

llm = ChatAnthropic(model='claude-3-5-sonnet-latest')

def simple_agent(state: AgentInput) -> AgentInput:
    """ Simple agent that answer questions using anthropic api """
    response = llm.invoke(state["messages"])
    print(f"AI: \n {response.content}")
    return state

graph = StateGraph(AgentInput)

graph.add_node('process', simple_agent)
graph.add_edge(START, 'process')
graph.add_edge('process', END)

agent = graph.compile()

user_input = input('ENTER: ')
while user_input != "exit":
    agent.invoke({"messages": [HumanMessage(content=user_input)]})
    user_input = input('ENTER: ')
