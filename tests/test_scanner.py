from src.scanner import Scanner
from src.token import Token
from src.token_type import TokenType


def test_scan_empty_source():
    scanner = Scanner(source="")
    tokens = scanner.scan_tokens()
    assert len(tokens) == 1
    assert tokens[0] == Token(TokenType.EOF, "", None, 1)


def test_scan_number():
    scanner = Scanner(source="10")
    tokens = scanner.scan_tokens()
    assert len(tokens) == 2

    assert tokens[0] == Token(TokenType.NUMBER, "10", 10.0, 1)
    assert tokens[1] == Token(TokenType.EOF, "", None, 1)


def test_scan_variable_assignment():
    scanner = Scanner(source="var x = 25;")
    tokens = scanner.scan_tokens()
    assert len(tokens) == 6
    assert tokens[0] == Token(TokenType.VAR, "var", None, 1)
    assert tokens[1] == Token(TokenType.IDENTIFIER, "x", None, 1)
    assert tokens[2] == Token(TokenType.EQUAL, "=", None, 1)
    assert tokens[3] == Token(TokenType.NUMBER, "25", 25.0, 1)
    assert tokens[4] == Token(TokenType.SEMICOLON, ";", None, 1)
    assert tokens[5] == Token(TokenType.EOF, "", None, 1)


def test_scan_string():
    scanner = Scanner(source='"hello, woRLD!"')
    tokens = scanner.scan_tokens()
    assert len(tokens) == 2
    assert tokens[0] == Token(TokenType.STRING, '"hello, woRLD!"', "hello, woRLD!", 1)
    assert tokens[1] == Token(TokenType.EOF, "", None, 1)


def test_scan_comparision():
    scanner = Scanner(source="a != b == c < d")
    tokens = scanner.scan_tokens()
    assert len(tokens) == 8
    assert tokens[0] == Token(TokenType.IDENTIFIER, "a", None, 1)
    assert tokens[1] == Token(TokenType.BANG_EQUAL, "!=", None, 1)
    assert tokens[2] == Token(TokenType.IDENTIFIER, "b", None, 1)
    assert tokens[3] == Token(TokenType.EQUAL_EQUAL, "==", None, 1)
    assert tokens[4] == Token(TokenType.IDENTIFIER, "c", None, 1)
    assert tokens[5] == Token(TokenType.LESS, "<", None, 1)
    assert tokens[6] == Token(TokenType.IDENTIFIER, "d", None, 1)
    assert tokens[7] == Token(TokenType.EOF, "", None, 1)


def test_scan_brackets_and_braces():
    scanner = Scanner(source="{}()")
    tokens = scanner.scan_tokens()
    assert len(tokens) == 5
    assert tokens[0] == Token(TokenType.LEFT_BRACE, "{", None, 1)
    assert tokens[1] == Token(TokenType.RIGHT_BRACE, "}", None, 1)
    assert tokens[2] == Token(TokenType.LEFT_PAREN, "(", None, 1)
    assert tokens[3] == Token(TokenType.RIGHT_PAREN, ")", None, 1)
    assert tokens[4] == Token(TokenType.EOF, "", None, 1)


def test_scan_all_keywords():
    keywords = [
        "and",
        "class",
        "else",
        "false",
        "for",
        "fun",
        "if",
        "nil",
        "or",
        "print",
        "return",
        "super",
        "this",
        "true",
        "var",
        "while",
    ]
    source = " ".join(keywords)
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    # Should have all keyword tokens plus EOF
    assert len(tokens) == len(keywords) + 1

    expected_types = [
        TokenType.AND,
        TokenType.CLASS,
        TokenType.ELSE,
        TokenType.FALSE,
        TokenType.FOR,
        TokenType.FUN,
        TokenType.IF,
        TokenType.NIL,
        TokenType.OR,
        TokenType.PRINT,
        TokenType.RETURN,
        TokenType.SUPER,
        TokenType.THIS,
        TokenType.TRUE,
        TokenType.VAR,
        TokenType.WHILE,
    ]

    for i, expected_type in enumerate(expected_types):
        assert tokens[i].type == expected_type
        assert tokens[i].lexeme == keywords[i]
        assert tokens[i].literal is None
        assert tokens[i].line == 1


def test_scan_all_operators():
    scanner = Scanner(source="+ - * / = == != < <= > >= ! , . ;")
    tokens = scanner.scan_tokens()

    expected_types = [
        TokenType.PLUS,
        TokenType.MINUS,
        TokenType.STAR,
        TokenType.SLASH,
        TokenType.EQUAL,
        TokenType.EQUAL_EQUAL,
        TokenType.BANG_EQUAL,
        TokenType.LESS,
        TokenType.LESS_EQUAL,
        TokenType.GREATER,
        TokenType.GREATER_EQUAL,
        TokenType.BANG,
        TokenType.COMMA,
        TokenType.DOT,
        TokenType.SEMICOLON,
    ]

    assert len(tokens) == len(expected_types) + 1  # +1 for EOF

    for i, expected_type in enumerate(expected_types):
        assert tokens[i].type == expected_type


def test_scan_decimal_numbers():
    scanner = Scanner(source="123.456 0.5 999.999")
    tokens = scanner.scan_tokens()

    assert len(tokens) == 4  # 3 numbers + EOF
    assert tokens[0] == Token(TokenType.NUMBER, "123.456", 123.456, 1)
    assert tokens[1] == Token(TokenType.NUMBER, "0.5", 0.5, 1)
    assert tokens[2] == Token(TokenType.NUMBER, "999.999", 999.999, 1)
    assert tokens[3] == Token(TokenType.EOF, "", None, 1)


def test_scan_identifiers():
    scanner = Scanner(source="variable _private myVar123 some_function")
    tokens = scanner.scan_tokens()

    assert len(tokens) == 5  # 4 identifiers + EOF
    assert tokens[0] == Token(TokenType.IDENTIFIER, "variable", None, 1)
    assert tokens[1] == Token(TokenType.IDENTIFIER, "_private", None, 1)
    assert tokens[2] == Token(TokenType.IDENTIFIER, "myVar123", None, 1)
    assert tokens[3] == Token(TokenType.IDENTIFIER, "some_function", None, 1)
    assert tokens[4] == Token(TokenType.EOF, "", None, 1)


def test_scan_comments():
    scanner = Scanner(source="var x = 5; // This is a comment\nvar y = 10;")
    tokens = scanner.scan_tokens()

    # Should skip the comment and parse the two variable declarations
    assert len(tokens) == 11  # var x = 5 ; var y = 10 ; EOF
    assert tokens[0] == Token(TokenType.VAR, "var", None, 1)
    assert tokens[1] == Token(TokenType.IDENTIFIER, "x", None, 1)
    assert tokens[2] == Token(TokenType.EQUAL, "=", None, 1)
    assert tokens[3] == Token(TokenType.NUMBER, "5", 5.0, 1)
    assert tokens[4] == Token(TokenType.SEMICOLON, ";", None, 1)
    assert tokens[5] == Token(TokenType.VAR, "var", None, 2)
    assert tokens[6] == Token(TokenType.IDENTIFIER, "y", None, 2)
    assert tokens[7] == Token(TokenType.EQUAL, "=", None, 2)
    assert tokens[8] == Token(TokenType.NUMBER, "10", 10.0, 2)
    assert tokens[9] == Token(TokenType.SEMICOLON, ";", None, 2)
    assert tokens[10] == Token(TokenType.EOF, "", None, 2)


def test_scan_multiline_string():
    scanner = Scanner(source='"hello\nworld"')
    tokens = scanner.scan_tokens()

    assert len(tokens) == 2
    assert tokens[0] == Token(TokenType.STRING, '"hello\nworld"', "hello\nworld", 2)
    assert tokens[1] == Token(TokenType.EOF, "", None, 2)


def test_scan_whitespace_handling():
    scanner = Scanner(source="  var\t  x\r\n=\n  5  ")
    tokens = scanner.scan_tokens()

    assert len(tokens) == 5  # var x = 5 EOF
    assert tokens[0] == Token(TokenType.VAR, "var", None, 1)
    assert tokens[1] == Token(TokenType.IDENTIFIER, "x", None, 1)
    assert tokens[2] == Token(TokenType.EQUAL, "=", None, 2)
    assert tokens[3] == Token(TokenType.NUMBER, "5", 5.0, 3)
    assert tokens[4] == Token(TokenType.EOF, "", None, 3)


def test_scan_keyword_vs_identifier():
    # Test that keywords are recognized correctly vs similar identifiers
    scanner = Scanner(source="if iffy var variable true truthy")
    tokens = scanner.scan_tokens()

    assert len(tokens) == 7  # 6 tokens + EOF
    assert tokens[0] == Token(TokenType.IF, "if", None, 1)
    assert tokens[1] == Token(TokenType.IDENTIFIER, "iffy", None, 1)
    assert tokens[2] == Token(TokenType.VAR, "var", None, 1)
    assert tokens[3] == Token(TokenType.IDENTIFIER, "variable", None, 1)
    assert tokens[4] == Token(TokenType.TRUE, "true", None, 1)
    assert tokens[5] == Token(TokenType.IDENTIFIER, "truthy", None, 1)
    assert tokens[6] == Token(TokenType.EOF, "", None, 1)


def test_scan_complex_expression():
    # Test a more complex expression
    scanner = Scanner(
        source="fun fibonacci(n) {\n  if (n <= 1) return n;\n  return fibonacci(n - 1) + fibonacci(n - 2);\n}"
    )
    tokens = scanner.scan_tokens()

    # Check that we have the right number of tokens and some key ones
    assert len(tokens) > 20  # Should be many tokens
    assert tokens[0] == Token(TokenType.FUN, "fun", None, 1)
    assert tokens[1] == Token(TokenType.IDENTIFIER, "fibonacci", None, 1)
    assert tokens[2] == Token(TokenType.LEFT_PAREN, "(", None, 1)
    # Check that line numbers are correctly tracked
    assert any(token.line == 2 for token in tokens)
    assert any(token.line == 3 for token in tokens)
    assert any(token.line == 4 for token in tokens)


def test_scan_empty_string():
    scanner = Scanner(source='""')
    tokens = scanner.scan_tokens()

    assert len(tokens) == 2
    assert tokens[0] == Token(TokenType.STRING, '""', "", 1)
    assert tokens[1] == Token(TokenType.EOF, "", None, 1)


def test_scan_single_line_comment_at_end():
    scanner = Scanner(source="var x = 5; // comment at end")
    tokens = scanner.scan_tokens()

    # Should scan everything before the comment
    assert len(tokens) == 6
    assert tokens[0] == Token(TokenType.VAR, "var", None, 1)
    assert tokens[1] == Token(TokenType.IDENTIFIER, "x", None, 1)
    assert tokens[2] == Token(TokenType.EQUAL, "=", None, 1)
    assert tokens[3] == Token(TokenType.NUMBER, "5", 5.0, 1)
    assert tokens[4] == Token(TokenType.SEMICOLON, ";", None, 1)
    assert tokens[5] == Token(TokenType.EOF, "", None, 1)


def test_scan_number_edge_cases():
    # Test various number formats
    scanner = Scanner(source="0 0.0 123 123.0 0.123")
    tokens = scanner.scan_tokens()

    assert len(tokens) == 6  # 5 numbers + EOF
    assert tokens[0] == Token(TokenType.NUMBER, "0", 0.0, 1)
    assert tokens[1] == Token(TokenType.NUMBER, "0.0", 0.0, 1)
    assert tokens[2] == Token(TokenType.NUMBER, "123", 123.0, 1)
    assert tokens[3] == Token(TokenType.NUMBER, "123.0", 123.0, 1)
    assert tokens[4] == Token(TokenType.NUMBER, "0.123", 0.123, 1)
