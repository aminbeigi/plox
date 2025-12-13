import sys
from pathlib import Path

from src.plox import Plox
from src.constants import EX_USAGE


def main() -> int:
    """Entry point for the Plox interpreter."""
    if len(sys.argv) > 2:
        print("Usage: plox [script]", file=sys.stderr)
        return EX_USAGE
    elif len(sys.argv) == 2:
        plox = Plox()
        path = Path(sys.argv[1])
        return plox.run_file(path)
    else:
        plox = Plox()
        return plox.run_prompt()


if __name__ == "__main__":
    sys.exit(main())
