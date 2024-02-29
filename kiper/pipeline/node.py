class Node:
    def __init__(self, name, function, inputs):
        self.name = name
        self.function = function
        self.inputs = inputs

    def execute(self):
        return self.function(*self.inputs)