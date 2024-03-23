class Node:
    def __init__(self, name, function, inputs, outputs=None):
        """
        Args:
            name: Der Name der Funktion.
            function: Die Funktion, die aufgerufen wird.
            inputs: Die Inputs, die der Funktion übergeben werden.
            outputs: Eine Liste von Namen der Outputs, die im DataManager gespeichert werden sollen.
        """
        self.name = name
        self.function = function
        self.inputs = inputs
        self.outputs = outputs

    def execute(self, data_manager):
        """
        Führt die Funktion mit den Inputs aus und speichert jeden Output im DataManager, falls Output-Namen angegeben wurden.
        
        Args:
            data_manager: Eine Instanz von DataManager, um Outputs zu speichern.
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
