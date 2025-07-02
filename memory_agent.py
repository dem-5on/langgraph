from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage
from typing import TypedDict, List, Union
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")


class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]


llm = ChatAnthropic(model='claude-3-5-sonnet-latest')
def process(state: AgentState) -> AgentState:
    """_summary_

    Args:
        state (AgentState): _description_

    Returns:
        AgentState: _description_
    """
    response = llm.invoke(state["messages"])
    print(f"AI: \n {response.content}")
    state["messages"].append(AIMessage(content=response.content))
    print('CURRENT STATE: ', state)
    return state

graph = StateGraph(AgentState)
graph.add_node('process', process)
graph.add_edge(START, 'process')
graph.add_edge('process', END)

agent = graph.compile()

conversation_history = []
user_input = input('INPUT: ')
while user_input != 'exit':
    conversation_history.append(HumanMessage(content=user_input))
    result = agent.invoke({'messages': conversation_history})
    conversation_history = result['messages']
    user_input = input('INPUT: ')

with open('convo.txt', 'w') as file:
    file.write('YOUR CONVERSATION LOG: \n\n')

    for message in conversation_history:
        if isinstance(message, HumanMessage):
            file.write(f"YOU: {message.content}\n\n")
        elif isinstance(message, AIMessage):
            file.write(f"AI: {message.content}\n\n")
    file.write("End of conversation")

print('Coversation logged to convo.txt')