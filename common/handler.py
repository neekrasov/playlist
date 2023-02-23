from abc import ABC, abstractmethod
from typing import Generic, TypeVar

InputType = TypeVar("InputType")
ReturnType = TypeVar("ReturnType")


class Handler(ABC, Generic[InputType, ReturnType]):
    @abstractmethod
    async def execute(self, command: InputType) -> ReturnType:
        ...
