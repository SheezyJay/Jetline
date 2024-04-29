from jetline.data.data import Data
from jetline.data.helper import choose_file


class YourDataClass(Data):
    def __init__(self):
        super().__init__(
            name="Name",
            data=choose_file(),

        )

    class Meta:
        description = "This is the description for viz"
        y = 0
        x = 0
