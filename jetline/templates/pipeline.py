
from jetline.pipeline.pipeline import Pipeline
from jetline.pipeline.node import Node
from __PIPE__ import nodes as func

# Dont change name and directory of __file__ (pipline.py)

"""
dont change the name and the directory of the __file__ (pipeline.py) and the structure of the register function.
Just define and order your nodes in the return statement:
Node(name='[can_be_any]', function=func.[your_specific_node], inputs=["Name_of_your_Data_defined_in_data.py"]
, outputs=["Name_of_your_Data_defined_in_data.py"]
"""
def register(data_manager) -> Pipeline:

    return Pipeline(nodes=[
        Node(name='node1', function=func.node_function_1, inputs=["Name"], outputs=["Name"]),
        Node(name='node2', function=func.node_function_2,inputs=["Name"]),
       
    ], data_manager=data_manager)


