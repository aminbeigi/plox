# plox

A Python implementation of the Lox programming language interpreter using the tree-walking interpretation method, following the book "Crafting Interpreters" by Robert Nystrom.

## Getting Started

These instructions will help you set up and run the Plox interpreter on your local machine.

### Prerequisites

- Python 3.14 or higher
- [uv](https://github.com/astral-sh/uv) package manager version 0.9.4 or higher

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

## Implementation Notes

This interpreter follows the tree-walking approach:

1. **Scanning**: Source code is tokenized into a stream of tokens
2. **Parsing**: Tokens are parsed into an Abstract Syntax Tree (AST) using recursive descent
3. **Interpretation**: The AST is evaluated directly using the visitor pattern

### Current Progress

**A Tree-Walk Interpreter**
- ✅ Chapter 4: Scanning
- ✅ Chapter 5: Representing Code  
- ✅ Chapter 6: Parsing Expressions
- ✅ Chapter 7: Evaluating Expressions
- ✅ Chapter 8: Statements and State
- ✅ Chapter 9: Control Flow
- 🚧 Chapter 10: Functions (function calls implemented, declarations in progress)
- ⏳ Chapter 11: Resolving and Binding
- ⏳ Chapter 12: Classes  
- ⏳ Chapter 13: Inheritance


## Built With

* [Python](https://www.python.org/) - Programming language
* [pytest](https://pytest.org/) - Testing framework
* [uv](https://github.com/astral-sh/uv) - Package manager
* [ruff](https://github.com/astral-sh/ruff) - Python linter and formatter

## Authors

* **Amin Beigi** - [aminbeigi](https://github.com/aminbeigi)

## Acknowledgments

* Based on "Crafting Interpreters" by Robert Nystrom
* https://craftinginterpreters.com/
