# my first langgraph project -- single input
from langgraph.graph import StateGraph
from typing import TypedDict, List

#schema
class AgentState(TypedDict):
    message: str
    value: List[int]
    result: str
    operator: str
    

def send_message(state: AgentState, ) -> AgentState:
    """ Send a simple good morning message"""

    state['message'] = "Hey, "+ state["message"] + ", how is your day?"

    return state

app = StateGraph(AgentState)

greeter = app.add_node("greeter", send_message)

greeter.set_entry_point("greeter")
greeter.set_finish_point("greeter")

result = greeter.compile()
answer = result.invoke({"message": "Joe"})
print(answer['message'])


#multiple inputs

def process_val(state: AgentState) -> AgentState:
    """ this is to perform multiple task"""

    state['result'] = f"Hey there {state["message"] }, these are the values you passed in  = {state["value"]}"

    return state

app = StateGraph(AgentState)
processor = app.add_node("process", process_val)

processor.set_entry_point("process")
processor.set_finish_point("process")

result = processor.compile()

answer = result.invoke({"message":"Joe", "value":[1,2, 2,3,3]})
print(answer['result'])


#if-statement graph

def operation(state: AgentState) -> AgentState:
    """Perform operation on a list of integer values """

    if state['operator'] == '*':
        multi = map(lambda x : x * x, state['value'])
        state['result'] = f"Hey {state['message']}, Your answer is {sum(multi)} "
    elif state["operator"] == '+':
        add = map(lambda x: x + x, state['value'])
        state['result'] = f"Hey {state['message']}, Your answer is {sum(add)} "
    else:
        print('Could not execute both * and + operations')
    
    return state

app = StateGraph(AgentState)

operate = app.add_node("op", operation)

operate.set_entry_point("op")
operate.set_finish_point("op")

result = operate.compile()

answer = result.invoke({"message": "Joe", "value": [1,2,3,4,5], "operator": "+"})

print(answer['result'])
