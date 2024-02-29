from kiper.data.data import Data

class YourDataClass(Data):
    def __init__(self):
        super().__init__(
            name="Name",
            data="Data",
            description="Description"
        )