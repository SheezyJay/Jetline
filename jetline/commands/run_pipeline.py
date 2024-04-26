import os
import click
import sys


@click.command()
@click.argument('pipeline_name', default=None, required=False)
def main(pipeline_name):
    """
    Run a pipeline or all pipelines if pipeline_name is None. This is a command line tool to run a pipeline or all pipelines in the current directory.

    Args:
        pipeline_name: Name of the pipeline to run or None
    """
    main_file = "main.py"
    current_directory = os.getcwd()
    main_path = os.path.join(current_directory, main_file)

    if os.path.isfile(main_path):
        if pipeline_name is not None:
            click.secho(f"Directory successfully located. Running pipeline(s) '{pipeline_name}'...", fg='green')
            os.system(f'{sys.executable} -c "from main import run_pipelines; run_pipelines(\'{pipeline_name}\')"')
        else:
            click.secho("Directory successfully located. Running Pipelines...", fg='green')
            os.system(f'{sys.executable} -c "from main import run_pipelines; run_pipelines()"')
    else:
        click.secho(f"{main_file} not found in the current directory.", fg='red')


if __name__ == "__main__":
    main()
