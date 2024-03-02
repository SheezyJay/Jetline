
from jetline.data.data import Data
from jetline.data.helper import choose_file


class YourDataClass(Data):
   
    def __init__(self):
        super().__init__(
            name="Name",
            data=self.get_data(),
          
        )

    def get_data(self):
        file = choose_file()
        return file

