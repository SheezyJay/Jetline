from jetline.pipeline.pipeline import PipelineManager
from jetline.logging import logger
import sys

def run_pipelines(pipes=None):
    """
    Load and execute pipelines defined in the pipeline folder.
    """
    try:
        # Initialize the PipelineManager
        pipeline_manager = PipelineManager()

        # Define the order of pipelines by folder name
        PIPELINE_ORDER = ["example_pipeline"] if pipes is None else pipes.split(',')

        # Execute pipelines
        pipeline_manager.run(PIPELINE_ORDER)

    except Exception as e:
        raise RuntimeError(f"Error running pipelines: {e}") from e

if __name__ == "__main__":
    run_pipelines()
