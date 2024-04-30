from jetline.data.data import Data


class Fruits(Data):
    def __init__(self):
        super().__init__(
            name="Fruits",
            data=self.__getter__()
        )

    def __getter__(self):
        return ['banana', 'apple', 'mango']

    class Meta:
        description = "This is the Fruit Data Class"
        y = 0
        x = 0
