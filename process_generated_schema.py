import json
from collections import defaultdict

def build_dependency_tree(schema, start_item):
    def recurse(item, depth=0):
        if item not in visited:
            visited.add(item)
            result = {"name": item, "depth": depth, "dependencies": []}
            
            for module, module_info in schema.items():
                if item in module_info:
                    item_info = module_info[item]
                    if isinstance(item_info, dict):
                        dependencies = item_info.get('dependency_from_body', []) + item_info.get('dependency_from_input', [])
                        for dep in dependencies:
                            dep_result = recurse(dep, depth + 1)
                            if dep_result:
                                result["dependencies"].append(dep_result)
            
            return result
        return None

    visited = set()
    return recurse(start_item)

def update_caller_functions(schema):
    caller_map = defaultdict(list)
    
    # Build a map of all potential callers
    for module, module_info in schema.items():
        for item, item_info in module_info.items():
            if isinstance(item_info, dict):
                dependencies = item_info.get('dependency_from_body', []) + item_info.get('dependency_from_input', [])
                for dep in dependencies:
                    caller_map[dep].append(item)
    
    # Update the schema with caller information
    for module, module_info in schema.items():
        for item, item_info in module_info.items():
            if isinstance(item_info, dict):
                item_info['caller_function'] = caller_map[item]

def process_schema(schema):
    # Update caller functions
    update_caller_functions(schema)
    
    # Build dependency trees for all items
    dependency_trees = {}
    for module, module_info in schema.items():
        for item in module_info.keys():
            if isinstance(module_info[item], dict):
                dependency_trees[item] = build_dependency_tree(schema, item)
    
    return {
        "updated_schema": schema,
        "dependency_trees": dependency_trees
    }

# Load the schema
with open('schema.json', 'r') as f:
    schema = json.load(f)

# Process the schema
result = process_schema(schema)

# Save the result
with open('processed_schema.json', 'w') as f:
    json.dump(result, f, indent=2)

# Example usage
def print_dependency_tree(tree, indent=""):
    print(f"{indent}{tree['name']} (depth: {tree['depth']})")
    for dep in tree['dependencies']:
        print_dependency_tree(dep, indent + "  ")

# Print dependency tree for 'create_item'
print("Dependency tree for 'create_item':")
print_dependency_tree(result['dependency_trees']['create_item'])

# Print updated caller functions for 'Car'
print("\nUpdated caller functions for 'Car':")
print(result['updated_schema']['car_emi.py']['Car']['caller_function'])