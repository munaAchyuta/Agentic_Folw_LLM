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


def get_definition(schema, item_name):
    for module, module_info in schema.items():
        if item_name in module_info:
            item_info = module_info[item_name]
            if isinstance(item_info, dict):
                return item_info.get('definition', 'Definition not found')
    return 'Item not found in schema'

def get_hierarchical_dependencies(schema, start_item, max_depth=None):
    def recurse(item, depth=0):
        if max_depth is not None and depth > max_depth:
            return None
        
        if item not in visited:
            visited.add(item)
            result = {
                "name": item,
                "definition": get_definition(schema, item),
                "depth": depth,
                "dependencies": []
            }
            
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
with open('processed_schema_2.json', 'w') as f:
    json.dump(result, f, indent=2)

# Function to print hierarchical dependencies
def print_hierarchical_dependencies(tree, indent=""):
    print(f"{indent}{tree['name']} (depth: {tree['depth']})")
    print(f"{indent}Definition: {tree['definition']}\n")
    for dep in tree['dependencies']:
        print_hierarchical_dependencies(dep, indent + "  ")

# Example usage
print("Hierarchical dependencies for 'create_item':")
create_item_deps = get_hierarchical_dependencies(schema, 'create_item', max_depth=3)
print_hierarchical_dependencies(create_item_deps)

# Print updated caller functions for 'Car'
print("\nUpdated caller functions for 'Car':")
print(result['updated_schema']['car_emi.py']['Car']['caller_function'])