from src.parser import Parser
from src.token import Token
from src.token_type import TokenType
from src.expr import LiteralExpr


def test_parser_creation():
    """Test basic parser creation with token list."""
    tokens = [Token(TokenType.NUMBER, "42", 42.0, 1), Token(TokenType.EOF, "", None, 1)]
    parser = Parser(tokens)

    assert parser._tokens == tokens
    assert parser._current == 0


def test_parse_simple_number():
    """Test parsing a simple number literal."""
    tokens = [Token(TokenType.NUMBER, "42", 42.0, 1), Token(TokenType.EOF, "", None, 1)]
    parser = Parser(tokens)

    expr = parser._expression()

    assert isinstance(expr, LiteralExpr)
    assert expr.value == 42.0


def test_parse_simple_string():
    """Test parsing a simple string literal."""
    tokens = [
        Token(TokenType.STRING, '"hello"', "hello", 1),
        Token(TokenType.EOF, "", None, 1),
    ]
    parser = Parser(tokens)

    expr = parser._expression()

    assert isinstance(expr, LiteralExpr)
    assert expr.value == "hello"


def test_parse_boolean_true():
    """Test parsing boolean true literal."""
    tokens = [Token(TokenType.TRUE, "true", None, 1), Token(TokenType.EOF, "", None, 1)]
    parser = Parser(tokens)

    expr = parser._expression()

    assert isinstance(expr, LiteralExpr)
    assert expr.value is True


def test_parse_boolean_false():
    """Test parsing boolean false literal."""
    tokens = [
        Token(TokenType.FALSE, "false", None, 1),
        Token(TokenType.EOF, "", None, 1),
    ]
    parser = Parser(tokens)

    expr = parser._expression()

    assert isinstance(expr, LiteralExpr)
    assert expr.value is False
