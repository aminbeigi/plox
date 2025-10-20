import sys
from pathlib import Path

from lox import Lox


def main() -> int:
    if len(sys.argv) > 2:
        print("Usage: plox [script]", file=sys.stderr)
        return 64  # EX_USAGE
    elif len(sys.argv) == 2:
        lox = Lox()
        path = Path(sys.argv[1])
        return lox.run_file(path)
    else:
        lox = Lox()
        return lox.run_prompt()


if __name__ == "__main__":
    sys.exit(main())
