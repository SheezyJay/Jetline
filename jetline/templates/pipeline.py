from jetline.pipeline.pipeline import Pipeline
from jetline.pipeline.node import Node
from __PIPE__ import nodes as func


def register(data_manager) -> Pipeline:
    node1 = Node(
        function=func.node_function_1,
        inputs=["Name"],
        outputs=["Name"],
        viz={"y": 150, "x": 00, "sources": ['Name']}
    )
    node2 = Node(
        function=func.node_function_2,
        inputs=["Name"],
        viz={"y": 300, "x": 00, "sources": ["node_function_1"]}
    )

    return Pipeline(nodes=[node1, node2], data_manager=data_manager)
