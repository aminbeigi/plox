import sys
from pathlib import Path
from src.token import Token
from src.token_type import TokenType
from src.scanner import Scanner
from src.parser import Parser
from src.ast_printer import AstPrinter


class Plox:
    """The Lox interpreter class. Handles running files and REPL."""

    had_error = False

    def run_file(self, path: Path) -> int:
        """Runs a Plox script from a file."""
        try:
            lines = Path.read_text(path, encoding="utf8")
        except FileNotFoundError:
            print(f"error: file not found: {path}", file=sys.stderr)
            return 1
        self._run(lines)

        if Plox.had_error:
            return 1
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
        scanner = Scanner(source, Plox.error_line)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens, Plox.error)
        expression = parser.parse()
        if self.had_error:
            return

        if expression is not None:
            astPrinter = AstPrinter()
            print(astPrinter.print(expression))

    @staticmethod
    def error(token: Token, message: str) -> None:
        """Reports an error at a specific token."""
        if token.type == TokenType.EOF:
            Plox._report(token.line, " at end", message)
        else:
            Plox._report(token.line, f" at '{token.lexeme}'", message)

    @staticmethod
    def error_line(line: int, message: str) -> None:
        """Reports an error at a specific line (for scanner errors)."""
        Plox._report(line, "", message)

    @staticmethod
    def _report(line: int, where: str, message: str) -> None:
        """Reports an error with line number and message."""
        print(f"[line {line} Error{where} : {message}]", file=sys.stderr)
        Plox.had_error = True
