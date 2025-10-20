import sys
from pathlib import Path


class Lox:
    hadError = False

    def run_file(self, path: Path) -> int:
        try:
            lines = Path.read_text(path, encoding="utf8")
        except FileNotFoundError:
            print(f"error: file not found: {path}", file=sys.stderr)
            return 1
        self._run(lines)

        if Lox.hadError:
            return 1
        return 0

    def run_prompt(self) -> int:
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
        tokens = source.split()
        for token in tokens:
            print(token)

    @staticmethod
    def error(line: int, message: str) -> None:
        Lox.report(line, "", message)

    @staticmethod
    def report(line: int, where: str, message: str) -> None:
        print(f"[line {line} Error{where} : {message}]", file=sys.stderr)
        Lox.hadError = True
