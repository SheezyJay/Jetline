from jetline.pipeline.pipeline import PipelineManager


def run_pipelines():
    """Run administrative tasks."""
    try:
        pipeline_manager = PipelineManager()

        # Define the order of pipelines by folder name
        #   [["example_pipeline"], ["example_pipeline2"]] to run after
        #   [["example_pipeline", "example_pipeline2"]] to run at the same time
        #   [["example_pipeline", "example_pipeline2"], ["example_pipeline3"]] combination
        PIPELINE_ORDER = [['raw']]

        pipeline_manager.run(PIPELINE_ORDER)
    except Exception as e:
        raise RuntimeError(f"Error running pipelines: {e}") from e


if __name__ == "__main__":
    run_pipelines()
