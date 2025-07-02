from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, START, END
from langchain_core import tools
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
from langchain_core.messages import (HumanMessage, AIMessage, 
                                     SystemMessage, BaseMessage, ToolMessage)
from typing import TypedDict, Annotated, Sequence
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# @tools
def add(a: int, b: int):
    """_summary_

    Args:
        a (int): first number 
        b (int): second number

    Returns:
        int: an integer number/function
    """
    return a + b

def multiply(a: int, b: int):
    """_summary_

    Args:
        a (int): first number 
        b (int): second number

    Returns:
        int: an integer number/function
    """
    return a * b

def divide(a: int, b: int):
    """_summary_

    Args:
        a (int): first number 
        b (int): second number

    Returns:
        int: an integer number/function
    """
    return a / b

tools = [add, divide, multiply]
llm = ChatAnthropic(
    model_name='claude-3-5-sonnet-latest'
).bind_tools(tools)


def llm_call(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(
        'You are my AI assistant, PLease answer my queries to the best of your knowledge'
    )
    response = llm.invoke([system_prompt] + state['messages'])

    return {'messages': response}


def should_continue(state: AgentState):
    messages = state['messages']
    latest_message = messages[-1]

    if not latest_message.tool_calls:
        return 'end'
    else:
        return 'continue'
    

graph = StateGraph(AgentState)

graph.add_node('model', llm_call)
tools_node = ToolNode(tools=tools)

graph.add_node('tools', tools_node)

graph.add_edge(START, 'model')
graph.add_conditional_edges(
    'model',
    should_continue,
    {
        'continue': 'tools',
        'end': END
    }
)
graph.add_edge('tools', 'model')

app = graph.compile()

def print_stream(stream):
    for s in stream:
        message = s['messages'][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

input = {'messages': [("user", "Add 3 + 4. Add 92+ 16 Add 12 + 90 After tha multiply the first answer by 9 and devide the second answer by 3")]}
print_stream(app.stream(input, stream_mode='values'))