from __future__ import annotations
import uuid
from multiprocessing import Process

from node import Node
from status import Status

class NodeExecutor:
    id: uuid.UUID
    status: str
    node: Node
    __process: Process

    def __init__(self, node: Node) -> None:
        self.id = uuid.uuid4()
        self.node = node
        self.node.succeded = False
        self.__process = Process(target=self.node.run)
        self.status = Status.Queued
    
    def start(self) -> None:
        self.__process.start()
        self.status = Status.Running

    def join(self) -> None:
        self.__process.join()

    def close(self) -> None:
        self.node.succeded = True
        self.status = Status.Executed
        self.__process.close()

    def is_alive(self) -> bool:
        return self.__process.is_alive()