import click
import os
from pathlib import Path
from colorama import Fore, Style
import shutil
import toml

def update_pipeline_order(pipeline_name):
    """
    Update the PIPELINE_ORDER list in the main.py file with the given pipeline name.

    Args:
        pipeline_name (str): The name of the pipeline to be added to the PIPELINE_ORDER list.
    """
    current_directory = os.getcwd()
    main_py_path = os.path.join(current_directory, 'main.py')
    print(main_py_path)
    if not os.path.exists(main_py_path):
        click.echo(f"{Fore.RED}main.py file not found in the current directory.{Style.RESET_ALL}")
        return

    pipeline_found = False  # Variable to track if PIPELINE_ORDER was found

    try:
        with open(main_py_path, 'r') as f:
            lines = f.readlines()

        for i, line in enumerate(lines):

            if 'PIPELINE_ORDER' in line:
                start_index = line.find('[')
                end_index = line.rfind(']')
                pipeline_order = line[start_index+1:end_index]
                pipeline_order = [element.strip() for element in pipeline_order.split(',') if element.strip()]
                pipeline_order.append(f'"{pipeline_name}"')

                for j in range(len(pipeline_order) - 1):
                    if not pipeline_order[j].endswith('"') and not pipeline_order[j+1].startswith('"'):
                        pipeline_order[j] += ','

                new_line = f'        PIPELINE_ORDER = [{", ".join(pipeline_order)}] if pipes is None else pipes.split(\',\')\n'
                lines[i] = new_line
                pipeline_found = True  # Set to True when PIPELINE_ORDER is found
                break

        # Check if PIPELINE_ORDER was not found
        if not pipeline_found:
            raise ValueError('PIPELINE_ORDER must be set in main.py and a valid list with "" separation')

        with open(main_py_path, 'w') as f:
            f.writelines(lines)

        click.echo(f"{Fore.GREEN}PIPELINE_ORDER updated successfully.{Style.RESET_ALL}")

    except Exception as e:
        click.echo(f"{Fore.RED}Error updating PIPELINE_ORDER: {e}{Style.RESET_ALL}")


@click.command()
@click.option('--pipeline-name', prompt=f'{Fore.YELLOW}Please enter the pipeline name{Style.RESET_ALL}',help='Name of the project')
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

    update_pipeline_order(pipeline_name)

    click.echo(f"{Fore.GREEN}New pipeline '{pipeline_name}' created successfully.{Style.RESET_ALL}")


if __name__ == '__main__':
    main()
