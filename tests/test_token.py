from src.token import Token
from src.token_type import TokenType


def test_token_creation_basic():
    """Test basic token creation and attribute assignment."""
    token = Token(TokenType.IDENTIFIER, "myVar", None, 5)

    assert token.type == TokenType.IDENTIFIER
    assert token.lexeme == "myVar"
    assert token.literal is None
    assert token.line == 5


def test_token_repr():
    """Test that __repr__ returns the correct string representation."""
    token = Token(type=TokenType.NUMBER, lexeme="45", literal=45.0, line=1)
    expected = "Token(self=TokenType.NUMBER, lexeme=45, literal=45.0, line=1)"
    assert token.__repr__() == expected


def test_token_str_representation():
    """Test that __str__ uses __repr__ and returns the same string."""
    token = Token(type=TokenType.STRING, lexeme='"hello"', literal="hello", line=2)
    # __str__ should use __repr__ in Token class
    assert str(token) == repr(token)
    expected = 'Token(self=TokenType.STRING, lexeme="hello", literal=hello, line=2)'
    assert str(token) == expected


def test_token_equality_same_tokens():
    """Test that identical tokens are equal."""
    token1 = Token(TokenType.PLUS, "+", None, 1)
    token2 = Token(TokenType.PLUS, "+", None, 1)
    assert token1 == token2
    assert not (token1 != token2)  # Test != operator as well


def test_token_equality_different_tokens():
    """Test that tokens with different types are not equal."""
    token1 = Token(TokenType.PLUS, "+", None, 1)
    token2 = Token(TokenType.MINUS, "-", None, 1)
    assert token1 != token2
    assert not (token1 == token2)  # Test == operator returns False


def test_token_equality_different_type():
    """Test that tokens are not equal to non-Token objects."""
    token = Token(TokenType.PLUS, "+", None, 1)

    # Test against different object types
    assert token != "apples"
    assert token != 42
    assert token is not None
    assert token != []
    assert token != {}

    # Ensure == returns False (not just != returning True)
    assert not (token == "apples")
