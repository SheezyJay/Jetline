import click
from colorama import Fore, Style

@click.command()
def main():
    """
    Print information about jetline.
    """
    click.echo(f"{Fore.BLUE}What is jetline?{Style.RESET_ALL}")
    click.echo("jetline is a powerful, lightweight pipeline builder designed to simplify the creation and management of data processing pipelines.")
    click.echo("\n")

    click.echo(f"{Fore.BLUE}What can you do with jetline?{Style.RESET_ALL}")
    click.echo("With jetline, you can define, organize, and execute complex data processing workflows with ease.")
    click.echo("\n")

    click.echo(f"{Fore.BLUE}Documentation:{Style.RESET_ALL}")
    click.echo("For more information and detailed documentation, visit:")
    click.echo("https://jetline.readthedocs.io/en/latest/")
    click.echo("\n")

    click.echo(f"{Fore.BLUE}GitHub Repository:{Style.RESET_ALL}")
    click.echo("Find the jetline source code and contribute on GitHub:")
    click.echo("https://github.com/yourusername/jetline")
    click.echo("\n")

    click.echo(f"{Fore.BLUE}PyPI Package:{Style.RESET_ALL}")
    click.echo("jetline is available as a Python package on PyPI. Install it via pip:")
    click.echo("pip install jetline")
    click.echo("\n")


    click.echo(f"{Fore.BLUE}Welcome to jetline!{Style.RESET_ALL}")
    click.echo("This command will guide you through setting up a new jetline project.")
    click.echo("It will create the necessary project structure and files.")
    click.echo("\n")
    click.echo("To set up the project, run the following commands:")
    click.echo("1. jetline-setup")
    click.echo("2. Follow the prompts to provide project details.")
    click.echo("\n")

    click.echo(f"{Fore.BLUE}Creating a new pipeline!{Style.RESET_ALL}")
    click.echo("This command will create a new pipeline in your jetline project.")
    click.echo("It will set up the necessary files and configurations.")
    click.echo("\n")
    click.echo("To create a new pipeline, run the following command:")
    click.echo("jetline-new-pipe")
    click.echo("\n")


if __name__ == '__main__':
    main()