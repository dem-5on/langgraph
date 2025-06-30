from langgraph.graph import StateGraph
from typing import TypedDict, Dict


class AgentState(TypedDict):
    message: str


def send_message(state: AgentState, ) -> AgentState:
    """ Send a simple good morning message"""

    state['message'] = "Hey, "+ state["message"] + ", how is your day?"

    return state

app = StateGraph(AgentState)

greeter = app.add_node("greeter", send_message)

greeter.set_entry_point("greeter")
greeter.set_finish_point("greeter")

result = greeter.compile()
print(result.invoke({"message": "Joe"}))
