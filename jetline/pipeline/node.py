class Node:
    def __init__(self, name, function, inputs):
        """
         Initializes the Function object. This is the method that should be called by the user to initialize the Function object
         
         Args:
         	 name: The name of the function
         	 function: The function that will be called when the function is called
         	 inputs: The inputs that will be passed to the function
        """
        self.name = name
        self.function = function
        self.inputs = inputs

    def execute(self):
        """
         Execute the function with the inputs. This is the method that will be called by the : class : ` Function ` when it is called.
         
         
         Returns: 
         	 The result of the function ( if any ) or None if there was an error ( in which case the error will be logged
        """
        return self.function(*self.inputs)