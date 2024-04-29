import click
import os
from pathlib import Path
from colorama import Fore, Style
import shutil
import toml


@click.command()
@click.option('--pipeline-name', prompt=f'{Fore.YELLOW}Please enter the pipeline name{Style.RESET_ALL}',
              help='Name of the project')
def main(pipeline_name):
    """
    Create a new pipeline with the given name.

    Args:
        pipeline_name (str): The name of the pipeline to be created.
    """
    current_directory = os.getcwd()
    toml_path = os.path.join(current_directory, 'project.toml')
    if not os.path.exists(toml_path):
        click.echo(f"{Fore.RED}project.toml file not found in the current directory.{Style.RESET_ALL}")
        return

    with open(toml_path, 'r') as f:
        project_config = toml.load(f)
        pipeline_folder = project_config['project']['place']

    pipeline_folder = os.path.join(current_directory, pipeline_folder, pipeline_name)
    if os.path.exists(pipeline_folder):
        click.echo(f"{Fore.RED}Pipeline '{pipeline_name}' already exists.{Style.RESET_ALL}")
        return

    os.makedirs(pipeline_folder)
    init_file = os.path.join(pipeline_folder, "__init__.py")
    Path(init_file).touch()

    templates_folder = os.path.join(os.path.dirname(__file__), '..', 'templates')

    # Copy pipeline.py from the template folder to the pipeline folder
    pipeline_py_path = os.path.join(pipeline_folder, 'pipeline.py')
    shutil.copy(os.path.join(templates_folder, 'pipeline.py'), pipeline_py_path)

    # Replace __PIPE__ with the actual pipeline name in pipeline.py
    with open(pipeline_py_path, 'r') as f:
        pipeline_content = f.read()

    new_content = pipeline_content.replace('__PIPE__', pipeline_name)

    with open(pipeline_py_path, 'w') as f:
        f.write(new_content)

    # Copy nodes.py from the template folder to the pipeline folder
    shutil.copy(os.path.join(templates_folder, 'nodes.py'), pipeline_folder)

    click.echo(f"{Fore.GREEN}New pipeline '{pipeline_name}' created successfully.{Style.RESET_ALL}")


if __name__ == '__main__':
    main()
