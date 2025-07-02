from langgraph.graph import StateGraph, START, END
from typing import TypedDict


class AgentState(TypedDict):
    num1: int
    num2: int
    num3: int
    num4: int
    operator: str
    operator2: str
    finalnum1: int
    finalnum2: int

def adder(state: AgentState) -> AgentState:
    """_summary_

    Args:
        state (AgentState): _description_

    Returns:
        AgentState: _description_
    """
    state['finalnum1'] = state['num1'] + state['num2']
    return state

def subtract(state: AgentState) -> AgentState:
    """_summary_

    Args:
        state (AgentState): _description_

    Returns:
        AgentState: _description_
    """
    state['finalnum1'] = state['num1'] - state['num2']
    return state

def adder2(state: AgentState) -> AgentState:
    """_summary_

    Args:
        state (AgentState): _description_

    Returns:
        AgentState: _description_
    """
    state['finalnum2'] = state['num3'] + state['num4']
    return state

def subtract2(state: AgentState) -> AgentState:
    """_summary_

    Args:
        state (AgentState): _description_

    Returns:
        AgentState: _description_
    """
    state['finalnum2'] = state['num3'] - state['num4']
    return state

def decide(state: AgentState) -> AgentState:
    """_summary_

    Args:
        state (AgentState): _description_

    Returns:
        AgentState: _description_
    """

    if state['operator'] == "+":
        return "addition_node"
    elif state['operator'] == "-":
        return "subtraction_node"


def decide2(state: AgentState) -> AgentState:
    """_summary_

    Args:
        state (AgentState): _description_

    Returns:
        AgentState: _description_
    """

    if state['operator2'] == "+":
        return "addition_node2"
    elif state['operator2'] == "-":
        return "subtraction_node2"

graph = StateGraph(AgentState)

graph.add_node("add_node", adder)
graph.add_node("subtract_node", subtract)
graph.add_node("decision", lambda state:state)
graph.add_node("add_node2", adder2)
graph.add_node("subtract_node2", subtract2)
graph.add_node("decision2", lambda state:state)

graph.add_edge(START, "decision")
graph.add_conditional_edges(
    "decision",
    decide,
    {
        "addition_node": "add_node",
        "subtraction_node": "subtract_node"
    }
)

graph.add_edge("add_node", "decision2")
graph.add_edge("subtract_node", "decision2")
graph.add_conditional_edges(
    "decision2",
    decide2,
    {
        "addition_node2": "add_node2",
        "subtraction_node2": "subtract_node2"
    }
)
graph.add_edge("add_node2", END)
graph.add_edge("subtract_node2", END)

app = graph.compile()

answer = app.invoke({"num1": 2, "num2": 4, "num3": 1, "num4": 6, "operator": "+", "operator2": "-", })

print(f"{answer["finalnum1"]} and {answer["finalnum2"]}")
