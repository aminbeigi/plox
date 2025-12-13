from src.expr import Expr

from abc import ABC, abstractmethod
from typing import Generic, TypeVar


R = TypeVar("R")


class Stmt(ABC):
    """
    Base class for all statement nodes.
    """

    class Visitor(ABC, Generic[R]):
        def visit_expression_stmt(self, stmt: Expression) -> R: ...
        def visit_print_stmt(self, stmt: Print) -> R: ...

    @abstractmethod
    def accept(self, visitor: Stmt.Visitor[R]) -> R: ...


class Expression(Stmt):
    def __init__(self, expression: Expr) -> None:
        self.expression = expression

    def accept(self, visitor: Stmt.Visitor[R]) -> R:
        return visitor.visit_expression_stmt(self)


class Print(Stmt):
    def __init__(self, expression: Expr) -> None:
        self.expression = expression

    def accept(self, visitor: Stmt.Visitor[R]) -> R:
        return visitor.visit_print_stmt(self)
