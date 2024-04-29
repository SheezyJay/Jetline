

class Node:
    """
    Node

    Represents a node in a graph that performs a specific function on input data.

    Attributes:
        name (str): The name of the node.
        function (callable): The function to be executed by the node.
        inputs (list): A list of input names or values for the function.
        outputs (list or None): A list of output names for the function. If None, the node does not have outputs.

    Methods:
        execute(data_manager):
        Executes the function of the node using input data from the data manager. If outputs are specified, updates the data manager with the results.

    """
    def __init__(self, function, inputs, outputs=None, viz=None):
        self.function = function
        self.inputs = inputs
        self.outputs = outputs
        self.viz = viz

    def execute(self, data_manager):
        """

        Executes the given function with the provided input data and updates the output data if specified.

        Parameters:
        - data_manager: The data manager object that is used to access and update data.

        Returns:
        - The result of executing the function.

        """
        resolved_inputs = [data_manager.get_jetline_data(name) if isinstance(name, str) else name for name in self.inputs]
        result = self.function(*resolved_inputs)
        
        if self.outputs:
            if isinstance(self.outputs, list):
                for output_name in self.outputs:
                    data_manager.update_jetline_data(output_name, result)
            else:
                raise ValueError("Invalid type for `outputs`. `outputs` must be a list of hashable types.")

        return result
