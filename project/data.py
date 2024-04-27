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
