from typing import Dict, List
from langgraph.graph import Graph
from langgraph.prebuilt import PromptNode
import json

# Define the system message and context
SYSTEM_MESSAGE = """You are an AI assistant tasked with analyzing function definitions and their context to determine if sufficient information is available for test generation."""

FUNCTION_CONTEXT = """
def add_numbers(a: int, b: int) -> int:
    return a + b

def multiply_numbers(x: int, y: int) -> int:
    return x * y
"""

def check_test_info(state):
    prompt = f"{SYSTEM_MESSAGE}\n\nFunction and Context:\n{FUNCTION_CONTEXT}\n\nAnalyze and answer the following questions (yes/no):"
    questions = [
        "Can input/output data structures be identified?",
        "Can sample test data be created?",
        "Is there sufficient clear information to create test mocks for dependencies?"
    ]
    
    llm_response = state['llm'](prompt + "\n".join(questions))
    
    # Parse LLM response into yes/no answers
    answers = [line.split(":")[-1].strip().lower() for line in llm_response.split("\n") if line]
    response = {q: a for q, a in zip(questions, answers)}
    
    state['analysis'] = response
    return state

def get_user_input(state):
    print("Additional information needed. Please provide:")
    for question, answer in state['analysis'].items():
        if answer == 'no':
            user_input = input(f"{question}: ")
            state['analysis'][question] = "yes"
            state['additional_info'] = state.get('additional_info', "") + f"\n{question}: {user_input}"
    return state

def generate_test_code(state):
    prompt = f"{SYSTEM_MESSAGE}\n\nFunction and Context:\n{FUNCTION_CONTEXT}\n"
    if 'additional_info' in state:
        prompt += f"\nAdditional Information:\n{state['additional_info']}\n"
    prompt += "\nGenerate test scenarios and code for the given function(s):"
    
    llm_response = state['llm'](prompt)
    state['test_code'] = llm_response
    return state

def router(state):
    if all(state['analysis'].values()):
        return "generate_test_code"
    else:
        return "get_user_input"

# Create the graph
workflow = Graph()

# Add nodes to the graph
workflow.add_node("check_test_info", check_test_info)
workflow.add_node("get_user_input", get_user_input)
workflow.add_node("generate_test_code", generate_test_code)

# Add edges
workflow.add_edge("check_test_info", router)
workflow.add_edge("get_user_input", "check_test_info")
workflow.add_edge("generate_test_code", END)

# Set the entry point
workflow.set_entry_point("check_test_info")

# Compile the graph
app = workflow.compile()

# Run the graph
final_state = app.invoke({
    "llm": PromptNode(model_name="gpt-3.5-turbo")  # You may need to configure this based on your setup
})

print("\nAnalysis Results:")
print(json.dumps(final_state['analysis'], indent=2))

if 'additional_info' in final_state:
    print("\nAdditional Information Provided:")
    print(final_state['additional_info'])

print("\nGenerated Test Code:")
print(final_state['test_code'])