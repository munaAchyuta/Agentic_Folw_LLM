import ast
import os
import json

def get_function_info(node):
    params = [{'type': param.annotation.id if hasattr(param, 'annotation') and hasattr(param.annotation, 'id') else 'Any', 
               'data': param.arg} for param in node.args.args]
    return_type = node.returns.id if hasattr(node, 'returns') and hasattr(node.returns, 'id') else 'Any'
    return {
        'definition': ast.get_source_segment(source, node),
        'description': ast.get_docstring(node) or '',
        'params': params,
        'returns': {'type': return_type, 'data': 'Sample data'},
        'caller_function': 'Unknown'
    }

def get_class_info(node):
    class_info = {'definition': ast.get_source_segment(source, node)}
    for item in node.body:
        if isinstance(item, ast.FunctionDef):
            class_info[item.name] = get_function_info(item)
    return class_info

def analyze_file(file_path):
    global source
    with open(file_path, 'r') as file:
        source = file.read()
    
    tree = ast.parse(source)
    
    module_info = {'abs_path': os.path.abspath(file_path)}
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if node.name not in module_info:
                module_info[node.name] = get_function_info(node)
        elif isinstance(node, ast.ClassDef):
            module_info[node.name] = get_class_info(node)
    
    return module_info

def create_module_meta_schema(files):
    module_meta_schema = {}
    for file in files:
        module_name = os.path.basename(file)
        module_meta_schema[module_name] = analyze_file(file)
    return module_meta_schema

def get_python_files(project_path):
    python_files = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith('.py') and (not file.endswith('__init__.py')):
                python_files.append(os.path.join(root, file))
    return python_files

def generate_project_schema(project_path):
    python_files = get_python_files(project_path)
    #print(python_files)
    schema = create_module_meta_schema(python_files)
    return schema

if __name__ == '__main__':
    project_path = 'dummy_project'  # Replace with your actual project path
    schema = generate_project_schema(project_path)
    
    # Print the schema (you might want to save it to a file instead)
    print(json.dumps(schema, indent=2))