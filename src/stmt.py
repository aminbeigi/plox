from src.expr import Expr
from src.token import Token

from abc import ABC, abstractmethod
from typing import Generic, TypeVar


R = TypeVar("R")


class Stmt(ABC):
    """
    Base class for all statement nodes.
    """

    class Visitor(ABC, Generic[R]):
        @abstractmethod
        def visit_expression_stmt(self, stmt: Expression) -> R: ...
        @abstractmethod
        def visit_print_stmt(self, stmt: Print) -> R: ...
        @abstractmethod
        def visit_var_stmt(self, stmt: Var) -> R: ...

    @abstractmethod
    def accept(self, visitor: Stmt.Visitor[R]) -> R: ...


class Expression(Stmt):
    def __init__(self, expression: Expr) -> None:
        self.expression = expression

    def accept(self, visitor: Stmt.Visitor[R]) -> R:
        return visitor.visit_expression_stmt(self)


class Print(Stmt):
    def __init__(self, expression: Expr) -> None:
        self._expression = expression

    def accept(self, visitor: Stmt.Visitor[R]) -> R:
        return visitor.visit_print_stmt(self)


class Var(Stmt):
    def __init__(self, name: Token, initializer: Expr | None) -> None:
        self._name = name
        self._initializer = initializer

    def accept(self, visitor: Stmt.Visitor[R]) -> R:
        return visitor.visit_var_stmt(self)
