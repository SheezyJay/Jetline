import os
import importlib.util
import inspect
import toml
import logging
logging.basicConfig(level=logging.DEBUG)


class Data:
    def __init__(self, name, data, description=None):
        """
         Initializes the object with data. This is the constructor for the class. You can override this if you want to do something other than initialize the object with a different name and / or data
         
         Args:
         	 name: The name of the object
         	 data: The data to be stored in the object's data
         	 description: A description of the
        """
        
        self.name = name
        self.data = data
        self.description = description



class DataManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, caller_path):
        if self._initialized:
            return
        self.data = {}
        self.caller_base_path = caller_path
        data_classes = self.load_data_classes()
        self.auto_add(data_classes)
        self._initialized = True

    def load_data_classes(self):
        data_classes = []
        project_toml_path = self.caller_base_path / "project.toml"
        if os.path.exists(project_toml_path):
            with open(project_toml_path, "r") as f:
                config = toml.load(f)
                data_file = config.get("locations", {}).get("data_file")
                if data_file and os.path.exists(data_file):
                    try:
                        spec = importlib.util.spec_from_file_location("data_module", data_file)
                        data_module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(data_module)

                        for name, obj in inspect.getmembers(data_module):
                            if inspect.isclass(obj) and isinstance(obj, type) and obj != data_module.Data:
                                data_classes.append(obj)

                        for data_class in data_classes:
                            logging.info(f"Found: {data_class.__name__}, Description: {data_class.__doc__}")

                    except Exception as e:
                        logging.error(f"Error loading data classes from file {data_file}: {e}")
                        exit(1)

        return data_classes

    def auto_add(self, data_classes):
        for data_class in data_classes:
            instance = data_class()
            self.add(instance.name, instance, instance.description)

    def add(self, name, value, description=None):
        self.data[name] = {'value': value, 'description': description}

    def get(self, name):
        data_info = self.data.get(name)
        if data_info:
            return data_info['value'].data
        else:
            print(f"Data object '{name}' not found.")
            print("Contents of the self.data dictionary:")
            for data_name, data_info in self.data.items():
                print(f"Name: {data_name}, Value: {data_info['value']}")
            return None

    def update(self, name, new_value):
        if name in self.data:
            self.data[name]['value'] = new_value
            print(f"Data object '{name}' successfully updated.")
        else:
            print(f"Data object '{name}' not found. Cannot be updated.")

    def list(self):
        print("Stored data objects:")
        for name, data_info in self.data.items():
            value_type = type(data_info['value'])
            description = data_info['description']
            print(f"{name}: {value_type} - {description}")
# Beispielklassen für Daten
"""
class SapData(Data):
    def __init__(self):
        super().__init__(
            name="SAP-Daten",
            data="asd",
            description="Daten aus dem SAP-System"
        )

class DrcData(Data):
    def __init__(self):
        super().__init__(
            name="DRC-Daten",
            data=None,
            description="Daten aus dem DRC-System"
        )

# Beispielverwendung des DataManager

def main():
    data_manager = DataManager([SapData, DrcData])
    data_manager.list()

if __name__ == "__main__":
    main()
"""