from kiper.pipeline.pipeline import Pipeline
from kiper.pipeline.node import Node
from kiper.example_pipeline.example_node import node_function_1, node_function_2

# Dont change name and directory of __file__ (pipline.py)

def register() -> Pipeline:
    # Define notes for the pipeline
    nodes = [
        Node(name='node1', function=node_function_1, inputs=[1, 2]),
        Node(name='node2', function=node_function_2, inputs=[1, 2])
    ]


    pipeline = Pipeline() 
    for node in nodes:
        pipeline.add_node(node.name, node.function, node.inputs)

    return pipeline