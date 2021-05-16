from __future__ import annotations
from typing import Callable, Set
from time import sleep

from data import DataValue, StringType, IntegerType
from pipeline_context import PipelineContext

class Node:
    typeName: DataValue[StringType] 
    name: DataValue[StringType]
    description: DataValue[StringType]
    predecessors: Set[Node]
    sucessors: Set[Node]
    succeded: bool

    def __init__(self, typeName: str, name: str, description: str):
        self.typeName = DataValue[StringType](typeName)
        self.name = DataValue[StringType](name)
        self.description = DataValue[StringType](description)
        self.predecessors = set()
        self.sucessors = set()
        self.succeded = False
        PipelineContext.register(self)
    
    def run(self):
        raise ValueError("Node can't be intantiated, please use a exetend class")
    
    @staticmethod
    def forward(previous: Node, posterior: Node):
        print(type(previous), type(posterior))
        if isinstance(previous, Node) and isinstance(posterior, Node):
            posterior.predecessors.add(previous)
            previous.sucessors.add(posterior)
        elif isinstance(previous, Node) and isinstance(posterior, list):
            if any([not isinstance(o, Node) for o in posterior]):
                raise ValueError("The elements in the list all must be a Node")
            else:
                for o in posterior:
                    previous.sucessors.add(o)
                    o.predecessors.add(previous)
        elif isinstance(previous, list) and isinstance(posterior, Node):
            if any([not isinstance(o, Node) for o in previous]):
                raise ValueError("The elements in the list all must be a Node")
            else:
                for o in previous:
                    o.sucessors.add(posterior)
                    posterior.predecessors.add(o)
        elif isinstance(previous, list) and isinstance(posterior, list):
            if any([not isinstance(o, Node) for o in previous]) and any([not isinstance(o, Node) for o in posterior]):
                raise ValueError("The elements in the list all must be a Node")
            else:
                for node_posterior in posterior:
                    for node_predecessor in posterior:
                        node_posterior.predecessors.add(node_predecessor)
                        node_predecessor.sucessors.add(node_posterior)

    def __rshift__(self, node):
        Node.forward(self, node)

    def __lshift__(self, node):
        Node.forward(node, self)

class DelayNode(Node):
    delay_time: DataValue[IntegerType]

    def __init__(self, name: str, description: str, delay_time: int):
        super().__init__("DelayNode", name, description)

        self.delay_time = DataValue[IntegerType](delay_time)

    def run(self):
        sleep(self.delay_time.value)

class PythonNode(Node):
    python_fn: DataValue[IntegerType]

    def __init__(self, name: str, description: str, python_fn: Callable):
        super().__init__("DelayNode", name, description)

        self.python_fn = DataValue[IntegerType](python_fn)

    def run(self):
        self.python_fn.value()