import os
from dotenv import load_dotenv
from langchain_core import tools
from langgraph.prebuilt import ToolNode
from langchain_anthropic import ChatAnthropic
from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import (HumanMessage, AIMessage, 
                                     SystemMessage, BaseMessage, ToolMessage)


load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

document_content =""

def update(content: str) -> str:
    """_summary_

    Args:
        content (str): add the provided content to the document

    Returns:
        str: and returns the content of the document
    """
    global document_content
    document_content = content
    return f"Document has succesfully been added {document_content}"

def save_doc(filename: str) -> str:
    """_summary_

    Args:
        filename (str): Save the current document to a text file 

    Returns:
        str: Return the document
    """
    global document_content
    if not filename.endswith('.txt'):
        filename = f"{filename}.txt"


    try:
        with open(filename, 'w') as file:
            file.write(document_content)
        return f"Document saved successfully to {filename}"
    except Exception as e:
        print(e)
        return f"Error saving document: {str(e)}"
    

tools = [update, save_doc]

llm = ChatAnthropic(model_name='claude-3-5-sonnet-latest').bind_tools(tools)

def worker(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content=f""" You are a document Drafter, a helpful writing assistant.You are my personal AI assistant that make use of provided tools base on tasks youve been assigned
    - Use the update tool to modify or update the document if the user want to do that
    - Use the save tool to save and finish if the user wants to finish the document
    - Make sure to always show the content of the current document
    The current document is {document_content}    
    """)
    
    if not state['messages']:
        user_input=f"I can help you modify your documents, What would you like to do?"
        user_message = HumanMessage(content=user_input)
    else:
        user_input = input("\nWhat would you like to do with the document? ")
        print(f"USER: {user_input}")
        user_message = HumanMessage(content=user_input)

    all_messages = [system_prompt] + list(state['messages']) + [user_message]

    response = llm.invoke(all_messages)
    print(f"AI: {response.content}")
    if hasattr(response, 'tool_calls') and response.tool_calls:
        print(f"USING TOOL: {[tc['name'] for tc in response.tool_calls]}")
    return {'messages': list(state['messages']) + [user_message, response]}

def should_continue(state: AgentState) -> str:
    """ Determine if we should continue or end the conversation"""
    messages = state['messages']

    for message in reversed(messages):
        if ((isinstance(message, ToolMessage)) and ("saved" in message.content.lower()) and ("document" in message.content.lower())):
            return "end"
    return "continue"


def print_messages(messages):
    if not messages:
        return 
    
    for message in messages[-3:]:
        if isinstance(message, ToolMessage):
            print(f"TOOL RESULT: {message.content}")


graph = StateGraph(AgentState)

graph.add_node('agent', worker)
graph.add_node('tools', ToolNode(tools))

graph.set_entry_point('agent')

graph.add_edge('agent', 'tools')
graph.add_conditional_edges(
    'tools',
    should_continue,
    {
        "continue": "agent",
        "end": END
    }
)

app = graph.compile()

def run():
    print("=====GRAFTER====")

    state = {'messages': []}

    for step in app.stream(state, stream_mode='values'):
        if "messages" in step:
            print_messages(step['messages'])
    print("=======DRAFTER FINISHED=========")

if __name__ == "__main__":
    run()