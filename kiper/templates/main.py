from kiper.pipeline.pipeline import PipelineManager

# initialize pipeline
manager = PipelineManager()
manager.load_pipelines()

# Define order for the piplines by foldername
pipeline_order = ["example_pipeline",]

results = manager.run(pipeline_order)
for pipeline_name, result in results.items():
    print(f"Results for pipeline '{pipeline_name}': {result}")
