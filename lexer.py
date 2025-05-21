import re
from enum import Enum, auto

class TokenType(Enum):
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    BOOL = auto()
    OPERATOR = auto()
    ASSIGN = auto()
    KEYWORD = auto()
    SYMBOL = auto()
    NEWLINE = auto()
    EOF = auto()

KEYWORDS = {
    "init", "make", "structure", "return", "check", "else", "while", "for",
    "await", "go", "sync", "throws", "excepts", "verify", "assert", "truth",
    "proof", "attach", "detach", "link", "in", "out", "checkpoint", "true", "false"
}

OPERATORS = {
    "+", "-", "*", "/", "%", "^", "==", "!=", "<", ">", "<=", ">=",
    "and", "or", "xor", "not", "="
}

SYMBOLS = { "(", ")", "{", "}", "[", "]", ",", ":", "|", ";", "#" }

class Token:
    def __init__(self, type_, value, line, col):
        self.type = type_
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        return f"{self.type.name}({self.value}) @ {self.line}:{self.col}"

class Lexer:
    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1
        self.length = len(source)

    def peek(self):
        return self.source[self.pos] if self.pos < self.length else ''

    def advance(self):
        c = self.peek()
        self.pos += 1
        self.col += 1
        if c == '\n':
            self.line += 1
            self.col = 1
        return c

    def next_token(self):
        while self.pos < self.length:
            c = self.peek()

            # Skip whitespace
            if c.isspace():
                self.advance()
                continue

            # Identifiers / keywords / boolean
            if c.isalpha() or c == '_':
                return self.identifier()

            # Numbers
            if c.isdigit():
                return self.number()

            # Strings
            if c == '"':
                return self.string()

            # Comments
            if c == '/' and self._peek_ahead(1) == '/':
                while self.peek() != '\n' and self.pos < self.length:
                    self.advance()
                continue

            # Operators
            for op in sorted(OPERATORS, key=lambda x: -len(x)):
                if self.source.startswith(op, self.pos):
                    self._consume(len(op))
                    return Token(TokenType.OPERATOR if op != '=' else TokenType.ASSIGN, op, self.line, self.col)

            # Symbols
            if c in SYMBOLS:
                self.advance()
                return Token(TokenType.SYMBOL, c, self.line, self.col)

            raise SyntaxError(f"Unknown character: '{c}' at {self.line}:{self.col}")

        return Token(TokenType.EOF, 'EOF', self.line, self.col)

    def identifier(self):
        start = self.pos
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()
        word = self.source[start:self.pos]
        if word in KEYWORDS:
            return Token(TokenType.KEYWORD if word not in {"true", "false"} else TokenType.BOOL, word, self.line, self.col)
        return Token(TokenType.IDENTIFIER, word, self.line, self.col)

    def number(self):
        start = self.pos
        while self.peek().isdigit() or self.peek() == '.':
            self.advance()
        return Token(TokenType.NUMBER, self.source[start:self.pos], self.line, self.col)

    def string(self):
        self.advance()  # skip opening quote
        result = ''
        while self.peek() != '"' and self.pos < self.length:
            result += self.advance()
        self.advance()  # skip closing quote
        return Token(TokenType.STRING, result, self.line, self.col)

    def _peek_ahead(self, n):
        return self.source[self.pos + n] if self.pos + n < self.length else ''

    def _consume(self, n):
        for _ in range(n):
            self.advance()
