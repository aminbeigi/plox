from collections.abc import Callable
from src.token import Token
from src.token_type import TokenType
from src.expr import Expr
from src.expr import BinaryExpr
from src.expr import UnaryExpr
from src.expr import LiteralExpr
from src.expr import GroupingExpr
from src.expr import VariableExpr
from src.expr import AssignExpr
from src.expr import LogicalExpr
from src.exceptions import ParseError
from src.stmt import Stmt, PrintStmt, ExpressionStmt, VarStmt, BlockStmt, IfStmt


class Parser:
    def __init__(
        self,
        tokens: list[Token],
        error_reporter: Callable[[Token, str], None],
    ):
        """Initialize the parser with tokens and error reporting."""
        self._tokens: list[Token] = tokens
        self._current = 0
        self._error_reporter = error_reporter

    def parse(self) -> list[Stmt]:
        statements: list[Stmt] = []
        while not self._is_at_end():
            decl = self._declaration()
            if decl is not None:
                statements.append(decl)
        return statements

    def _declaration(self) -> Stmt | None:
        try:
            if self._match(TokenType.VAR):
                return self._var_declaration()
            return self._statement()
        except ParseError:
            self._synchronize()
            return None

    def _var_declaration(self) -> Stmt:
        name = self._consume(TokenType.IDENTIFIER, "Expect variable name.")
        initalizer: Expr | None = None

        if self._match(TokenType.EQUAL):
            initalizer = self._expression()

        self._consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return VarStmt(name, initalizer)

    def _if_statement(self) -> Stmt:
        self._consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        then_branch = self._statement()
        else_branch: Stmt | None = None
        if self._match(TokenType.ELSE):
            else_branch = self._statement()

        return IfStmt(condition, then_branch, else_branch)

    def _statement(self) -> Stmt:
        if self._match(TokenType.IF):
            return self._if_statement()
        if self._match(TokenType.PRINT):
            return self._print_statement()
        if self._match(TokenType.LEFT_BRACE):
            return BlockStmt(self._block())
        return self._expression_statement()

    def _block(self) -> list[Stmt]:
        statements: list[Stmt] = []
        while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
            # TODO
            statements.append(self._declaration())  # type: ignore

        self._consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def _print_statement(self) -> Stmt:
        value = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return PrintStmt(value)

    def _expression_statement(self) -> Stmt:
        expr = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return ExpressionStmt(expr)

    def _expression(self) -> Expr:
        """Parse an expression (top-level rule)."""
        return self._assignment()

    def _assignment(self) -> Expr:
        expr = self._or()

        if self._match(TokenType.EQUAL):
            # equals = self._previous()
            value = self._assignment()

            if isinstance(expr, VariableExpr):
                name = expr.name
                return AssignExpr(name, value)

            # error(equals, "Invalid assignment target.");  # TODO

        return expr

    def _or(self) -> Expr:
        expr = self._and()

        while self._match(TokenType.OR):
            operator = self._previous()
            right = self._and()
            expr = LogicalExpr(expr, operator, right)
        return expr

    def _and(self) -> Expr:
        expr = self._equality()

        while self._match(TokenType.AND):
            operator = self._previous()
            right = self._equality()
            expr = LogicalExpr(expr, operator, right)
        return expr

    def _equality(self) -> Expr:
        """Parse equality expressions (== !=)."""
        expr = self._comparison()

        while self._match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self._previous()
            right = self._comparison()
            expr = BinaryExpr(expr, operator, right)
        return expr

    def _comparison(self) -> Expr:
        """Parse comparison expressions (> >= < <=)."""
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
        """Parse term expressions (+ -)."""
        expr = self._factor()

        while self._match(TokenType.MINUS, TokenType.PLUS):
            operator = self._previous()
            right = self._factor()
            expr = BinaryExpr(expr, operator, right)
        return expr

    def _factor(self) -> Expr:
        """Parse factor expressions (* /)."""
        expr = self._unary()

        while self._match(TokenType.SLASH, TokenType.STAR):
            operator = self._previous()
            right = self._unary()
            expr = BinaryExpr(expr, operator, right)
        return expr

    def _unary(self) -> Expr:
        """Parse unary expressions (! -)."""
        if self._match(TokenType.BANG, TokenType.MINUS):
            operator = self._previous()
            right = self._unary()
            return UnaryExpr(operator, right)
        return self._primary()

    def _primary(self) -> Expr:
        """Parse primary expressions (literals, identifiers, parentheses)."""
        if self._match(TokenType.FALSE):
            return LiteralExpr(False)
        if self._match(TokenType.TRUE):
            return LiteralExpr(True)
        if self._match(TokenType.NIL):
            return LiteralExpr(None)

        if self._match(TokenType.NUMBER, TokenType.STRING):
            return LiteralExpr(self._previous().literal)

        if self._match(TokenType.IDENTIFIER):
            return VariableExpr(self._previous())

        if self._match(TokenType.LEFT_PAREN):
            expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return GroupingExpr(expr)

        raise self._error(self._peek(), "Expect expression.")

    def _match(self, *types: TokenType):
        """Check if current token matches any of the given types."""
        for type in types:
            if self._check(type):
                self._advance()
                return True
        return False

    def _consume(self, type: TokenType, message: str) -> Token:
        """Consume a token of the expected type or report an error."""
        if self._check(type):
            return self._advance()
        raise self._error(self._peek(), message)

    def _error(self, token: Token, message: str) -> ParseError:
        """Report a parse error and return a ParseError exception."""
        self._error_reporter(token, message)
        return ParseError()

    def _synchronize(self) -> None:
        """Synchronize parser after an error by finding statement boundaries."""
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
        """Check if current token is of the given type."""
        if self._is_at_end():
            return False
        return self._peek().type == type

    def _advance(self) -> Token:
        """Advance to the next token and return the current one."""
        if not self._is_at_end():
            self._current += 1
        return self._previous()

    def _is_at_end(self) -> bool:
        """Check if we've reached the end of tokens."""
        return self._peek().type == TokenType.EOF

    def _peek(self) -> Token:
        """Return the current token without advancing."""
        return self._tokens[self._current]

    def _previous(self) -> Token:
        """Return the previously consumed token."""
        return self._tokens[self._current - 1]
