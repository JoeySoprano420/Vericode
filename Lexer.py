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
    EOF = auto()
