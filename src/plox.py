import sys
from pathlib import Path


class Plox:
    """The Lox interpreter class. Handles running files and REPL."""

    hadError = False

    def run_file(self, path: Path) -> int:
        """Runs a Plox script from a file."""
        try:
            lines = Path.read_text(path, encoding="utf8")
        except FileNotFoundError:
            print(f"error: file not found: {path}", file=sys.stderr)
            return 1
        self._run(lines)

        if Plox.hadError:
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
        tokens = source.split()
        for token in tokens:
            print(token)

    @staticmethod
    def error(line: int, message: str) -> None:
        """Reports an error at a specific line."""
        Plox._report(line, "", message)

    @staticmethod
    def _report(line: int, where: str, message: str) -> None:
        """Reports an error with line number and message."""
        print(f"[line {line} Error{where} : {message}]", file=sys.stderr)
        Plox.hadError = True
