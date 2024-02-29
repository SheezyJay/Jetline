import os
import importlib.util
from pathlib import Path
import toml

class Node:
    def __init__(self, name, function, inputs):
        self.name = name
        self.function = function
        self.inputs = inputs

    def execute(self):
        return self.function(*self.inputs)

class Pipeline:
    def __init__(self, requires=None):
        self.nodes = {}
        self.requires = requires or ""

    def run(self):
        outputs = {}
        for node_name, node in self.nodes.items():
            outputs[node_name] = node.execute()
        return outputs

    def add_node(self, name, func, inputs):
        self.nodes[name] = Node(name, func, inputs)

    def register(self, pipeline_instance):
        for required_pipeline in pipeline_instance.requires:
            if required_pipeline not in self.nodes:
                raise ValueError(f"Pipeline '{required_pipeline}' ist erforderlich, wurde aber nicht gefunden.")
        self.nodes.update(pipeline_instance.nodes)


class PipelineManager:
    def __init__(self):
        self.pipelines = {}

    def load_pipelines(self):
        # Bestimme den Basispfad der ausführbaren Python-Datei
        base_path = Path(os.path.dirname(__file__))
        
        # Lade project.toml-Datei und extrahiere den Pfad und die Namen der Pipelines
        with open("project.toml", "r") as f:
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

    def run_pipelines_in_order(self, pipeline_order):
        results = {}
        for pipeline_name in pipeline_order:
            if pipeline_name in self.pipelines:
                pipeline = self.pipelines[pipeline_name]
                results[pipeline_name] = pipeline.run()
            else:
                raise ValueError(f"Pipeline '{pipeline_name}' not found.")

        return results