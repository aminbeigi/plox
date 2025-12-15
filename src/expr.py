from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from src.token import Token


T = TypeVar("T")


class Expr(ABC):
    """Base class for all expression types."""

    class Visitor(ABC, Generic[T]):
        """Visitor interface for expression nodes."""

        @abstractmethod
        def visit_assign_expr(self, expr: AssignExpr) -> T: ...

        @abstractmethod
        def visit_binary_expr(self, expr: BinaryExpr) -> T: ...

        @abstractmethod
        def visit_grouping_expr(self, expr: GroupingExpr) -> T: ...

        @abstractmethod
        def visit_unary_expr(self, expr: UnaryExpr) -> T: ...

        @abstractmethod
        def visit_literal_expr(self, expr: LiteralExpr) -> T: ...

        @abstractmethod
        def visit_logical_expr(self, expr: LogicalExpr) -> T: ...

        @abstractmethod
        def visit_variable_expr(self, expr: VariableExpr) -> T: ...

    @abstractmethod
    def accept(self, visitor: Visitor[T]) -> T: ...


class AssignExpr(Expr):
    def __init__(self, name: Token, value: Expr) -> None:
        self.name = name
        self.value = value

    def accept(self, visitor: Expr.Visitor[T]) -> T:
        return visitor.visit_assign_expr(self)


class BinaryExpr(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: Expr.Visitor[T]) -> T:
        return visitor.visit_binary_expr(self)


class UnaryExpr(Expr):
    def __init__(self, operator: Token, right: Expr) -> None:
        self.operator = operator
        self.right = right

    def accept(self, visitor: Expr.Visitor[T]) -> T:
        return visitor.visit_unary_expr(self)


class GroupingExpr(Expr):
    def __init__(self, expression: Expr) -> None:
        self.expression = expression

    def accept(self, visitor: Expr.Visitor[T]) -> T:
        return visitor.visit_grouping_expr(self)


class LiteralExpr(Expr):
    def __init__(self, value: object) -> None:
        self.value = value

    def accept(self, visitor: Expr.Visitor[T]) -> T:
        return visitor.visit_literal_expr(self)


class LogicalExpr(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: Expr.Visitor[T]) -> T:
        return visitor.visit_logical_expr(self)


class VariableExpr(Expr):
    def __init__(self, name: Token) -> None:
        self.name = name

    def accept(self, visitor: Expr.Visitor[T]) -> T:
        return visitor.visit_variable_expr(self)
