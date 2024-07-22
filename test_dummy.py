import inspect
import networkx as nx

def build_dependency_graph(module):
    graph = nx.DiGraph()
    
    # Iterate over all functions in the module
    for name, func in inspect.getmembers(module, inspect.isfunction):
        print("func------")
        print(func)
        # Get the function's signature
        signature = inspect.signature(func)
        print('signature-----')
        print(signature)
        # Add the function to the graph
        graph.add_node(name)
        
        # Check for dependencies in the function body
        print('signature.parameters------')
        print(signature.parameters)
        print('\n')
        for param in signature.parameters:
            # If the parameter is a callable, add an edge to the graph
            if inspect.isfunction(param):
                graph.add_edge(param, name)
    
    return graph

# Example usage
import sb_main  # Replace with your actual module name
dependency_graph = build_dependency_graph(sb_main)
#print(nx.info(dependency_graph))
print(dependency_graph)
print(dependency_graph.nodes)