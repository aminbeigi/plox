from src.expr import BinaryExpr, LiteralExpr, GroupingExpr, UnaryExpr
from src.token import Token
from src.token_type import TokenType
from src.ast_printer import AstPrinter


def test_binary():
    left = LiteralExpr(1)
    operator = Token(token_type=TokenType.PLUS, lexeme="+", literal=None, line=1)
    right = LiteralExpr(2)
    binaryExpr = BinaryExpr(left, operator, right)
    result = AstPrinter().print(binaryExpr)
    assert result == "(+ 1 2)"


def test_grouping():
    expression = LiteralExpr(42)
    groupingExpr = GroupingExpr(expression)
    result = AstPrinter().print(groupingExpr)
    assert result == "(group 42)"


def test_unary():
    unaryExpr = UnaryExpr(
        Token(token_type=TokenType.MINUS, lexeme="-", literal=None, line=1),
        LiteralExpr(500),
    )
    result = AstPrinter().print(unaryExpr)
    assert result == "(- 500)"


def test_literal():
    literalExpr = LiteralExpr(123)
    result = AstPrinter().print(literalExpr)
    assert result == "123"


def test_complex():
    left = UnaryExpr(
        Token(token_type=TokenType.MINUS, lexeme="-", literal=None, line=1),
        LiteralExpr("123"),
    )
    expression = Token(token_type=TokenType.STAR, lexeme="*", literal=None, line=1)
    right = GroupingExpr(LiteralExpr("45.67"))
    result = AstPrinter().print(BinaryExpr(left, expression, right))
    assert result == "(* (- 123) (group 45.67))"
