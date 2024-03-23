import os
import json
import importlib.util
import inspect
import ast
import re
from jetline.commands._helper import _extract_pipeline_order,get_project_infos



class FunctionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.functions = []

    def visit_FunctionDef(self, node):
        self.functions.append(node)


def extract_function_code(module_path, function_name):
    spec = importlib.util.spec_from_file_location("module.name", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    function = getattr(module, function_name)
    return inspect.getsource(function)


def extract_functions_from_module(module_path):
    with open(module_path, "r") as f:
        tree = ast.parse(f.read(), filename=module_path)
        visitor = FunctionVisitor()
        visitor.visit(tree)
        functions = [ast.unparse(func) for func in visitor.functions]
        return functions


def extract_function_code_from_imports(module_path, function_name):
    with open(module_path, "r") as f:
        tree = ast.parse(f.read(), filename=module_path)
        for node in tree.body:
            if isinstance(node, ast.Import):
                for alias in node.names:
                    try:
                        module = importlib.import_module(alias.name)
                        source_path = inspect.getsourcefile(module)
                        if source_path:
                            functions = extract_functions_from_module(source_path)
                            for func_code in functions:
                                if function_name in func_code:
                                    return func_code
                    except ImportError:
                        pass
            elif isinstance(node, ast.ImportFrom):
                try:
                    module = importlib.import_module(node.module)
                    source_path = inspect.getsourcefile(module)
                    if source_path:
                        functions = extract_functions_from_module(source_path)
                        for func_code in functions:
                            if function_name in func_code:
                                return func_code
                except ImportError:
                    pass
    return None


def extract_register_function(folder_path):
    pipeline_file_path = os.path.join(folder_path, "pipeline.py")

    if os.path.exists(pipeline_file_path):
        with open(pipeline_file_path, "r") as f:
            lines = f.readlines()
            register_function_lines = []
            found_register_function = False
            for line in lines:
                if found_register_function:
                    if line.strip():  # Check if line is not empty
                        register_function_lines.append(line.rstrip())
                    else:
                        break
                elif "def register(" in line:
                    found_register_function = True
                    register_function_lines.append(line.rstrip())
            if register_function_lines:
                register_function = "\n".join(register_function_lines)
                return register_function.strip()

    return None


def extract_node_inputs(node_code):
    inputs = []
    for keyword in node_code.keywords:
        if keyword.arg == "inputs" and isinstance(keyword.value, ast.List):
            for input_elt in keyword.value.elts:
                input_str = ast.unparse(input_elt)
                if isinstance(input_str, str):
                    inputs.append(input_str)
    return inputs


def extract_node_description(function_code):
    if function_code:
        match = re.search(r'"""(.*?)"""', function_code, re.DOTALL)
        if match:
            return match.group(1).strip()
    return None


def extract_register_description(register_function_code):
    if register_function_code:
        match = re.search(r'"""(.*?)"""', register_function_code, re.DOTALL)
        if match:
            return match.group(1).strip()
    return None



def extract_functions_from_register(register_function):
    """Extract functions, inputs, outputs from a given register function."""

    functions = re.findall(r'function=([a-zA-Z0-9_.-]+)', register_function)
    inputs = re.findall(r'inputs=\[(.*?)\]', register_function)
    outputs = re.findall(r'outputs=\[(.*?)\]', register_function)
  
    return functions, inputs, outputs


def format_node_parameters(param):
    """Format given node parameter by removing unnecessary characters and splitting by comma."""

    formatted = param.replace('"', '').replace("'", "").replace(" ", "")
    return formatted.split(',')
def extract_nodes_info(folder_path, register_function):
    """Extract and return nodes information from a given Python file in a folder using a register function."""

    function_names, inputs, outputs = extract_functions_from_register(register_function)

    sorted_nodes = [None] * len(function_names)
    nodes_dict = {}

    node_file_path = os.path.join(folder_path, "nodes.py")
    if os.path.exists(node_file_path):
        with open(node_file_path, "r") as file:
            tree = ast.parse(file.read(), filename=node_file_path)

            for node_def in tree.body:
                if isinstance(node_def, ast.FunctionDef):
                    node_name = node_def.name
                    node_description = ast.get_docstring(node_def) or ''
                    node_code = ast.unparse(node_def)

                    nodes_dict[node_name] = {
                        "data": {
                          
                        "title": node_name,
                          "type": "function",
                        "code": node_code,
                        "description": node_description,
                        "inputs": "",
                        "outputs": "",
                        "stream": ""
                        }
                    }
                for i, func_name in enumerate(function_names):
                    node_name = func_name.split('.')[-1]
                    if node_name in nodes_dict:
                        sorted_nodes[i] = nodes_dict[node_name]

                        if i < len(inputs):
                            sorted_nodes[i]["data"]["inputs"] = format_node_parameters(inputs[i])

                        if i < len(outputs):
                            sorted_nodes[i]["data"]["outputs"] = format_node_parameters(outputs[i])

                        # Adding 'stream' attribute
                        if sorted_nodes[i]["data"]["inputs"] and sorted_nodes[i]["data"]["outputs"]:
                            sorted_nodes[i]["data"]["stream"] = ["input", "output"]
                        elif sorted_nodes[i]["data"]["inputs"]:
                            sorted_nodes[i]["data"]["stream"] = ["input"]
                        elif sorted_nodes[i]["data"]["outputs"]:
                            sorted_nodes[i]["data"]["stream"] = ["output"]
                        else:
                            sorted_nodes[i]["data"]["stream"] = []


            return sorted_nodes

    return []




def extract_register_info(folder_path):
    pipeline_file_path = os.path.join(folder_path, "pipeline.py")

    if os.path.exists(pipeline_file_path):
        with open(pipeline_file_path, "r") as f:
            tree = ast.parse(f.read(), filename=pipeline_file_path)
            for node_def in tree.body:
                if isinstance(node_def, ast.FunctionDef) and node_def.name == "register":
                    register_function_code = ast.unparse(node_def)
                    register_description = extract_register_description(register_function_code)
                    return register_description

    return None

def extract_data_classes_info(current_directory):
    data_classes_info = []
    data_file_path = os.path.join(current_directory, "data.py")
    if os.path.exists(data_file_path):
        with open(data_file_path, 'r') as f:
            tree = ast.parse(f.read(), filename=data_file_path)
            for i,node in enumerate(tree.body):
                if isinstance(node, ast.ClassDef):
                    class_description = ast.get_docstring(node)
                    class_code = ast.unparse(node)

                    class_name_match = re.search(r"name\s*=\s*'([^']*)'", class_code)
                    class_name = class_name_match.group(1) if class_name_match else "Unknown"

                    data_classes_info.append({
                      
                        "data": {
                        "title": class_name,
                         "type": "data",
                        "description": class_description if class_description else "",
                        "code": class_code}
                    })
    return data_classes_info




def main():
    
    project_name,place_path, current_dir=  get_project_infos()
    

   
    pipeline_order = _extract_pipeline_order(current_dir)
    pipeline_folders = [folder for folder in os.listdir(place_path) if os.path.isdir(os.path.join(place_path, folder))]
    pipeline_folders = sorted(pipeline_folders,
                              key=lambda x: pipeline_order.index(x) if x in pipeline_order else len(pipeline_order))
    
    nodes = []
    data = {
        "ProjectName": project_name,
        "DataClasses": [],
        "Pipelines": {}
    }

    # Extract data classes information
    
    nodes.extend(extract_data_classes_info(current_dir))

    
   # data["DataClasses"] = data_classes_info

    # Extract pipeline information

    for folder in pipeline_folders:
        folder_path = os.path.join(place_path, folder)
        pipeline_info = {
            "RegisterFunction": {
                "Function": None,
                "Description": None
            },
            "Nodes": None
        }

        # Extract register function information
        register_function = extract_register_function(folder_path)
        pipeline_info["RegisterFunction"]["Function"] = extract_register_function(folder_path)
        pipeline_info["RegisterFunction"]["Description"] =  extract_register_description(register_function)

        # Extract nodes information
        nodes_info = extract_nodes_info(folder_path, register_function)
        pipeline_info["Nodes"] = nodes_info
        nodes.extend(nodes_info)
      
        # Add pipeline information to data
        data["Pipelines"][folder] = pipeline_info
    
  #  print(nodes)
    json_file_path = os.path.join(current_dir, "viz-data.json")
    with open(json_file_path, "w") as json_file:
        json.dump(nodes, json_file, indent=4)

    print("JSON-Datei erfolgreich erstellt.")


if __name__ == "__main__":
    main()
