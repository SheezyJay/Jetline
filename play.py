
from Base import PipelineManager
# Beispiel für die Verwendung
manager = PipelineManager()
manager.load_pipelines()

# Definiere die Reihenfolge der Pipelines, in der sie ausgeführt werden sollen
pipeline_order = ["asd","asd copy"]

results = manager.run_pipelines_in_order(pipeline_order)
for pipeline_name, result in results.items():
    print(f"Results for pipeline '{pipeline_name}': {result}")
