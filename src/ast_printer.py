from src.expr import Expr, BinaryExpr, GroupingExpr, LiteralExpr, UnaryExpr
from src.visitor import Visitor


class AstPrinter(Visitor[str]):
    """Prints the AST in a parenthesized format."""

    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    def visit_binary_expr(self, expr: BinaryExpr) -> str:
        return self._parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: GroupingExpr) -> str:
        return self._parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: LiteralExpr) -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_unary_expr(self, expr: UnaryExpr) -> str:
        return self._parenthesize(expr.operator.lexeme, expr.right)

    def _parenthesize(self, name: str, *exprs: Expr) -> str:
        res = "(" + name
        for expr in exprs:
            res += " "
            res += expr.accept(self)
        res += ")"
        return res
