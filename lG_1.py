from typing import Dict, List
from langgraph.graph import Graph
from langgraph.prebuilt import PromptNode

# Define the system message and context
SYSTEM_MESSAGE = """You are a test scenario and code generator. 
Given a function, create test scenarios and corresponding test code."""

FUNCTION_CONTEXT = """
def add_numbers(a: int, b: int) -> int:
    return a + b
"""

# Create the first node for generating test scenarios and code
def generate_tests(state):
    prompt = f"{SYSTEM_MESSAGE}\n\nFunction:\n{FUNCTION_CONTEXT}\n\nGenerate test scenarios and code:"
    llm_response = state['llm'](prompt)
    state['test_scenarios'] = llm_response
    return state

# Create the second node (placeholder for now)
def second_node(state):
    # This is a placeholder function for the second node
    # You can implement its logic based on your requirements
    state['second_node_output'] = "Processed by second node"
    return state

# Create the graph
workflow = Graph()

# Add nodes to the graph
workflow.add_node("generate_tests", generate_tests)
workflow.add_node("second_node", second_node)

# Connect the nodes
workflow.add_edge("generate_tests", "second_node")

# Set the entry point
workflow.set_entry_point("generate_tests")

# Compile the graph
app = workflow.compile()

# Run the graph
final_state = app.invoke({
    "llm": PromptNode(model_name="gpt-3.5-turbo")  # You may need to configure this based on your setup
})

print("Test Scenarios and Code:")
print(final_state['test_scenarios'])
print("\nSecond Node Output:")
print(final_state['second_node_output'])