import sys
from pathlib import Path

from src.plox import Plox

# Exit codes following Unix conventions
EX_USAGE = 64  # Command line usage error


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
