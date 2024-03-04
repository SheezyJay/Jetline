import click
import os
import re
import vulture
import toml
def _read_main_file_content(main_path):
    """
    Liest den Inhalt der Hauptdatei (main.py).

    :param main_path: Der Pfad zur Hauptdatei.
    :return: Der Inhalt der Hauptdatei.
    """
    with open(main_path, 'r') as file:
        return file.read()


def _extract_pipeline_order(main_content):
    """
    Extrahiert die PIPELINE_ORDER-Liste aus dem Inhalt der Hauptdatei.

    :param main_content: Der Inhalt der Hauptdatei.
    :return: Die extrahierte PIPELINE_ORDER-Liste oder None, falls nicht gefunden.
    """
    pipeline_order_match = re.search(r'PIPELINE_ORDER\s*=\s*\[([^\]]+)\]', main_content)
    if pipeline_order_match:
        return pipeline_order_match.group(1).replace("'", "").replace('"', "").split(',')
    return None


def _find_folders(directory, folder_list):
    """
    Sucht nach Ordnern in einem Verzeichnis basierend auf einer Liste von Ordnernamen.

    :param directory: Das Verzeichnis, in dem nach den Ordnern gesucht werden soll.
    :param folder_list: Die Liste von Ordnernamen, nach denen gesucht werden soll.
    """
    for folder_name in folder_list:
        folder_path = os.path.join(directory, folder_name)
        if os.path.isdir(folder_path):
            click.echo(f"Ordner '{folder_name}' gefunden: {folder_path}")
        else:
            click.echo(f"Ordner '{folder_name}' nicht gefunden.")




def _extract_project_info(caller_path):
    """
    Extrahiert den Namen und den Ort (place) aus der project.toml-Datei.

    :param caller_path: Der Pfad des aufrufenden Verzeichnisses.
    :return: Ein Tupel (name, place) des extrahierten Projekts oder (None, None), falls nicht gefunden.
    """

    if os.path.exists(caller_path):
       
        with open(caller_path, 'r') as f:
            toml_data = toml.load(f)
            project_info = toml_data.get('project', {})
            place = project_info.get('place')
            name = project_info.get('name')
            return place, name
    return None, None


def _copy_nodes_content(folder_name, folder_path):
    """
    Kopiert den Inhalt der 'nodes.py'-Datei im angegebenen Ordner und fügt ihn in die 'exe.py'-Datei ein.

    :param folder_name: Der Name des Ordners, in dem 'nodes.py' gefunden wurde.
    :param folder_path: Der Pfad zum Ordner, in dem 'nodes.py' gefunden wurde.
    """
    nodes_file_path = os.path.join(folder_path, 'nodes.py')
    if os.path.exists(nodes_file_path):
     
        with open(nodes_file_path, 'r') as nodes_file:
            nodes_content = nodes_file.read()
            if nodes_content.strip(): 
                _modify_exe_file(f"Nodes content from '{folder_name}'", nodes_content.strip())
            else:
                click.echo(f"Die 'nodes.py'-Datei in '{folder_name}' ist leer.")
    else:
        click.echo(f"Die 'nodes.py'-Datei wurde in '{folder_name}' nicht gefunden.")

def _extract_node_functions(pipeline_content):
    extracted_functions = []
    lines = pipeline_content.split('\n')
    for line in lines:
        if 'Node(' in line:
            function_name = None
            inputs = None
            outputs = None
            
            # Extrahiere Funktion
            if 'function=' in line:
                function_start = line.find('function=') + len('function=')
                function_end = line.find(',', function_start)
                function_name = line[function_start:function_end].strip().split('.')[-1]
            
            # Extrahiere Inputs
            if 'inputs=[' in line:
                inputs_start = line.find('inputs=[') + len('inputs=[')
                inputs_end = line.find(']', inputs_start)
                inputs = line[inputs_start:inputs_end].strip().replace('"', '').replace("'", '').split(',')
                inputs = [inp.strip() + ".data" for inp in inputs]

            # Extrahiere Outputs
            if 'outputs=[' in line:
                outputs_start = line.find('outputs=[') + len('outputs=[')
                outputs_end = line.find(']', outputs_start)
                outputs = line[outputs_start:outputs_end].strip().replace('"', '').replace("'", '').split(',')
                outputs = [out.strip() + ".data" for out in outputs]
                
            # Erstelle die Funktionseinträge
            if function_name and inputs:
                if outputs:
                    extracted_functions.append(f"{', '.join(outputs)} = {function_name}({', '.join(inputs)})")
                else:
                    extracted_functions.append(f"{function_name}({', '.join(inputs)})")
    return extracted_functions


def _call_node_functions(folder_name, folder_path):
  
    pipeline_file_path = os.path.join(folder_path, 'pipeline.py')
    if os.path.exists(pipeline_file_path):
     
        with open(pipeline_file_path, 'r') as nodes_file:
            pipeline_content = nodes_file.read()
            if pipeline_content.strip(): 
               
                modified_content = "\n".join(_extract_node_functions(pipeline_content))
                _modify_exe_file(f"Nodes content from '{folder_name}'",modified_content )
            else:
                click.echo(f"Die 'nodes.py'-Datei in '{folder_name}' ist leer.")
    else:
        click.echo(f"Die 'pipeline.py'-Datei wurde in '{folder_name}' nicht gefunden.")

def _search_folders(place_directory, pipeline_order):
    """
    Sucht nach den Ordnern im angegebenen Verzeichnis basierend auf der extrahierten Liste.

    :param place_directory: Das Verzeichnis, in dem gesucht werden soll.
    :param pipeline_order: Die Liste von Ordnernamen, nach denen gesucht werden soll.
    """
    if os.path.exists(place_directory):
        click.echo(f"Suche nach Ordnern in '{place_directory}':")
        for folder_name in pipeline_order:
            folder_name = folder_name.strip()
            folder_path = os.path.join(place_directory, folder_name)
            if os.path.isdir(folder_path):
                click.echo(f"Ordner '{folder_name}' gefunden: {folder_path}")
                _copy_nodes_content(folder_name, folder_path)
                _call_node_functions(folder_name, folder_path)
            else:
                click.echo(f"Ordner '{folder_name}' nicht gefunden.")
    else:
        click.echo(f"Ort '{place_directory}' nicht gefunden.")


def _create_exe_file(project_name):
    """
    Erstellt eine exe.py im aktuellen Verzeichnis.
    """
    exe_file_path = os.path.join(os.getcwd(), 'exe.py')
    with open(exe_file_path, 'w') as exe_file:
        exe_file.write(f"# This is the compiles Source Code of your Pipeline project called '{project_name}'\n")


def _modify_exe_file(comment, value):
    """
    Modifiziert die exe.py-Datei im aktuellen Verzeichnis.

    :param comment: Der Kommentar, der zur letzten Zeile hinzugefügt werden soll.
    :param value: Der Wert, der hinzugefügt werden soll.
    """
    exe_file_path = os.path.join(os.getcwd(), 'exe.py')
    with open(exe_file_path, 'r') as exe_file:
        lines = exe_file.readlines()

    # Finde die letzte Zeile, füge den Kommentar hinzu und aktualisiere den Wert
    last_line_index = len(lines) - 1
    lines[last_line_index] = lines[last_line_index].rstrip() + f"\n\n# {comment}\n"
    lines.append(f"{value}\n")

    with open(exe_file_path, 'w') as exe_file:
        exe_file.writelines(lines)


def _copy_jetline_functions():
    """
    Kopiert die Funktionen aus dem Modul jetline.data.helper und gibt sie als Text zurück.
    """
    try:
        # Pfad zum Modul jetline.data.helper
        module_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "helper.py")

        # Funktionen aus dem Modul lesen und als Text zurückgeben
        with open(module_path, 'r') as module_file:
            module_content = module_file.read()
            return module_content
    except FileNotFoundError:
        print("Modul jetline.data.helper nicht gefunden.")
    except Exception as e:
        print(f"Fehler beim Lesen des Moduls jetline.data.helper: {e}")


def clean_exe_file():
    exe_file_path = os.path.join(os.getcwd(), 'exe.py')

    # Vulture verwenden, um nicht verwendeten Code zu finden
    def vulture_scan():
        v = vulture.Vulture()
        v.scan(open(exe_file_path).read())

        # Zeilennummern des nicht verwendeten Codes extrahieren
        unused_code_lines = set()
        for item in v.get_unused_code():
            unused_code_lines.update(range(item.first_lineno, item.last_lineno + 1))

        # Alle Zeilen mit nicht verwendeten Code oder Kommentaren in """ entfernen
        if unused_code_lines:
            with open(exe_file_path, 'r') as f:
                lines = f.readlines()

            modified_lines = []
            in_multiline_comment = False
            for line_number, line in enumerate(lines, start=1):
                # Überprüfen, ob die Zeile in einem mehrzeiligen Kommentar ist
                if '"""' in line:
                    if not in_multiline_comment:
                        in_multiline_comment = True
                    else:
                        in_multiline_comment = False
                        continue
                if in_multiline_comment:
                    continue
                
                # Überprüfen, ob die Zeile nicht verwendet wird oder leer ist
                if line_number not in unused_code_lines and line.strip():  # strip entfernt Whitespace am Anfang und Ende
                    modified_lines.append(line)

            with open(exe_file_path, 'w') as f:
                f.writelines(modified_lines)

    vulture_scan()
    vulture_scan()
    print("Nicht verwendeten Code erfolgreich entfernt.")
    

def _find_classes():
    """
    Sucht nach Klassen in der data.py-Datei im aktuellen Verzeichnis und initialisiert sie in der exe.py-Datei.
    """
    current_directory = os.getcwd()
    data_file_path = os.path.join(current_directory, 'data.py')

    if os.path.exists(data_file_path):
        with open(data_file_path, 'r') as file:
            file_content = file.read()
            if file_content.strip():  # Überprüfen, ob die Dateiinhalt nicht leer ist
                # Kopieren von Funktionen aus jetline-Modulen
                copied_functions = _copy_jetline_functions()
                _modify_exe_file("Helper", copied_functions.strip())

                # Entfernen von 'Data' innerhalb von Klammern

                file_content = re.sub(r'^(?:from\s+jetline.*|import\s+jetline.*)$', '', file_content, flags=re.MULTILINE)
                file_content = "class Data:\n    def __init__(self, name, data):\n        self.name = name\n        self.data = data\n\n" + file_content

                _modify_exe_file("Data Classes", file_content.strip())

                # Finden aller Klassendefinitionen
                class_definitions = re.findall(r'class\s+(\w+)\(.*?\):', file_content)

                # Initialisieren von Klassen in exe.py
                initialization_lines = []
                for class_name in class_definitions:
                    class_content = re.search(r'class\s+' + class_name + r'\(.*?\):(.+?)(?=class|\Z)', file_content, re.DOTALL)
                    if class_content:
                        name_assignment = re.search(r'name\s*=\s*["\']([^"\']+)["\']', class_content.group(1))
                        if name_assignment:
                            initialization_line = f"{name_assignment.group(1)} = {class_name}()"
                            initialization_lines.append(initialization_line)


                # Verbinden der Initialisierungszeilen
                initialization_content = '\n'.join(initialization_lines)

                # Ändern der exe.py-Datei
                _modify_exe_file("Your data classes", initialization_content)
                print("Klassen aus data.py erfolgreich in exe.py kopiert.")
            else:
                print("Die data.py-Datei ist leer.")
    else:
        print("data.py-Datei nicht gefunden.")


@click.command()
@click.argument('output_name', default='output', required=False)
def build_exe(output_name):
    """
    Erstellt eine ausführbare Datei aus der Hauptdatei (main.py) und extrahiert die PIPELINE_ORDER-Liste.

    :param output_name: Der Name der Ausgabedatei (Standard: 'output')
    """
    # Aktuelles Verzeichnis
    current_directory = os.getcwd()
    place_folder = None
    
    # Pfad zur Hauptdatei
    main_path = os.path.join(current_directory, 'main.py')
    
    main_content = _read_main_file_content(main_path)
    pipeline_order = _extract_pipeline_order(main_content)

    if pipeline_order:
        # Pfad zur project.toml-Datei
        project_toml_path = os.path.join(current_directory, 'project.toml')

        place_folder, project_name = _extract_project_info(project_toml_path)

        if place_folder:
            place_directory = os.path.join(current_directory, place_folder)
        else:
            click.echo("Ort (place) nicht gefunden.")
    else:
        click.echo("PIPELINE_ORDER nicht gefunden.")

    # Erstelle und modifiziere die exe.py-Datei
    _create_exe_file(project_name)
    _find_classes()
    _search_folders(place_directory, pipeline_order)
    clean_exe_file()
 
    

    


if __name__ == "__main__":
    build_exe()
