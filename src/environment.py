from src.token import Token
from src.exceptions import PloxRuntimeError


class Environment:
    def __init__(self) -> None:
        self._values: dict[str, object] = {}

    def define(self, name: str, value: object) -> None:
        self._values[name] = value

    def assign(self, name: Token, value: object) -> None:
        if name.lexeme in self._values:
            self._values[name.lexeme] = value
            return

        raise PloxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def get(self, name: Token) -> object:
        if name.lexeme in self._values:
            return self._values[name.lexeme]

        raise PloxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
