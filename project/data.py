from jetline.data.data import Data
from jetline.data.helper import choose_file


class YourDataClass(Data):
    "asdads"

    def __init__(self):
        super().__init__(
            name="Name",
            data=self.get_data(),

        )

    @staticmethod
    def get_data():
        file = choose_file()
        return file

class YourDataClass(Data):

    def __init__(self):
        super().__init__(
            name="Name",
            data=self.get_data(),

        )

    @staticmethod
    def get_data():
        file = choose_file()
        return file

class YourDataClass(Data):

    def __init__(self):
        super().__init__(
            name="Name",
            data=self.get_data(),

        )

    @staticmethod
    def get_data():
        file = choose_file()
        return file
