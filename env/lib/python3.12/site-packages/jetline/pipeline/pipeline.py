import importlib.util
from pathlib import Path
import toml
from .node import Node
import inspect
from jetline.data.data import DataManager
from jetline.logging import logger
import os, sys

from jetline.pipeline.node import Node

class Pipeline:
    def __init__(self, nodes=None, data_manager=None):
        """
        Initialize the Pipeline with a list of nodes and a data manager.
        """
        self.nodes = {node.name: node for node in nodes} if nodes else {}
        self.data_manager = data_manager
        self.outputs = {}

    def run(self):
        """
        Führt alle Nodes in der Pipeline aus und sammelt Outputs.
        """
        for node_name, node in self.nodes.items():
            # Übergeben des DataManager an die execute-Methode
            self.outputs[node_name] = node.execute(self.data_manager)

    def add_node(self, node):
        """
        Add a single node to the pipeline.
        """
        if node.name in self.nodes:
            raise ValueError(f"Node with name '{node.name}' already exists.")
        self.nodes[node.name] = node

class PipelineManager:
    def __init__(self):
        """
        Initialize the pipeline manager.
        """
        self.caller_path = self.get_caller_path()
        self.add_project_directory_to_sys_path()
        self.data_manager = DataManager(caller_path=self.caller_path)
        self.pipelines = {}
        self.load_pipelines()
       

    def get_caller_path(self):
        """
        Ermittelt den Pfad des Skripts, das diesen DataManager instanziiert.
        """
        frame = inspect.stack()[2]
        module = inspect.getmodule(frame[0])
        if module is not None:
            module_path = Path(module.__file__).parent
        else:
            module_path = Path.cwd()  
        return module_path
    
    def add_project_directory_to_sys_path(self):
        """Fügt das Projektverzeichnis zum sys.path hinzu."""
       
        toml_file_path = os.path.join(self.caller_path, 'project.toml')

        with open(toml_file_path, 'r') as f:
            toml_data = toml.load(f)
            place = toml_data.get('project', {}).get('place')

        if not place:
            print("Fehler: 'place' nicht gefunden in der project.toml-Datei.")
            sys.exit(1)

        target_directory = os.path.join(self.caller_path, place)

        sys.path.append(target_directory)
    

    def load_pipelines(self):
        """
        Load Pipelines from project.toml and create modules.
        """
        base_path = self.caller_path

        project_toml_path = base_path / "project.toml"
        with open(project_toml_path, "r") as f:
            project_config = toml.load(f)
            pipeline_folder_name = project_config["project"]["place"]
            pipeline_folder = base_path / pipeline_folder_name
        
            for pipeline_name in pipeline_folder.iterdir():
                if pipeline_name.is_dir():
                    pipeline_name = pipeline_name.name
                    pipeline_module_path = pipeline_folder / pipeline_name / "pipeline.py"
                    if pipeline_module_path.exists():
                        spec = importlib.util.spec_from_file_location("pipeline_module", pipeline_module_path)
                        pipeline_module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(pipeline_module)
                        pipeline_register_function = getattr(pipeline_module, "register", None)
                        if callable(pipeline_register_function):
                            # Übergeben Sie den data_manager-Parameter an die register-Funktion
                            pipeline_definition = pipeline_register_function(self.data_manager)
                            if isinstance(pipeline_definition, Pipeline):
                                self.pipelines[pipeline_name] = pipeline_definition
                            else:
                                raise ValueError(f"The register function in {pipeline_module_path} must return a Pipeline instance.")

    def run(self, pipeline_order):
        """
        Run a list of pipelines in the order they were added.
        """
        results = {}
        
        missing_pipelines = [pipeline_name for pipeline_name in pipeline_order if pipeline_name not in self.pipelines]
        if missing_pipelines:
            error_message = f"Error running pipelines: The following pipelines were not found: {', '.join(missing_pipelines)}"
            logger.error(error_message)
            raise ValueError(error_message)
        
        for pipeline_name in pipeline_order:
            pipeline = self.pipelines[pipeline_name]
            results[pipeline_name] = pipeline.run()
            logger.info(f"Pipeline '{pipeline_name}' executed successfully.")
        
        logger.info("All Pipelines ran successfully.")
        return results
