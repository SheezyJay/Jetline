import click
import os
import shutil
import toml
from pathlib import Path
from colorama import Fore, Style

@click.command()
@click.option('--project-name', prompt=f'{Fore.CYAN}? Project name:{Style.RESET_ALL}', default="project", help='Name of the project')
@click.option('--pipeline-name', prompt=f'{Fore.CYAN}? Pipeline folder name:{Style.RESET_ALL}', default='pipelines', help='Name of the pipeline Folder')
def installer(project_name, pipeline_name):
    # Bestimme den Pfad des Projektverzeichnisses
    project_folder = os.path.abspath(project_name)

    # Erstelle das Projektverzeichnis
    os.makedirs(project_folder, exist_ok=True)

    click.echo(click.style("\n🚀 Setting up your project...", fg='cyan', bold=True))

    # Erstelle die project.toml-Datei
    project_toml = {
        'project': {
            'name': project_name,
            'place': pipeline_name,
        },
        'locations': {
            'pipeline_folder': os.path.join(project_folder, pipeline_name),
            'main_file': os.path.join(project_folder, 'main.py'),
            'data_file': os.path.join(project_folder, 'data.py')
        }
    }

    # Speichere die project.toml-Datei
    with open(os.path.join(project_folder, 'project.toml'), 'w') as f:
        toml.dump(project_toml, f)

    # Erstelle die __init__.py Datei im Projektverzeichnis
    init_file = os.path.join(project_folder, "__init__.py")
    Path(init_file).touch()

    # Bestimme den Pfad des Vorlagenordners (templates folder)
    templates_folder = os.path.join(os.path.dirname(__file__), '..', 'templates')

    # Kopiere die Datei main.py aus dem Vorlagenordner in das Projektverzeichnis
    shutil.copy(os.path.join(templates_folder, 'main.py'), project_folder)

    # Erstelle einen neuen Ordner mit dem Namen pipeline_name im Projektverzeichnis
    pipeline_folder = os.path.join(project_folder, pipeline_name)
    os.makedirs(pipeline_folder, exist_ok=True)

    # create data folder
    shutil.copy(os.path.join(templates_folder, 'data.py'), project_folder)

    # Gehe in den Pipelinenordner und erstelle einen Unterordner "example_pipeline"
    example_pipeline_folder = os.path.join(pipeline_folder, 'example_pipeline')
    os.makedirs(example_pipeline_folder, exist_ok=True)

    # Erstelle die __init__.py Datei im Unterordner "example_pipeline"
    init_file_example = os.path.join(example_pipeline_folder, "__init__.py")
    Path(init_file_example).touch()

    # Kopiere die Dateien pipeline.py und example_node.py in den Unterordner "example_pipeline"
    shutil.copy(os.path.join(templates_folder, 'pipeline.py'), example_pipeline_folder)
    def replace_text_in_file(file_path, old_text, new_text):
        with open(file_path, 'r') as file:
            file_content = file.read()
        
        file_content = file_content.replace(old_text, new_text)
        
        with open(file_path, 'w') as file:
            file.write(file_content)

    # Ersetze __PIPELINE__ durch example_pipeline
    replace_text_in_file(os.path.join(example_pipeline_folder, 'pipeline.py'), '__PIPE__', 'example_pipeline')

    shutil.copy(os.path.join(templates_folder, 'nodes.py'), example_pipeline_folder)
    

    click.echo(click.style("✅ Project setup complete at ", fg='green', bold=True) + click.style(project_folder, fg='white'))

    click.echo(click.style(f"\nRun {Fore.YELLOW}cd {project_name}{Style.RESET_ALL} to navigate to the project directory.", fg='cyan'))

def main():
    click.echo(f"\n{Fore.BLUE}░▀▀█░█▀▀░▀█▀░█░░░▀█▀░█▀█░█▀▀{Style.RESET_ALL}")
    click.echo(f"{Fore.BLUE}░░░█░█▀▀░░█░░█░░░░█░░█░█░█▀▀{Style.RESET_ALL}")
    click.echo(f"{Fore.BLUE}░▀▀░░▀▀▀░░▀░░▀▀▀░▀▀▀░▀░▀░▀▀▀{Style.RESET_ALL}")
    
    click.echo(f"\n... a powerful, lightweight pipeline builder! by {Fore.GREEN}Kdc-Solutions{Style.RESET_ALL}\n")
    click.echo(f"\033[90;4mInstallation Guide:\033[0m")
    installer()
if __name__ == '__main__':
    main()

