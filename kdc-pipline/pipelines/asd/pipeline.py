from Base import Pipeline, Node

def node_function_1(data, multiplier):
    return data * multiplier

def node_function_2(data, offset):
    return data + offset
def register() -> Pipeline:
    # Definition der Nodes für diese Pipeline
    nodes = [
        Node(name='node1', function=node_function_1, inputs=[1, 2]),
        Node(name='node2', function=node_function_2, inputs=[1, 2])
    ]

    # Hier können Sie festlegen, welche anderen Pipelines vor dieser ausgeführt werden müssen
    requires = ['asd copy'],

    pipeline = Pipeline(requires)  # Änderung hier: Initialisierung mit den 'requires'
    for node in nodes:
        pipeline.add_node(node.name, node.function, node.inputs)

    return pipeline
