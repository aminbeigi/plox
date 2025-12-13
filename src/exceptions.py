"""Exception classes for the Plox interpreter."""

from src.token import Token


class ParseError(Exception):
    """Exception raised during parsing when syntax errors are encountered."""

    pass


class PloxRuntimeError(RuntimeError):
    """Exception raised during runtime when execution errors occur."""

    def __init__(self, token: Token, message: str) -> None:
        super().__init__(message)
        self.token = token
        self.message = message
