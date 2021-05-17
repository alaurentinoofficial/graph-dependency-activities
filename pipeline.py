from __future__ import annotations
from typing import Dict, List
from multiprocessing import Process

from node import Node
from node_executor import NodeExecutor
from status import Status
from pipeline_context import PipelineContext

class Pipeline:
    name: str
    __nodes: List[Node]
    __process: Process
    __queue: Dict

    def check_nodes(self):
        node_name = set()
        for n in self.__nodes:
            if not n.name.value in node_name:
                node_name.add(n.name.value)
            else:
                raise ValueError(f"Duplicated node name \"{n.name.value}\"")

    def __init__(self, name: str) -> None:
        self.name = name
        self.__nodes = []
        self.check_nodes()
        self.__process = Process(target=self.__run__)
        self.__queue = dict()
    
    def get_root_nodes(self):
        return [n for n in self.__nodes if len(n.predecessors) == 0]

    def add_in_queue(self, node: Node):
        process = NodeExecutor(node)
        print(f"{process.node.name.value}> {process.status}")
        self.__queue[process.id] = process
    
    def close(self):
        self.__process.close()

    def __run__(self):
        root_nodes = self.get_root_nodes()

        for node in root_nodes:
            self.add_in_queue(node)

        while any(not process.status == Status.Executed for process in self.__queue.values()):
            for _, process in list(self.__queue.items()):
                if process.status == Status.Queued:
                    process.start()
                    print(f"{process.node.name.value}> {process.status}")

                elif process.status == Status.Running and not process.is_alive():
                    process.close()
                    print(f"{process.node.name.value}> {process.status}")
                    
                    for next_node in process.node.sucessors:
                        if next_node.is_available:
                            self.add_in_queue(next_node)

    def __enter__(self):
        PipelineContext.listen()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__nodes = PipelineContext.close()
        self.start()
        self.join()

    def start(self):
        self.__process.start()

    def join(self):
        self.__process.join()