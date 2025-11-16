from src.token import Token
from src.token_type import TokenType

def test_token_object():
    token = Token(token_type=TokenType.EQUAL_EQUAL, lexeme="==", literal=None, line=1)
    assert token.__str__() == "Token(self=TokenType.EQUAL_EQUAL, lexeme===, literal=None, line=1)"
    assert token.__repr__() == "Token(self=TokenType.EQUAL_EQUAL, lexeme===, literal=None, line=1)"