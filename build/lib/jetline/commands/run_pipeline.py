import click
import os
import subprocess

@click.command()
@click.argument('pipeline_name', default=None, required=False)
def main(pipeline_name):
    main_file = "main.py"
    current_directory = os.getcwd()
    main_path = os.path.join(current_directory, main_file)
    
    if os.path.isfile(main_path):
        if pipeline_name is not None:
            click.secho(f"Directory successfully located. Running pipeline(s) '{pipeline_name}'...", fg='green')
        else:
            click.secho("Directory successfully located. Running Pipelines...", fg='green')
        
        subprocess.run(["python", main_path] + ([pipeline_name] if pipeline_name is not None else []))
    else:
        click.secho(f"{main_file} not found in the current directory.", fg='red')

if __name__ == "__main__":
    main()
