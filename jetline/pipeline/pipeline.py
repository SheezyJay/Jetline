import importlib.util
from pathlib import Path
import toml
from .node import Node
import inspect
from jetline.data.data import DataManager
from jetline.logging import logger

class Pipeline:
    def __init__(self):
        """
         Initialize the nodes dictionary. This is called by __init__ to initialize the node dictionary and its sub - classes
        """
        self.nodes = {}
      

    def run(self):
        """
         Run the nodes and return outputs. This is the entry point for the Node class. You can override this method to do something different
         
         
         Returns: 
         	 A dictionary of outputs keyed by
        """
        outputs = {}
        # Execute all nodes in the graph.
        for node_name, node in self.nodes.items():
            outputs[node_name] = node.execute()
        return outputs

    def add_node(self, name, func, inputs):
        """
         Add a node to the graph. This is a convenience method for creating a : class : ` Node ` and associating it with the graph.
         
         Args:
         	 name: The name of the node. It must be unique among all nodes in the graph.
         	 func: The function to run on the node. It must take a single argument : an instance of
         	 inputs: The inputs to the
        """
        self.nodes[name] = Node(name, func, inputs)

    def register(self, pipeline_instance):
        """
         Register a pipeline with the pipeline manager. This is a convenience method for the use of : meth : ` Pipeline. nodes `
         
         Args:
         	 pipeline_instance: An instance of : class : ` Pipeline
        """
        for pipline in pipeline_instance:
            if pipline not in self.nodes:
                raise ValueError(f"Pipeline '{pipline}' ist erforderlich, wurde aber nicht gefunden.")
        self.nodes.update(pipeline_instance.nodes)


class PipelineManager:
    def __init__(self):
        """
        Initialize the pipeline manager.
        """
        self.caller_path = self.get_caller_path()
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
        for pipeline_name in pipeline_order:
            if pipeline_name in self.pipelines:
                pipeline = self.pipelines[pipeline_name]
                results[pipeline_name] = pipeline.run()
                logger.info(f"Pipeline '{pipeline_name}' executed successfully.")
            else:
                logger.error(f"Pipeline '{pipeline_name}' not found.")
                raise ValueError(f"Pipeline '{pipeline_name}' not found.")
        logger.info("All Pipelines ran successfully.")
        return results