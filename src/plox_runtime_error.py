from src.token import Token


class PloxRuntimeError(RuntimeError):
    def __init__(self, token: Token, message: str) -> None:
        super().__init__(message)
        self.token = token
        self.message = message
