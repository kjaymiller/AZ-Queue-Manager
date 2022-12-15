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
    def transform_preview(self, data: str):
        pass

    @abstractmethod
    def transform_out(self, data: list[str]):
        pass