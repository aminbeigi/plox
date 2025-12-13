from collections.abc import Callable
from src.token import Token
from src.token_type import TokenType
from src.expr import Expr
from src.expr import BinaryExpr
from src.expr import UnaryExpr
from src.expr import LiteralExpr
from src.expr import GroupingExpr
from src.parse_error import ParseError


class Parser:
    def __init__(
        self,
        tokens: list[Token],
        error_reporter: Callable[[Token, str], None],
    ):
        self._tokens: list[Token] = tokens
        self._current = 0
        self._error_reporter = error_reporter

    def parse(self) -> Expr | None:
        try:
            return self._expression()
        except ParseError:
            return None

    def _expression(self) -> Expr:
        return self._equality()

    def _equality(self) -> Expr:
        expr = self._comparison()

        while self._match(TokenType.BANG_EQUAL, TokenType.BANG_EQUAL):
            operator = self._previous()
            right = self._comparison()
            expr = BinaryExpr(expr, operator, right)
        return expr

    def _comparison(self) -> Expr:
        expr = self._term()

        while self._match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            operator = self._previous()
            right = self._term()
            expr = BinaryExpr(expr, operator, right)
        return expr

    def _term(self) -> Expr:
        expr = self._factor()

        while self._match(TokenType.MINUS, TokenType.PLUS):
            operator = self._previous()
            right = self._factor()
            expr = BinaryExpr(expr, operator, right)
        return expr

    def _factor(self) -> Expr:
        expr = self._unary()

        while self._match(TokenType.SLASH, TokenType.STAR):
            operator = self._previous()
            right = self._unary()
            expr = BinaryExpr(expr, operator, right)
        return expr

    def _unary(self) -> Expr:
        if self._match(TokenType.BANG, TokenType.MINUS):
            operator = self._previous()
            right = self._unary()
            return UnaryExpr(operator, right)
        return self._primary()

    def _primary(self) -> Expr:
        if self._match(TokenType.FALSE):
            return LiteralExpr(False)
        if self._match(TokenType.TRUE):
            return LiteralExpr(True)
        if self._match(TokenType.NIL):
            return LiteralExpr(None)

        if self._match(TokenType.NUMBER, TokenType.STRING):
            return LiteralExpr(self._previous().literal)

        if self._match(TokenType.LEFT_PAREN):
            expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return GroupingExpr(expr)

        raise self._error(self._peek(), "Expect expression.")

    def _match(self, *types: TokenType):
        for type in types:
            if self._check(type):
                self._advance()
                return True
        return False

    def _consume(self, type: TokenType, message: str) -> Token:
        if self._check(type):
            return self._advance()
        raise self._error(self._peek(), message)

    def _error(self, token: Token, message: str) -> ParseError:
        self._error_reporter(token, message)
        return ParseError()

    def _synchronize(self) -> None:
        self._advance()

        while not self._is_at_end():
            if self._previous().type == TokenType.SEMICOLON:
                return

            match self._peek().type:
                case TokenType.CLASS:
                    return
                case TokenType.FUN:
                    return
                case TokenType.VAR:
                    return
                case TokenType.FOR:
                    return
                case TokenType.IF:
                    return
                case TokenType.WHILE:
                    return
                case TokenType.PRINT:
                    return
                case TokenType.RETURN:
                    return
            self._advance()

    def _check(self, type: TokenType) -> bool:
        if self._is_at_end():
            return False
        return self._peek().type == type

    def _advance(self) -> Token:
        if not self._is_at_end():
            self._current += 1
        return self._previous()

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _peek(self) -> Token:
        return self._tokens[self._current]

    def _previous(self) -> Token:
        return self._tokens[self._current - 1]
