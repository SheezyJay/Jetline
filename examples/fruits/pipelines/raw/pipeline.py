from jetline.pipeline.pipeline import Pipeline
from jetline.pipeline.node import Node
from raw import nodes as func


def register(data_manager) -> Pipeline:
    return Pipeline(
        nodes=[
            Node(
                function=func.validate,
                inputs=["Fruits"],
                outputs=["Fruits"],
                viz={"y": 150, "x": 0, "sources": ['Fruits']}
            ),
            Node(
                function=func.export,
                inputs=["Fruits"],
                viz={"y": 300, "x": 0, "sources": ['validate']}
            ),
        ],
        data_manager=data_manager)
