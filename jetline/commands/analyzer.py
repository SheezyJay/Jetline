import json
import toml

def create_json_file():
    # Lesen Sie den Namen und den Ort aus der project.toml-Datei
    with open("project.toml", "r") as f:
        toml_data = toml.load(f)
        project_name = toml_data["project"]["name"]
        project_place = toml_data["project"]["place"]

    # Erstellen Sie ein Dictionary mit den Informationen
    data = {
        "general": {
            "name": project_name
        }
    }

    # Schreiben Sie die Informationen in eine JSON-Datei
    with open("info.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

    print("JSON-Datei erfolgreich erstellt.")


if __name__ == "__main__":
    create_json_file()
