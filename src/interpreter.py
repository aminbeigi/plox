from src.expr import (
    AssignExpr,
    BinaryExpr,
    GroupingExpr,
    LiteralExpr,
    UnaryExpr,
    Expr,
    VariableExpr,
)
from src.token_type import TokenType
from src.token import Token
from src.exceptions import PloxRuntimeError
from collections.abc import Callable
from src.stmt import BlockStmt, Stmt, ExpressionStmt, PrintStmt, VarStmt, IfStmt
from src.environment import Environment


class Interpreter(Expr.Visitor[object], Stmt.Visitor[None]):
    def __init__(self) -> None:
        self._environment = Environment()

    def interpret(
        self, statements: list[Stmt], error_reporter: Callable[[PloxRuntimeError], None]
    ) -> None:
        try:
            for statement in statements:
                self._execute(statement)
        except PloxRuntimeError as error:
            error_reporter(error)

    def visit_var_stmt(self, stmt: VarStmt) -> None:
        value: object | None = None
        if stmt.initializer is not None:
            value = self._evaluate(stmt.initializer)

        self._environment.define(stmt.name.lexeme, value)

    def visit_variable_expr(self, expr: VariableExpr) -> object:
        return self._environment.get(expr.name)

    def visit_expression_stmt(self, stmt: ExpressionStmt) -> None:
        self._evaluate(stmt.expression)

    def visit_print_stmt(self, stmt: PrintStmt) -> None:
        value = self._evaluate(stmt.expression)
        print(self._stringify(value))

    def visit_if_stmt(self, stmt: IfStmt) -> None:
        if self._is_truthy(self._evaluate(stmt.condition)):
            self._execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self._execute(stmt.else_branch)

    def visit_assign_expr(self, expr: AssignExpr) -> object:
        value = self._evaluate(expr.value)
        self._environment.assign(expr.name, value)
        return value

    def visit_binary_expr(self, expr: BinaryExpr) -> object:
        """Evaluate a binary expression."""
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)

        match expr.operator.type:
            case TokenType.GREATER:
                self._check_number_operands(expr.operator, left, right)
                assert isinstance(left, float)
                assert isinstance(right, float)
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                self._check_number_operands(expr.operator, left, right)
                assert isinstance(left, float)
                assert isinstance(right, float)
                return float(left) >= float(right)
            case TokenType.LESS:
                self._check_number_operands(expr.operator, left, right)
                assert isinstance(left, float)
                assert isinstance(right, float)
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                self._check_number_operands(expr.operator, left, right)
                assert isinstance(left, float)
                assert isinstance(right, float)
                return float(left) <= float(right)
            case TokenType.BANG_EQUAL:
                return not self._is_equal(left, right)
            case TokenType.EQUAL_EQUAL:
                return self._is_equal(left, right)
            case TokenType.MINUS:
                self._check_number_operands(expr.operator, left, right)
                assert isinstance(left, float)
                assert isinstance(right, float)
                return float(left) - float(right)
            case TokenType.PLUS:
                if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                    return float(left) + float(right)
                elif isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)
                else:
                    raise PloxRuntimeError(
                        expr.operator, "Operands must be two numbers or two strings."
                    )
            case TokenType.SLASH:
                self._check_number_operands(expr.operator, left, right)
                assert isinstance(left, float)
                assert isinstance(right, float)
                return float(left) / float(right)
            case TokenType.STAR:
                self._check_number_operands(expr.operator, left, right)
                assert isinstance(left, float)
                assert isinstance(right, float)
                return float(left) * float(right)

        return None  # unreachable

    def visit_grouping_expr(self, expr: GroupingExpr) -> object:
        """Evaluate a grouping expression (parentheses)."""
        return self._evaluate(expr.expression)

    def visit_unary_expr(self, expr: UnaryExpr) -> object:
        """Evaluate a unary expression."""
        right = self._evaluate(expr.right)

        match expr.operator.type:
            case TokenType.BANG:
                return not self._is_truthy(right)
            case TokenType.MINUS:
                self._check_number_operand(expr.operator, right)
                assert isinstance(right, float)
                return -float(right)

        return None  # unreachable

    def visit_literal_expr(self, expr: LiteralExpr) -> object:
        """Evaluate a literal expression."""
        return expr.value

    def _stringify(self, obj: object) -> str:
        """Convert a Lox value to its string representation."""
        if obj is None:
            return "nil"

        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0"):
                text = text[0 : len(text) - 2]
            return text

        return str(obj)

    def _execute(self, statement: Stmt) -> None:
        statement.accept(self)

    def visit_block_stmt(self, stmt: BlockStmt) -> None:
        self._execute_block(stmt.statements, Environment(self._environment))

    def _execute_block(self, statements: list[Stmt], environment: Environment) -> None:
        previous = self._environment
        try:
            self._environment = environment
            for statement in statements:
                self._execute(statement)

        finally:
            self._environment = previous

    def _evaluate(self, expr: Expr) -> object:
        """Evaluate an expression using the visitor pattern."""
        return expr.accept(self)

    def _is_truthy(self, object: object) -> bool:
        """Determine if a value is truthy in Lox."""
        if object is None:
            return False
        if isinstance(object, bool):
            return bool(object)
        return True

    def _is_equal(self, object_a: object, object_b: object) -> bool:
        """Test if two values are equal in Lox."""
        if object_a is None and object_b is None:
            return True
        if object_a is None:
            return False
        return object_a == object_b

    def _check_number_operand(self, operator: Token, operand: object) -> None:
        """Check that an operand is a number for unary operations."""
        if isinstance(operand, (int, float)):
            return
        raise PloxRuntimeError(operator, "Operand must be a number.")

    def _check_number_operands(
        self, operator: Token, left: object, right: object
    ) -> None:
        """Check that both operands are numbers for binary operations."""
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return
        raise PloxRuntimeError(operator, "Operands must be numbers.")
