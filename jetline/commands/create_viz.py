import os
import ast
import astor
import toml
import re
import json
import shutil
import subprocess
import sys


def get_project_infos():
    """Fetches the project name and path based on project settings in a TOML file."""
    current_dir = os.getcwd()
    toml_file_path = os.path.join(current_dir, "project.toml")

    try:
        with open(toml_file_path, "r") as file:
            toml_data = toml.load(file)
            project_name = toml_data.get("project", {}).get("name")
            place = toml_data.get("project", {}).get("place")
            if not project_name or not place:
                return None, None
            place_path = os.path.join(current_dir, place)
            return project_name, place_path, current_dir
    except Exception:
        raise ValueError("Project name or place is missing in the TOML file.")


def extract_class_name(class_code):
    # Suchen Sie nach dem ersten Auftreten von 'name =' im Klassencode
    match = re.search(r"name\s*=\s*[\"']([^\"']+)[\"']", class_code)
    if match:
        # Extrahieren Sie den Namen aus dem Regex-Match
        class_name = match.group(1)
        return class_name


def extract_classes_with_parent(current_dir):
    """
    Extracts all classes with a given parent class from a file.
    """
    nodes = []
    file_path = os.path.join(current_dir, "data.py")
    with open(file_path, "r") as f:
        tree = ast.parse(f.read())

        for node in ast.walk(tree):
            if (
                    isinstance(node, ast.ClassDef) and
                    any("Data" in base.id for base in node.bases if isinstance(base, ast.Name))
            ):
                meta = {
                    assign.targets[0].id: ast.literal_eval(assign.value)
                    for inner_node in node.body
                    if (
                            isinstance(inner_node, ast.ClassDef) and
                            inner_node.name == 'Meta'
                    )
                    for assign in inner_node.body
                    if isinstance(assign, ast.Assign)
                }
                class_code = astor.to_source(node)
                node_name = extract_class_name(class_code)
                nodes.append({
                    "id": node_name,
                    "data": {
                        "title": node_name,
                        "type": "data",
                        "description": meta.get("description", "No description provided"),
                        "outputs": node_name,
                        "inputs": None,
                        "code": class_code
                    },
                    "position": {
                        "x": meta.get("x", 0),
                        "y": meta.get("y", 0)
                    }
                })
    return nodes


# pipelines extractor

def extract_functions_from_register(register_function):
    """Extract functions, inputs, outputs from a given register function."""

    functions = re.findall(r'function=([a-zA-Z0-9_.-]+)', register_function)
    inputs = re.findall(r'inputs=\[(.*?)\]', register_function)
    outputs = re.findall(r'outputs=\[(.*?)\]', register_function)
    viz = re.findall(r'viz=\{(.*?)\}', register_function)

    return functions, inputs, outputs, viz


def format_node_parameters(param):
    """Format given node parameter by removing unnecessary characters and splitting by comma."""

    formatted = param.replace('"', '').replace("'", "").replace(" ", "")
    return formatted.split(',')


def extract_nodes_info(folder_path, register_function):
    """Extract and return nodes information from a given Python file in a folder using a register function."""

    function_names, inputs, outputs, viz = extract_functions_from_register(register_function)
    sorted_nodes = [None] * len(function_names)
    nodes_dict = {}
    edges = []

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
                        "id": node_name,
                        "data": {
                            "title": node_name,
                            "description": node_description,
                            "type": "function",
                            "code": node_code,
                            "inputs": '',
                            "outputs": '',
                        },
                        "position": {
                            "x": '',
                            "y": '',
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

            for i, position_data in enumerate(viz):
                node_name = function_names[i].split('.')[-1]

                position_dict = eval("{" + position_data + "}")
                x = position_dict['x']
                y = position_dict['y']
                sources = position_dict['sources']

                for source in sources:
                    sorted_nodes[i]["position"]["x"] = x
                    sorted_nodes[i]["position"]["y"] = y

                    edge_id = f"{source}->{node_name}"
                    edges.append({
                        "id": edge_id,
                        "source": source,
                        "target": node_name,
                        "animated": True,
                        "type": "default",
                        "style": "edgeStyle"
                    })

            return sorted_nodes, edges

    return [], []


def extract_register_functions_from_pipeline(pipeline_file_path):
    with open(pipeline_file_path, "r") as f:
        tree = ast.parse(f.read())

        register_functions = ""
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name == 'register':
                register_functions = ast.unparse(node)
                break  # Stop after finding the first 'register' function
    return register_functions


def extract_data_from_pipelines(current_dir, place_path):
    nodes = []
    edges = []

    pipeline_folders = [folder for folder in os.listdir(place_path) if os.path.isdir(os.path.join(place_path, folder))]

    for folder in pipeline_folders:
        folder_path = os.path.join(current_dir, place_path, folder)
        pipeline_file_path = os.path.join(folder_path, "pipeline.py")
        if os.path.exists(pipeline_file_path):
            register_function = extract_register_functions_from_pipeline(pipeline_file_path)

            extracted_nodes, extracted_edges = extract_nodes_info(folder_path, register_function)
            nodes += extracted_nodes
            edges += extracted_edges
    return nodes, edges


def convert_to_numbered_ids(nodes, edges):
    name_to_number = {}
    new_nodes = []
    new_edges = []

    number = 1
    for node in nodes:
        node_id = node["id"]
        name_to_number[node_id] = str(number)
        node["id"] = str(number)
        new_nodes.append(node)
        number += 1

    for edge in edges:
        source_id = edge["source"]
        target_id = edge["target"]
        edge_id = f"{source_id}->{target_id}"

        if source_id in name_to_number:
            edge["source"] = name_to_number[source_id]
        if target_id in name_to_number:
            edge["target"] = name_to_number[target_id]

        new_edges.append(edge)

    return new_nodes, new_edges


def main():
    nodes = []
    project_name, place_path, current_dir = get_project_infos()
    nodes += extract_classes_with_parent(current_dir)

    new_nodes, edges = extract_data_from_pipelines(current_dir, place_path)

    nodes.extend(new_nodes)

    new_nodes, new_edges = convert_to_numbered_ids(nodes, edges)

    # create folder
    viz_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'visualization', 'server'))

    destination_folder = os.path.join(current_dir, "visualization")

    if os.path.exists(destination_folder) and os.path.isdir(destination_folder):
        shutil.rmtree(destination_folder)

    if os.path.exists(viz_folder) and os.path.isdir(viz_folder):
        shutil.copytree(viz_folder, destination_folder)

    with open("visualization/dist/viz-data.json", "w") as f:
        f.write(json.dumps({"nodes": new_nodes, "edges": new_edges}, indent=4))

    os.chdir(destination_folder)
    subprocess.Popen([sys.executable, 'server.py'])


if __name__ == "__main__":
    main()
