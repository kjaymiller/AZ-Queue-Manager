from abc import ABC, abstractmethod
from typing import Callable


# TODO: rename this
_parser_filter = Callable[[any], any]

class ExtensionBaseClass(ABC):
    def __init__(self, parser_filter: _parser_filter=lambda x:x):
        self.parser_filter = parser_filter

    @abstractmethod
    def transform_in(self, data: any):
        pass

    @abstractmethod
    def transform_one(self, data: str):
        pass

    @abstractmethod
    def transform_many(self, data: list[str]):
        pass