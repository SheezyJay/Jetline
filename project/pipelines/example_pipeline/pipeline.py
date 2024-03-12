from jetline.pipeline.pipeline import Pipeline
from jetline.pipeline.node import Node
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from nodes import node_function_1, node_function_2

# Dont change name and directory of __file__ (pipline.py)

# Beispiel für die Registrierung einer Pipeline


def register(data_manager) -> Pipeline:
    # Definieren Sie die Nodes für die Pipeline
    nodes = [
        Node(name='node1', function=node_function_1, inputs=[1, 2,data_manager]),
        Node(name='node2', function=node_function_2, inputs=[1, 2], )
    ]

    # Erstellen und konfigurieren Sie die Pipeline mit den Nodes
    pipeline = Pipeline() 
    for node in nodes:
        pipeline.add_node(node.name, node.function, node.inputs)

    return pipeline
