from __future__ import annotations
from typing import Callable, Set

from node import Node

class NodeFlow:
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
        else:
            raise ValueError("Invalid operations, both types needs to be a Node or List[Node]")

    @staticmethod
    def chain(*objs: Node):
        for i in range(1, len(objs)):
            NodeFlow.forward(objs[i-1], objs[i])