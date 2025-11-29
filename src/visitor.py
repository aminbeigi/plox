from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from src.expr import BinaryExpr, GroupingExpr, LiteralExpr, UnaryExpr


T = TypeVar("T")


class Visitor(ABC, Generic[T]):
    """Visitor interface for expression nodes."""

    @abstractmethod
    def visit_binary_expr(self, expr: BinaryExpr) -> T:
        pass

    @abstractmethod
    def visit_literal_expr(self, expr: LiteralExpr) -> T:
        pass

    @abstractmethod
    def visit_grouping_expr(self, expr: GroupingExpr) -> T:
        pass

    @abstractmethod
    def visit_unary_expr(self, expr: UnaryExpr) -> T:
        pass
