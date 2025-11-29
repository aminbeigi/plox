from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from src.token import Token

T = TypeVar("T")


class Expr(ABC, Generic[T]):
    """Base class for all expression types."""

    @abstractmethod
    def accept(self, visitor: T) -> T:
        """Accept a visitor for the Visitor pattern."""
        pass


class BinaryExpr(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary_expr(self)


class UnaryExpr(Expr):
    def __init__(self, operator: Token, right: Expr) -> None:
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary_expr(self)


class GroupingExpr(Expr):
    def __init__(self, expression: Expr) -> None:
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_grouping_expr(self)


class LiteralExpr(Expr):
    def __init__(self, value: object) -> None:
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal_expr(self)
