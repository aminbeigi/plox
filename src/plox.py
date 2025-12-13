import sys
from pathlib import Path
from src.token import Token
from src.token_type import TokenType
from src.scanner import Scanner
from src.parser import Parser
from src.exceptions import PloxRuntimeError
from src.interpreter import Interpreter
from src.constants import EX_DATAERR, EX_SOFTWARE


class Plox:
    """The Lox interpreter class. Handles running files and REPL."""

    def __init__(self):
        self._had_error = False
        self._had_runtime_error = False
        self._interpreter = Interpreter()

    def run_file(self, path: Path) -> int:
        """Runs a Plox script from a file."""
        try:
            lines = Path.read_text(path, encoding="utf8")
        except FileNotFoundError:
            print(f"error: file not found: {path}", file=sys.stderr)
            return 1
        self._run(lines)

        if self._had_error:
            return EX_DATAERR

        if self._had_runtime_error:
            return EX_SOFTWARE
        return 0

    def run_prompt(self) -> int:
        """Runs the Plox REPL (Read-Eval-Print Loop)."""
        while True:
            try:
                line = input("> ")
            except EOFError:
                print()
                break
            except KeyboardInterrupt:
                print()
                break
            self._run(line)
        return 0

    def _run(self, source: str) -> None:
        """Runs the given source code."""
        scanner = Scanner(source, self._error_line)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens, self._error)
        expression = parser.parse()
        if self._had_error:
            return
        assert expression is not None
        self._interpreter.interpret(expression, self._runtime_error)

    def _error(self, token: Token, message: str) -> None:
        """Reports an error at a specific token."""
        if token.type == TokenType.EOF:
            self._report(token.line, " at end", message)
        else:
            self._report(token.line, f" at '{token.lexeme}'", message)

    def _error_line(self, line: int, message: str) -> None:
        """Reports an error at a specific line (for scanner errors)."""
        self._report(line, "", message)

    def _runtime_error(self, error: PloxRuntimeError) -> None:
        print(f"{error.message}\n[line {error.token.line}]", file=sys.stderr)
        self._had_runtime_error = True

    def _report(self, line: int, where: str, message: str) -> None:
        """Reports an error with line number and message."""
        print(f"[line {line} Error{where} : {message}]", file=sys.stderr)
        self._had_error = True
