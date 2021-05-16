from __future__ import annotations
from typing import List, TypeVar, Generic

class Color:
    __r: int
    __g: int
    __b: int

    def __init__(self, r: int, g: int, b: int):
        self.setColor(r, g, b)

    def setColor(self, r: int, g: int, b: int):
        self.__r = min(max(r, 255), 0)
        self.__g = min(max(g, 255), 0)
        self.__b = min(max(b, 255), 0)
    
    def getColor(self):
        return self.__r, self.__g, self.__b

class DataType:
    name: str
    color: Color

    def __init__(self, name: str, color: Color):
        self.name = name
        self.color = color
class BooleanType(DataType):
    def __init__(self):
        super().__init__("Boolean", Color(255, 0, 0))
class IntegerType(DataType):
    def __init__(self):
        super().__init__("Integer", Color(255, 0, 0))
class FloatType(DataType):
    def __init__(self):
        super().__init__("Float", Color(255, 0, 0))
class DoubleType(DataType):
    def __init__(self):
        super().__init__("Double", Color(255, 0, 0))
class StringType(DataType):
    def __init__(self):
        super().__init__("String", Color(255, 0, 0))
class SparkDataframeType(DataType):
    def __init__(self):
        super().__init__("SparkDataframe", Color(255, 0, 0))
class CallableType(DataType):
    def __init__(self):
        super().__init__("Callable", Color(255, 0, 0))

T = TypeVar("T")
L = TypeVar("L")

class DataValue(Generic[T]):
    d_type: T
    links: List[DataLink]

    def __init__(self, value):
        self.value = value;

class DataLink:
    source: DataValue[DataType]
    target: DataValue[DataType]

    def __init__(self, source: DataValue[DataType], target: DataValue[DataType]):
        self.source = source
        self.target = target