import re
import os
import click
from colorama import Fore, Style
def echo_jetline():

    click.echo(f"\n")
    click.echo(f"{Fore.BLUE}░▀▀█░█▀▀░▀█▀░█░░░▀█▀░█▀█░█▀▀{Style.RESET_ALL}")
    click.echo(f"{Fore.BLUE}░░░█░█▀▀░░█░░█░░░░█░░█░█░█▀▀{Style.RESET_ALL}")
    click.echo(f"{Fore.BLUE}░▀▀░░▀▀▀░░▀░░▀▀▀░▀▀▀░▀░▀░▀▀▀{Style.RESET_ALL}")
    click.echo(f"\n... a powerful, lightweight pipeline builder! by {Fore.GREEN}Kdc-Solutions{Style.RESET_ALL}\n")
def _extract_pipeline_order(current_directory):
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
