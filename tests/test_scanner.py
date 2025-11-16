from src.scanner import Scanner
from src.token import Token
from src.token_type import TokenType


def test_scan_empty_source():
    scanner = Scanner(source="")
    scanner.scan_tokens()
    assert len(scanner.tokens) == 1
    assert scanner.tokens[0] == Token(TokenType.EOF, "", None, 1)


def test_scan_number():
    scanner = Scanner(source="10")
    scanner.scan_tokens()
    assert len(scanner.tokens) == 2

    assert scanner.tokens[0] == Token(TokenType.NUMBER, "10", 10.0, 1)
    assert scanner.tokens[1] == Token(TokenType.EOF, "", None, 1)


def test_scan_variable_assignment():
    scanner = Scanner(source="var x = 25;")
    scanner.scan_tokens()
    assert len(scanner.tokens) == 6
    assert scanner.tokens[0] == Token(TokenType.VAR, "var", None, 1)
    assert scanner.tokens[1] == Token(TokenType.IDENTIFIER, "x", None, 1)
    assert scanner.tokens[2] == Token(TokenType.EQUAL, "=", None, 1)
    assert scanner.tokens[3] == Token(TokenType.NUMBER, "25", 25.0, 1)
    assert scanner.tokens[4] == Token(TokenType.SEMICOLON, ";", None, 1)
    assert scanner.tokens[5] == Token(TokenType.EOF, "", None, 1)


def test_scan_string():
    scanner = Scanner(source='"hello, woRLD!"')
    scanner.scan_tokens()
    assert len(scanner.tokens) == 2
    assert scanner.tokens[0] == Token(
        TokenType.STRING, '"hello, woRLD!"', "hello, woRLD!", 1
    )
    assert scanner.tokens[1] == Token(TokenType.EOF, "", None, 1)


def test_scan_comparision():
    scanner = Scanner(source="a != b == c < d")
    scanner.scan_tokens()
    assert len(scanner.tokens) == 8
    assert scanner.tokens[0] == Token(TokenType.IDENTIFIER, "a", None, 1)
    assert scanner.tokens[1] == Token(TokenType.BANG_EQUAL, "!=", None, 1)
    assert scanner.tokens[2] == Token(TokenType.IDENTIFIER, "b", None, 1)
    assert scanner.tokens[3] == Token(TokenType.EQUAL_EQUAL, "==", None, 1)
    assert scanner.tokens[4] == Token(TokenType.IDENTIFIER, "c", None, 1)
    assert scanner.tokens[5] == Token(TokenType.LESS, "<", None, 1)
    assert scanner.tokens[6] == Token(TokenType.IDENTIFIER, "d", None, 1)
    assert scanner.tokens[7] == Token(TokenType.EOF, "", None, 1)


def test_scan_brackets_and_braces():
    scanner = Scanner(source="{}()")
    scanner.scan_tokens()
    assert len(scanner.tokens) == 5
    assert scanner.tokens[0] == Token(TokenType.LEFT_BRACE, "{", None, 1)
    assert scanner.tokens[1] == Token(TokenType.RIGHT_BRACE, "}", None, 1)
    assert scanner.tokens[2] == Token(TokenType.LEFT_PAREN, "(", None, 1)
    assert scanner.tokens[3] == Token(TokenType.RIGHT_PAREN, ")", None, 1)
    assert scanner.tokens[4] == Token(TokenType.EOF, "", None, 1)
