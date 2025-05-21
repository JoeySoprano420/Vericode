from lexer import Lexer
from ast_nodes import *

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current = self.lexer.next_token()

    def eat(self, token_type):
        if self.current.type == token_type:
            self.current = self.lexer.next_token()
        else:
            raise SyntaxError(f"Expected {token_type}, got {self.current.type}")

    def parse(self):
        statements = []
        while self.current.type != TokenType.EOF:
            statements.append(self.statement())
        return Program(statements)

    def statement(self):
        if self.current.value == 'init':
            return self.declaration()
        elif self.current.type == TokenType.IDENTIFIER:
            return self.assignment()
        else:
            raise SyntaxError(f"Unknown statement start: {self.current.value}")

    def declaration(self):
        self.eat(TokenType.KEYWORD)  # 'init'
        name = self.current.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.ASSIGN)
        value = self.expression()
        return Declaration(name, value)

    def assignment(self):
        name = self.current.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.ASSIGN)
        value = self.expression()
        return Assignment(name, value)

    def expression(self):
        left = self.term()
        while self.current.type == TokenType.OPERATOR:
            op = self.current.value
            self.eat(TokenType.OPERATOR)
            right = self.term()
            left = BinaryOp(left, op, right)
        return left

    def term(self):
        if self.current.type == TokenType.NUMBER:
            value = self.current.value
            self.eat(TokenType.NUMBER)
            return value
        elif self.current.type == TokenType.IDENTIFIER:
            value = self.current.value
            self.eat(TokenType.IDENTIFIER)
            return value
        else:
            raise SyntaxError("Unexpected token in expression")
