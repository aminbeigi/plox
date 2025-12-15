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
        def visit_expression_stmt(self, stmt: ExpressionStmt) -> R: ...
        @abstractmethod
        def visit_print_stmt(self, stmt: PrintStmt) -> R: ...
        @abstractmethod
        def visit_var_stmt(self, stmt: VarStmt) -> R: ...
        @abstractmethod
        def visit_block_stmt(self, stmt: BlockStmt) -> R: ...

    @abstractmethod
    def accept(self, visitor: Stmt.Visitor[R]) -> R: ...


class ExpressionStmt(Stmt):
    def __init__(self, expression: Expr) -> None:
        self.expression = expression

    def accept(self, visitor: Stmt.Visitor[R]) -> R:
        return visitor.visit_expression_stmt(self)


class PrintStmt(Stmt):
    def __init__(self, expression: Expr) -> None:
        self.expression = expression

    def accept(self, visitor: Stmt.Visitor[R]) -> R:
        return visitor.visit_print_stmt(self)


class VarStmt(Stmt):
    def __init__(self, name: Token, initializer: Expr | None) -> None:
        self.name = name
        self.initializer = initializer

    def accept(self, visitor: Stmt.Visitor[R]) -> R:
        return visitor.visit_var_stmt(self)


class BlockStmt(Stmt):
    def __init__(self, statements: list[Stmt]) -> None:
        self.statements = statements

    def accept(self, visitor: Stmt.Visitor[R]) -> R:
        return visitor.visit_block_stmt(self)
