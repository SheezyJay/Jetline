import click
import os
import shutil
import toml
from pathlib import Path
from colorama import Fore, Style
from jetline.commands._helper import echo_jetline
@click.command()
@click.option('--project-name', prompt=f'{Fore.CYAN}? Project name:{Style.RESET_ALL}', default="project", help='Name of the project')
@click.option('--pipeline-name', prompt=f'{Fore.CYAN}? Pipeline folder name:{Style.RESET_ALL}', default='pipelines', help='Name of the pipeline Folder')
def installer(project_name, pipeline_name):
    project_folder = os.path.abspath(project_name)
    os.makedirs(project_folder, exist_ok=True)

    click.echo(click.style("\n🚀 Setting up your project...", fg='cyan', bold=True))

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


    with open(os.path.join(project_folder, 'project.toml'), 'w') as f:
        toml.dump(project_toml, f)


    init_file = os.path.join(project_folder, "__init__.py")
    Path(init_file).touch()


    templates_folder = os.path.join(os.path.dirname(__file__), '..', 'templates')


    shutil.copy(os.path.join(templates_folder, 'main.py'), project_folder)

    pipeline_folder = os.path.join(project_folder, pipeline_name)
    os.makedirs(pipeline_folder, exist_ok=True)

    shutil.copy(os.path.join(templates_folder, 'data.py'), project_folder)

    example_pipeline_folder = os.path.join(pipeline_folder, 'example_pipeline')
    os.makedirs(example_pipeline_folder, exist_ok=True)

    init_file_example = os.path.join(example_pipeline_folder, "__init__.py")
    Path(init_file_example).touch()

    shutil.copy(os.path.join(templates_folder, 'pipeline.py'), example_pipeline_folder)
    def replace_text_in_file(file_path, old_text, new_text):
        with open(file_path, 'r') as file:
            file_content = file.read()
        
        file_content = file_content.replace(old_text, new_text)
        
        with open(file_path, 'w') as file:
            file.write(file_content)

    replace_text_in_file(os.path.join(example_pipeline_folder, 'pipeline.py'), '__PIPE__', 'example_pipeline')

    shutil.copy(os.path.join(templates_folder, 'nodes.py'), example_pipeline_folder)
    

    click.echo(click.style("✅ Project setup complete at ", fg='green', bold=True) + click.style(project_folder, fg='white'))

    click.echo(click.style(f"\nRun {Fore.YELLOW}cd {project_name}{Style.RESET_ALL} to navigate to the project directory.", fg='cyan'))

def main():
    echo_jetline()
    click.echo(f"\033[90;4mInstallation Guide:\033[0m")
    installer()
if __name__ == '__main__':
    main()

