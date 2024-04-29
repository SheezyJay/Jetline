import click
import os
import sys


def run_pipeline(pipeline_name=None):
    """
    Runs a pipeline specified by the given pipeline name.

    Parameters:
        pipeline_name (str): The name of the pipeline to run. Default is None.

    """
    current_directory = os.getcwd()
    sys.path.insert(0, current_directory)

    try:
        from main import run_pipelines
        run_pipelines()
    except ImportError as e:
        click.secho(f"Failed to import 'main.py'. Error: {e}", fg='red')
    finally:
        sys.path.remove(current_directory)


@click.command()
def main():
    """
    Run a pipeline or all pipelines if pipeline_name is None. This is a command line tool to run a pipeline or all pipelines in the current directory.

    """
    main_file = "main.py"
    current_directory = os.getcwd()
    main_path = os.path.join(current_directory, main_file)

    if os.path.isfile(main_path):

        click.secho("Directory successfully located. Running all pipelines...", fg='blue')
        run_pipeline()
    else:
        click.secho(f"{main_file} not found in the current directory.", fg='red')


if __name__ == "__main__":
    main()
