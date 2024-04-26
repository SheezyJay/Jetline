import importlib.util
from pathlib import Path
import toml
import inspect
from jetline.data.data import DataManager
from jetline.logging import logger
import os
import sys


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
        Runs the execute method of each node in the self.nodes dictionary
        and stores the output in the self.outputs dictionary.
        """
        for node_name, node in self.nodes.items():
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

    @staticmethod
    def get_caller_path():
        """
        Description:
        This method returns the path of the file that called it.

        Parameters:
        - self: The instance of the calling class. This is an implicit parameter and does not need to be provided explicitly.

        Returns:
        - module_path: The path of the file that called the method.


        Example Usage:
        instance = MyClass()
        path = instance.get_caller_path()

        """
        frame = inspect.stack()[2]
        module = inspect.getmodule(frame[0])
        if module is not None:
            module_path = Path(module.__file__).parent
        else:
            module_path = Path.cwd()
        return module_path

    def add_project_directory_to_sys_path(self):
        """

        Add the project directory to the system path.

        This method is used to add the project directory to the sys.path list in order to make modules and packages from the project directory importable.

        """
        toml_file_path = os.path.join(self.caller_path, 'project.toml')

        with open(toml_file_path, 'r') as f:
            toml_data = toml.load(f)
            place = toml_data.get('project', {}).get('place')

        if not place:
            raise FileNotFoundError('The project.toml file was not found in the directory. Hint: run cd to your project')

        target_directory = os.path.join(self.caller_path, place)

        sys.path.append(target_directory)

    def load_pipelines(self):
        """
        Load pipelines from project.toml file and add them to the pipelines dictionary.

        Args:
            self: The instance of the class calling the method.

        Returns:
            None

        Raises:
            ValueError: If the register function in the pipeline module does not return a Pipeline instance.

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

                            pipeline_definition = pipeline_register_function(self.data_manager)
                            if isinstance(pipeline_definition, Pipeline):
                                self.pipelines[pipeline_name] = pipeline_definition
                            else:
                                raise ValueError(
                                    f"The register function in {pipeline_module_path} must return a Pipeline instance.")

    def run(self, pipeline_order):
        """
        Run method to execute pipelines in a specific order.

        Parameters:
        - self: The object instance.
        - pipeline_order (list): The order in which the pipelines should be executed.

        Returns:
        - results (dict): A dictionary with the results of each pipeline execution.

        Raises:
        - ValueError: If any of the pipelines in the specified order are not found.

        Example usage:
            pipeline_order = ['pipeline1', 'pipeline2', 'pipeline3']
            results = obj.run(pipeline_order)
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
