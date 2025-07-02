from langgraph.graph import StateGraph
from typing import TypedDict, List


class AgentState(TypedDict):
    name: str
    age: int
    skills: List[str]
    result: str

def user_name(state: AgentState) -> AgentState:
    """_summary_

    Args:
        state (AgentState): _description_

    Returns:
        AgentState: _description_
    """
    state['name'] = input('PLease enter your name: ')
    state['result'] = f"{state['name']}, welcome! "

    return state

def user_age(state: AgentState) -> AgentState:
    """_summary_

    Args:
        state (AgentState): _description_

    Returns:
        AgentState: _description_
    """

    state['age'] = input('PLease enter your age : ')
    state['result'] = state['result'] + f", You are {state['age']} years old."

    return state

def user_skills(state: AgentState) -> AgentState:
    """_summary_

    Args:
        state (AgentState): _description_

    Returns:
        AgentState: _description_
    """
    state['skills'] = input('PLease input list of skills you have seperatevthem with comma(,) ')
    state['result'] = state['result'] + f"You are skilled in {state['skills']}"

    return state

graph = StateGraph(AgentState)

graph.add_node("name", user_name)
graph.add_node("age", user_age)
graph.add_node("skills", user_skills)

graph.set_entry_point('name')
graph.add_edge('name', 'age')
graph.add_edge('age', 'skills')
graph.set_finish_point('skills')

app = graph.compile()

answer = app.invoke({'name': '', 'age': '', 'skills': []})
print(answer['result'])