# This is the compiles Source Code of your Pipeline project called 'project'

# Data Classes
from jetline.data.data import Data
from jetline.data.helper import choose_file

"""
Here you can add your Data classes. You can import some helper classes @jetline.data.helper .
Every Dataclass needs a name and a data attributes. The name is like an id so only use a name once.

"""


class YourDataClass(Data):

    def __init__(self):
        super().__init__(
            name="Name",
            data=choose_file(),

        )

# Your data classes
Name = YourDataClass()

# Nodes content from 'example_pipeline'
def node_function_1(data):
    """An example function that processes data and returns a modified version."""
    print("Input Data:", data)
    processed_data = data + "asasdasdd"
    print("Processed Data:", processed_data)
    return processed_data
def node_function_2(data):
    """An example function that processes data andds"""
    print("Input Data:", data)
    return data

# Nodes content from 'example_pipeline'
Name.data = node_function_1(Name.data)
node_function_2(Name.data)
