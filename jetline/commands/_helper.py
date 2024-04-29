import re
import os
import click
import toml
from colorama import Fore, Style
def echo_jetline():

    click.echo(f"\n")
    click.echo(f"{Fore.BLUE}░▀▀█░█▀▀░▀█▀░█░░░▀█▀░█▀█░█▀▀{Style.RESET_ALL}")
    click.echo(f"{Fore.BLUE}░░░█░█▀▀░░█░░█░░░░█░░█░█░█▀▀{Style.RESET_ALL}")
    click.echo(f"{Fore.BLUE}░▀▀░░▀▀▀░░▀░░▀▀▀░▀▀▀░▀░▀░▀▀▀{Style.RESET_ALL}")
    click.echo(f"\n... a powerful, lightweight pipeline builder! by {Fore.GREEN}Kdc-Solutions{Style.RESET_ALL}\n")
    
    
def get_project_infos():
    """Fetches the project name and path based on project settings in a TOML file."""
    current_dir = os.getcwd()
    toml_file_path = os.path.join(current_dir, "project.toml")

    try:
        with open(toml_file_path, "r") as file:
            toml_data = toml.load(file)
            project_name = toml_data.get("project", {}).get("name")
            place = toml_data.get("project", {}).get("place")
            if not project_name or not place:
                return None, None
            place_path = os.path.join(current_dir, place)
            return project_name, place_path, current_dir
    except Exception:
        raise ValueError("Project name or place is missing in the TOML file.")


def extract_pipeline_order(current_directory):
    """
    Extracts the PIPELINE_ORDER list from the content of the main file.

    :param current_directory: The directory of the main file.
    :return: The extracted PIPELINE_ORDER list or None if not found.
    """
    main_path = os.path.join(current_directory, 'main.py')
    with open(main_path, 'r') as file:
        main_content = file.read()

    pipeline_order_match = re.search(r'PIPELINE_ORDER\s*=\s*\[([^\]]+)\]', main_content)
    if pipeline_order_match:
        return pipeline_order_match.group(1).replace("'", "").replace('"', "").split(',')
    return None
