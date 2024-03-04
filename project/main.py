from jetline.pipeline.pipeline import PipelineManager
import sys


def run_pipelines(pipes=None):
    """
     Run a pipeline or all pipelines if pipeline_name is None. This is a command line tool to run a pipeline or all pipelines in the current directory.

     Args:
        pipes: Name of the pipeline to run or None
    """
    try:
        # Initialize the PipelineManager
        pipeline_manager = PipelineManager()

        # Define the order of pipelines by folder name
        PIPELINE_ORDER = ["example_pipeline"] if pipes is None else pipes.split(',')

        # Execute pipelines
        pipeline_manager.run(PIPELINE_ORDER)

    except Exception as e:
        print(f"Error running pipelines: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_pipelines()
