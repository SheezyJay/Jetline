import os
import importlib.util
from pathlib import Path
import toml
from .node import Node
import inspect

class Pipeline:
    def __init__(self):
        self.nodes = {}
      

    def run(self):
        outputs = {}
        for node_name, node in self.nodes.items():
            outputs[node_name] = node.execute()
        return outputs

    def add_node(self, name, func, inputs):
        self.nodes[name] = Node(name, func, inputs)

    def register(self, pipeline_instance):
        for pipline in pipeline_instance:
            if pipline not in self.nodes:
                raise ValueError(f"Pipeline '{pipline}' ist erforderlich, wurde aber nicht gefunden.")
        self.nodes.update(pipeline_instance.nodes)


class PipelineManager:
    def __init__(self):
        self.pipelines = {}

    def load_pipelines(self, base_path=None):
        if base_path is None: base_path = Path(os.path.dirname(os.path.abspath(inspect.stack()[1].filename)))

        # Lade project.toml-Datei und extrahiere den Pfad und die Namen der Pipelines
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
                            pipeline_definition = pipeline_register_function()
                            if isinstance(pipeline_definition, Pipeline):
                                self.pipelines[pipeline_name] = pipeline_definition
                            else:
                                raise ValueError(f"The register function in {pipeline_module_path} must return a Pipeline instance.")

    def run(self, pipeline_order):
        results = {}
        for pipeline_name in pipeline_order:
            if pipeline_name in self.pipelines:
                pipeline = self.pipelines[pipeline_name]
                results[pipeline_name] = pipeline.run()
            else:
                raise ValueError(f"Pipeline '{pipeline_name}' not found.")

        return results