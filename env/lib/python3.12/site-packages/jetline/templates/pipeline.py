
from jetline.pipeline.pipeline import Pipeline
from jetline.pipeline.node import Node
from __PIPE__ import nodes as func

# Dont change name and directory of __file__ (pipline.py)
def register(data_manager) -> Pipeline:
    return Pipeline(nodes=[
        Node(name='node1', function=func.node_function_1, inputs=["Name"], outputs=["Name"]),
        Node(name='node2', function=func.node_function_2,inputs=["Name"]),
       
    ], data_manager=data_manager)


