import os
import toml
import re
import ast

def _get_project_infos():
    proj = toml.load("project.toml")["project"]
    return proj["name"], os.path.join(os.getcwd(), proj["place"]), os.getcwd()


def _extract_pipeline_order(current_directory):
    """
    Extracts the PIPELINE_ORDER list from the main file.

    :param current_directory: Directory of the main file.
    :return: Extracted PIPELINE_ORDER list or None if not found.
    """
    with open(os.path.join(current_directory, 'main.py'), 'r') as file:
        main_content = file.read()

    pipeline_order_match = re.search(r'PIPELINE_ORDER\s*=\s*\[([^\]]+)\]', main_content)
    return pipeline_order_match.group(1).replace("'", "").replace('"', "").split(',') if pipeline_order_match else None


def extract_data_classes_info(main_root, nID):

    data_file_path = os.path.join(main_root, "data.py")
    x_position = -100
    result = []
    for node in ast.parse(open(data_file_path, 'r').read(), filename=data_file_path).body:
        if isinstance(node, ast.ClassDef):
            nID += 1
            result.append({
                "id": f'{nID}',
                "type": "default",
                "data": {
                    
                    "title": re.search(r"name\s*=\s*'([^']*)'", ast.unparse(node)).group(1),
                    "type": "data",
                    "description": ast.get_docstring(node) or "",
                    "code": ast.unparse(node)
                },
                "position": {"x": (x_position := x_position + 200), "y": 0}
            })
    return result, nID





class NodeExtractor:
    
    def __init__(self, pipe_order, pipe_root, nID=1) -> None:
        self.pipe_order = pipe_order
        self.pipe_root = pipe_root
        self.nID = nID
    def extract_register_function(self,folder_path):
        pipeline_file_path = os.path.join(folder_path, "pipeline.py")

        if os.path.exists(pipeline_file_path):
            with open(pipeline_file_path, "r") as f:
                lines = f.read()
                start = lines.find("def register(")
                if start != -1:
                    end = lines.find("\n\n", start)
                    if end == -1:
                        end = len(lines)
                    return lines[start:end].strip()

        return None
    
    def _get_pipeline_folders(self,pipe_order,pipe_root):
        """
        Retrieves the folders in pipeline order based on PIPELINE_ORDER from the main file.

        :param pipe_root: Root directory of the pipeline folders.
        :return: Sorted list of folders based on PIPELINE_ORDER.
        """
        if pipe_order:
            pipeline_folders = [folder for folder in os.listdir(pipe_root) if os.path.isdir(os.path.join(pipe_root, folder))]
            return sorted(pipeline_folders, key=lambda x: pipe_order.index(x) if x in pipe_order else len(pipe_order))
        return []
   
    
    def get_node_info(self, node_def):
        """"""
        nID = self.nID
        self.nID += 1
        return {"id": nID, "data": {"title": node_def.name, "type": "function", "code": ast.unparse(node_def), "description": ast.get_docstring(node_def) or '', "inputs": "", "outputs": "", "stream": ""}}
    def extract_functions_from_register(self, register_function):
        """Extract functions, inputs, outputs from a given register function."""

        functions = re.findall(r'function=([a-zA-Z0-9_.-]+)', register_function)
        inputs = re.findall(r'inputs=\[(.*?)\]', register_function)
        outputs = re.findall(r'outputs=\[(.*?)\]', register_function)
        return functions, inputs, outputs
    
    def format_node_parameters(self,param):
        """Format given node parameter by removing unnecessary characters and splitting by comma."""

        formatted = param.replace('"', '').replace("'", "").replace(" ", "")
        return formatted.split(',')
    
    def extract_node_infos(self):
        
        for folder in self._get_pipeline_folders(pipe_order, pipe_root):
            folder_path = os.path.join(pipe_root, folder)
            function_names, inputs, outputs = self.extract_functions_from_register(self.extract_register_function(folder_path))
            nodes_dict = {}
            node_file_path = os.path.join(folder_path, "nodes.py")
            if os.path.exists(node_file_path):
                with open(node_file_path, "r") as file:
                    tree = ast.parse(file.read(), filename=node_file_path)
                    for node_def in tree.body:
                        if isinstance(node_def, ast.FunctionDef):
                            nodes_dict[node_def.name] = self.get_node_info(node_def)

                    sorted_nodes = []
                    for func_name in function_names:
                        node_name = func_name.split('.')[-1]
                        if node_name in nodes_dict:
                            node_info = nodes_dict[node_name]
                            i = len(sorted_nodes)
                            if i < len(inputs): node_info["data"]["inputs"] = self.format_node_parameters(inputs[i])
                            if i < len(outputs): node_info["data"]["outputs"] = self.format_node_parameters(outputs[i])
                            node_info["data"]["stream"] = ["input", "output"] if node_info["data"]["inputs"] and node_info["data"]["outputs"] else ["input"] if node_info["data"]["inputs"] else ["output"] if node_info["data"]["outputs"] else []
                            sorted_nodes.append(node_info)
                    return sorted_nodes
            return []
        
    pass






nID = 0
pipe_data = {
        "nodes": [],
        "edges": [],
    }


proj_name,pipe_root,main_root = _get_project_infos()


pipe_order = _extract_pipeline_order(main_root)


# data classes
nodes, nID = extract_data_classes_info(main_root, nID)
pipe_data["nodes"].extend(nodes)



#register functions
node_extractor = NodeExtractor(pipe_order,pipe_root, nID)
node_infos = node_extractor.extract_node_infos()

print(node_infos)
    
    
    
    
    
# no
import json
json_file_path = os.path.join(main_root, "viz-data.json")
with open(json_file_path, "w") as json_file:
        json.dump(node_infos, json_file, indent=4)