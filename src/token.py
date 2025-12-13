from src.token_type import TokenType


class Token:
    """Represents a lexical token in the source code.

    Attributes:
        type: The type of the token, from the TokenType enum.
        lexeme: The exact string representation of the token in the source.
        literal: The parsed literal value associated with the token, if any.
        line: The line number where the token appears in the source code.
    """

    def __init__(
        self,
        type: TokenType,
        lexeme: str,
        literal: str | float | bool | None,
        line: int,
    ):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self) -> str:
        return f"Token(self={self.type}, lexeme={self.lexeme}, literal={self.literal}, line={self.line})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Token):
            return NotImplemented
        return (
            self.type == other.type
            and self.lexeme == other.lexeme
            and self.literal == other.literal
            and self.line == other.line
        )
