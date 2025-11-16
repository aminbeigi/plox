from src.expr import BinaryExpr, LiteralExpr, GroupingExpr, UnaryExpr
from src.token import Token
from src.token_type import TokenType
from src.ast_printer import AstPrinter


def test_tree_print():
    left = UnaryExpr(
        Token(token_type=TokenType.MINUS, lexeme="-", literal=None, line=1),
        LiteralExpr("123"),
    )
    expression = Token(token_type=TokenType.STAR, lexeme="*", literal=None, line=1)
    right = GroupingExpr(LiteralExpr("45.67"))
    tmp = BinaryExpr(left, expression, right)
    banana = AstPrinter()
    result = banana.print(tmp)
    assert result == "(* (- 123) (group 45.67))"
