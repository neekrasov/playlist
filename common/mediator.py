from typing import Protocol, Type

from .handler import Handler, InputType, ReturnType


class CommandNotFoundException(Exception):
    """Raised when a command is not found."""


class Mediator(Protocol):
    async def send(self, command: InputType):
        ...

    def bind(
        self,
        command: Type[InputType],
        handler: Handler[InputType, ReturnType],
    ):
        ...
