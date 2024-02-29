import click
import os
import shutil
import toml
from pathlib import Path

@click.command()
@click.option('--project-name', prompt='Please enter the project name (optional)', default="project", help='Name of the project')
@click.option('--pipeline-name', prompt='Please enter the pipeline name (optional)', default='pipelines', help='Name of the pipeline Folder')
def setup_project(project_name, pipeline_name):
    # Bestimme den Pfad des Projektverzeichnisses
    project_folder = os.path.abspath(project_name)

    # Erstelle das Projektverzeichnis
    os.makedirs(project_folder, exist_ok=True)

    # Erstelle die project.toml-Datei
    project_toml = {
        'project': {
            'name': project_name,
            'place': pipeline_name,
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
    shutil.copy(os.path.join(templates_folder, 'example_node.py'), example_pipeline_folder)

    # Bestimme den Pfad des Quellordners (source folder)
    source_folder = os.path.join(os.path.dirname(__file__), '..', 'source')

    # Kopiere den Quellordner (source folder) in das Projektverzeichnis
    if os.path.exists(source_folder):
        shutil.copytree(source_folder, os.path.join(project_folder, os.path.basename(source_folder)))

    click.echo(f"Project setup complete. Project directory created: {project_folder}")

if __name__ == '__main__':
    setup_project()
