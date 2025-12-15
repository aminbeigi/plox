from src.token import Token
from src.exceptions import PloxRuntimeError


class Environment:
    def __init__(self, enclosing: Environment | None = None) -> None:
        self._values: dict[str, object] = {}
        self._enclosing = enclosing

    def define(self, name: str, value: object) -> None:
        self._values[name] = value

    def assign(self, name: Token, value: object) -> None:
        if name.lexeme in self._values:
            self._values[name.lexeme] = value
            return

        if self._enclosing is not None:
            self._enclosing.assign(name, value)
            return

        raise PloxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def get(self, name: Token) -> object:
        if name.lexeme in self._values:
            return self._values[name.lexeme]

        if self._enclosing is not None:
            return self._enclosing.get(name)

        raise PloxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
