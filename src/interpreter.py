from src.expr import BinaryExpr, GroupingExpr, LiteralExpr, UnaryExpr, Expr
from src.visitor import Visitor
from src.token_type import TokenType
from src.token import Token
from src.exceptions import PloxRuntimeError
from collections.abc import Callable


class Interpreter(Visitor[object]):
    def interpret(
        self, expression: Expr, error_reporter: Callable[[PloxRuntimeError], None]
    ) -> None:
        try:
            value = self._evaluate(expression)
            print(self._stringify(value))
        except PloxRuntimeError as error:
            error_reporter(error)

    def _stringify(self, obj: object) -> str:
        if obj is None:
            return "nil"

        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0"):
                text = text[0 : len(text) - 2]
            return text

        return str(obj)

    def visit_binary_expr(self, expr: BinaryExpr) -> object:
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
        return self._evaluate(expr.expression)

    def visit_unary_expr(self, expr: UnaryExpr) -> object:
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
        return expr.value

    def _evaluate(self, expr: Expr) -> object:
        return expr.accept(self)

    def _is_truthy(self, object: object) -> bool:
        if object is None:
            return False
        if isinstance(object, bool):
            return bool(object)
        return True

    def _is_equal(self, object_a: object, object_b: object) -> bool:
        if object_a is None and object_b is None:
            return True
        if object_a is None:
            return False
        return object_a == object_b

    def _check_number_operand(self, operator: Token, operand: object) -> None:
        if isinstance(operand, (int, float)):
            return
        raise PloxRuntimeError(operator, "Operand must be a number.")

    def _check_number_operands(
        self, operator: Token, left: object, right: object
    ) -> None:
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return
        raise PloxRuntimeError(operator, "Operands must be numbers.")
