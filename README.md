# plox

A Python implementation of the Lox programming language interpreter, following the book "Crafting Interpreters" by Robert Nystrom.

## Getting Started

These instructions will help you set up and run the Plox interpreter on your local machine.

### Prerequisites

- Python 3.14 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Installing

1. Clone the repository:
```bash
git clone https://github.com/aminbeigi/plox.git
cd plox
```

2. Install dependencies:
```bash
uv sync
```

3. Run the interpreter:
```bash
# Interactive REPL mode
uv run python -m src.main

# Run a Lox script file
uv run python -m src.main path/to/script.lox
```

## Running the tests

Run the test suite using pytest:

```bash
uv run pytest
```

For verbose output:
```bash
uv run pytest -v
```

Run specific tests:
```bash
uv run pytest tests/test_scanner.py
```

### Test Coverage

The test suite currently includes:
- Scanner/lexer tests for tokenizing source code
- Token equality and representation tests

## Project Structure

```
plox/
├── src/
│   ├── main.py         # Entry point
│   ├── plox.py         # Main interpreter class
│   ├── scanner.py      # Lexical scanner/tokenizer
│   ├── token.py        # Token class
│   └── token_type.py   # Token type enumeration
├── tests/
│   ├── test_scanner.py # Scanner tests
│   └── test_token.py   # Token tests
└── pyproject.toml      # Project configuration
```

## Built With

* [Python](https://www.python.org/) - Programming language
* [pytest](https://pytest.org/) - Testing framework
* [uv](https://github.com/astral-sh/uv) - Package manager

## Authors

* **Amin Beigi** - [aminbeigi](https://github.com/aminbeigi)

## Acknowledgments

* Based on "Crafting Interpreters" by Robert Nystrom
* [craftinginterpreters.com](https://craftinginterpreters.com/)
