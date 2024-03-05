import os
import importlib.util
import inspect
import toml
from jetline.logging import logger


class Data:
    """
    A class representing data.

    Attributes:
        name (str): The name of the data.
        data (Any): The actual data stored.
    """
    def __init__(self, name, data):
        self.name = name
        self.data = data
   
class DataManager:
    """
    The DataManager class is responsible for managing data objects. It ensures that only a single instance of the class is created.


    Example usage:

    caller_path = '/path/to/caller'
    data_manager = DataManager(caller_path)
    data_manager.add_jetline_data('name', obj)
    data_manager.update_jetline_data('name', new_value)
    data_manager.get_jetline_data('name')
    data_manager.list_jetline_data()
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
            Create a new instance of the class and ensures that only one instance of the class is created

            Parameters:
            - cls: The class object itself.
            - *args: Variable length argument list.
            - **kwargs: Arbitrary keyword arguments.

            Returns:
            - The instance of the class.

            """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, caller_path):
        """

        Initialize the object.

        :param caller_path: The caller_path parameter represents the base path of the caller.
        :type caller_path: str

        """
        if self._initialized:
            return
        self.data = {}
        self.caller_base_path = caller_path
        data_classes = self.load_data_classes()
        self.auto_add(data_classes)
        self._initialized = True

    def load_data_classes(self):
        """

        Purpose:
        This method loads data classes from a specified file and returns a list of the loaded classes.

        Parameters:
        - No parameters required.

        Returns:
        - List of loaded data classes.

        Example Usage:
        data_classes = load_data_classes()

        """
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
                            logger.info(f"Found: {data_class.__name__}, Description: {data_class.__doc__}")

                    except Exception as e:
                        logger.error(f"Error loading data classes from file {data_file}: {e}")
                        exit(1)

        return data_classes

    def auto_add(self, data_classes):
        """
        Automatically adds instances of given data classes to the jetline data.

        :param data_classes: List of data classes to add.
        """
        for data_class in data_classes:
            instance = data_class()
            self.add_jetline_data(instance.name, instance)

    def add_jetline_data(self, name, value):
        """
        Add jetline data to the data dictionary.
        """
        self.data[name] = {'value': value}

    def update_jetline_data(self, name, new_value):
        """
        Update jetline data to the data dictionary.
        """
        if name in self.data:
            self.data[name]['value'] = new_value
            logger.info(f"Data object '{name}' successfully updated.")
        else:
            logger.info(f"Data object '{name}' not found. Cannot be updated.")

    def get_jetline_data(self, name):
        """
        Retrieve the data associated with the given name from the self.data dictionary.
        """
        data_info = self.data.get(name)
        if data_info:
            return data_info['value'].data if hasattr(data_info['value'], 'data') else data_info['value']
        else:
            logger.error(f"Data object '{name}' not found.")
            logger.info("Contents of the self.data dictionary:")
            for data_name, data_info in self.data.items():
                logger.info(f"Name: {data_name}, Value: {data_info['value']}")
            return None
    def list_jetline_data(self):
        """
        Prints the stored data objects. Just for development.
        """
        print("Stored data objects:")
        for name, data_info in self.data.items():
            value_type = type(data_info['value'])
            print(f"{name}: {value_type} ")
