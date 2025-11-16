from typing import List

from src.token_type import TokenType
from src.token import Token
from src.plox import Plox


class Scanner:
    """Scans source code and produces a list of tokens.
    
    Attributes:
        source: The source code to scan.
        tokens: The list of tokens produced from scanning.
        start: The starting index of the current lexeme being scanned.
        current: The current index in the source code being scanned.
        line: The current line number in the source code.
    """
    KEYWORDS = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
    }

    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens: List[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self) -> None:
        """Scans the source code and populates the tokens list."""
        while not self._is_at_end():
            self.start = self.current
            self._scan_token()

        token = Token(TokenType.EOF, "", None, self.line)
        self.tokens.append(token)

    def _scan_token(self) -> None:
        """Scans a single token from the source code."""
        char = self._advance()
        match char:
            case "(":
                self._add_token(TokenType.LEFT_PAREN)
            case ")":
                self._add_token(TokenType.RIGHT_PAREN)
            case "{":
                self._add_token(TokenType.LEFT_BRACE)
            case "}":
                self._add_token(TokenType.RIGHT_BRACE)
            case ",":
                self._add_token(TokenType.COMMA)
            case ".":
                self._add_token(TokenType.DOT)
            case "-":
                self._add_token(TokenType.MINUS)
            case "+":
                self._add_token(TokenType.PLUS)
            case ";":
                self._add_token(TokenType.SEMICOLON)
            case "*":
                self._add_token(TokenType.STAR)
            case "!":
                if self._match("="):
                    self._add_token(TokenType.BANG_EQUAL)
                else:
                    self._add_token(TokenType.BANG)
            case "=":
                if self._match("="):
                    self._add_token(TokenType.EQUAL_EQUAL)
                else:
                    self._add_token(TokenType.EQUAL)
            case "<":
                if self._match("="):
                    self._add_token(TokenType.LESS_EQUAL)
                else:
                    self._add_token(TokenType.LESS)
            case ">":
                if self._match("="):
                    self._add_token(TokenType.GREATER_EQUAL)
                else:
                    self._add_token(TokenType.GREATER)
            case "/":
                if self._match("/"):
                    # a comment goes until the end of the line
                    while self._peek() != "\n" and not self._is_at_end():
                        self._advance()
                else:
                    self._add_token(TokenType.SLASH)
            case " ":
                pass
            case "\r":
                pass
            case "\t":
                pass
            case "\n":
                self.line = self.line + 1
            case '"':
                self._string()
            case _:
                if char.isdigit():
                    self._number()
                elif self._is_alpha(char):
                    self._identifier()
                else:
                    Plox.error(self.line, "Unexpected character.")

    def _add_token(self, token_type: TokenType, literal: object = None) -> None:
        """Adds a token to the tokens list."""
        text = self.source[self.start : self.current]
        token = Token(token_type, text, literal, self.line)
        self.tokens.append(token)

    def _advance(self) -> str:
        """Advances the scanner by one character and returns it."""
        res = self.source[self.current]
        self.current += 1
        return res

    def _is_at_end(self) -> bool:
        """Checks if the scanner has reached the end of the source code."""
        return self.current >= len(self.source)

    def _match(self, expected: str) -> bool:
        """Checks if the next character matches the expected character."""
        if self._is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current = self.current + 1
        return True

    def _peek(self) -> str:
        """Returns the current character without advancing the scanner."""
        if self._is_at_end():
            return "\0"
        return self.source[self.current]

    def _peek_next(self) -> str:
        """Returns the character after the current one without advancing the scanner."""
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def _is_alpha(self, char: str) -> bool:
        """Checks if a character is an alphabetic letter or underscore."""
        return char.isalpha() or char == "_"

    def _is_alphanumeric(self, char: str) -> bool:
        """Checks if a character is alphanumeric (letter or digit)."""
        return char.isdigit() or self._is_alpha(char)

    def _string(self) -> None:
        """Scans a string literal from the source code."""
        while self._peek() != '"' and not self._is_at_end():
            if self._peek() == "\n":
                self.line = self.line + 1
            self._advance()

        if self._is_at_end():
            Plox.error(self.line, "Unterminated string.")
            return

        self._advance()

        value = self.source[self.start + 1 : self.current - 1]
        self._add_token(TokenType.STRING, value)

    def _number(self) -> None:
        """Scans a number literal from the source code."""
        while self._peek().isdigit():
            self._advance()

        if self._peek() == "." and self._peek_next().isdigit():
            self._advance()

            while self._peek().isdigit():
                self._advance()

        self._add_token(TokenType.NUMBER, float(self.source[self.start : self.current]))

    def _identifier(self) -> None:
        """Scans an identifier or keyword from the source code."""
        while self._is_alphanumeric(self._peek()):
            self._advance()

        text = self.source[self.start : self.current]
        token_type = Scanner.KEYWORDS.get(text)
        if token_type is None:
            token_type = TokenType.IDENTIFIER

        self._add_token(token_type)
