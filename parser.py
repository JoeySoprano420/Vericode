from lexer import Lexer, TokenType
from ast_nodes import *

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current = self.lexer.next_token()

    def eat(self, expected_type):
        if self.current.type == expected_type:
            tok = self.current
            self.current = self.lexer.next_token()
            return tok
        else:
            raise SyntaxError(f"Expected {expected_type}, got {self.current.type} ({self.current.value})")

    def parse(self):
        statements = []
        while self.current.type != TokenType.EOF:
            statements.append(self.statement())
        return Program(statements)

    def statement(self):
        if self.current.type == TokenType.KEYWORD:
            if self.current.value == "init":
                return self.declaration()
            elif self.current.value == "make":
                return self.function_def()
            elif self.current.value == "structure":
                return self.structure_def()
            elif self.current.value == "check":
                return self.if_stmt()
            elif self.current.value == "while":
                return self.while_loop()
            elif self.current.value == "return":
                return self.return_stmt()
            elif self.current.value == "out":
                return self.output_stmt()
            elif self.current.value == "go":
                return self.go_stmt()
            elif self.current.value == "await":
                return self.await_stmt()
            elif self.current.value == "sync":
                return self.sync_stmt()
            elif self.current.value == "throws":
                return self.throws_stmt()
            elif self.current.value == "verify":
                return self.verify_stmt()
            elif self.current.value == "proof":
                return self.proof_stmt()
            elif self.current.type == TokenType.IDENTIFIER:
            return self.assignment_or_call()
            else:
            raise SyntaxError(f"Unknown statement start: {self.current.value}")
            elif self.current.value == "for":
            return self.for_loop()


    def declaration(self):
        self.eat(TokenType.KEYWORD)  # init
        name = self.eat(TokenType.IDENTIFIER).value
        type_ = None
        if self.current.value == ":":
            self.eat(TokenType.SYMBOL)
            type_ = self.eat(TokenType.IDENTIFIER).value
        self.eat(TokenType.ASSIGN)
        value = self.expression()
        return Declaration(name, value, type_)

    def assignment_or_call(self):
        name = self.eat(TokenType.IDENTIFIER).value
        if self.current.value == "=":
            self.eat(TokenType.ASSIGN)
            value = self.expression()
            return Assignment(name, value)
        elif self.current.value == "(":
            self.eat(TokenType.SYMBOL)
            args = self.arguments()
            self.eat(TokenType.SYMBOL)  # )
            return FunctionCall(name, args)
        else:
            raise SyntaxError("Expected = or ( after identifier")

    def function_def(self):
        self.eat(TokenType.KEYWORD)  # make
        name = self.eat(TokenType.IDENTIFIER).value
        self.eat(TokenType.SYMBOL)  # (
        params = []
        if self.current.type != TokenType.SYMBOL or self.current.value != ")":
            while True:
                param_name = self.eat(TokenType.IDENTIFIER).value
                params.append(param_name)
                if self.current.value == ",":
                    self.eat(TokenType.SYMBOL)
                else:
                    break
        self.eat(TokenType.SYMBOL)  # )
        body = self.block()
        return FunctionDef(name, params, body)

    def structure_def(self):
        self.eat(TokenType.KEYWORD)  # structure
        name = self.eat(TokenType.IDENTIFIER).value
        base = None
        if self.current.value == "inherits":
            self.eat(TokenType.KEYWORD)
            base = self.eat(TokenType.IDENTIFIER).value
        body = self.block()
        return StructureDef(name, base, body.statements)

    def if_stmt(self):
        self.eat(TokenType.KEYWORD)  # check
        cond = self.expression()
        then_block = self.block()
        else_block = None
        if self.current.value == "else":
            self.eat(TokenType.KEYWORD)
            else_block = self.block()
        return IfStatement(cond, then_block, else_block)

    def while_loop(self):
        self.eat(TokenType.KEYWORD)  # while
        cond = self.expression()
        body = self.block()
        return WhileLoop(cond, body)

    def return_stmt(self):
        self.eat(TokenType.KEYWORD)  # return
        value = None
        if self.current.type != TokenType.SYMBOL or self.current.value != "}":
            value = self.expression()
        return ReturnStatement(value)

    def output_stmt(self):
        self.eat(TokenType.KEYWORD)  # out
        self.eat(TokenType.SYMBOL)   # :
        expr = self.expression()
        return Output(expr)

    def go_stmt(self):
        self.eat(TokenType.KEYWORD)
        expr = self.expression()
        return Go(expr)

    def await_stmt(self):
        self.eat(TokenType.KEYWORD)
        expr = self.expression()
        return Await(expr)

    def sync_stmt(self):
        self.eat(TokenType.KEYWORD)
        body = self.block()
        return Sync(body)

    def throws_stmt(self):
        self.eat(TokenType.KEYWORD)
        try_block = self.block()
        except_block = None
        if self.current.value == "excepts":
            self.eat(TokenType.KEYWORD)
            except_block = self.block()
        return Throws(try_block, except_block)

    def verify_stmt(self):
        self.eat(TokenType.KEYWORD)
        condition = self.expression()
        return Verify(condition)

    def proof_stmt(self):
        self.eat(TokenType.KEYWORD)
        self.eat(TokenType.SYMBOL)  # :
        expr = self.expression()
        return Proof(expr)

    def block(self):
        self.eat(TokenType.SYMBOL)  # {
        statements = []
        while self.current.value != "}":
            statements.append(self.statement())
        self.eat(TokenType.SYMBOL)  # }
        return Block(statements)

    def arguments(self):
        args = []
        if self.current.value != ")":
            while True:
                args.append(self.expression())
                if self.current.value == ",":
                    self.eat(TokenType.SYMBOL)
                else:
                    break
        return args

    def expression(self):
        left = self.term()
        while self.current.type == TokenType.OPERATOR:
            op = self.eat(TokenType.OPERATOR).value
            right = self.term()
            left = BinaryOp(left, op, right)
        return left

    def term(self):
        if self.current.type == TokenType.NUMBER:
            value = self.eat(TokenType.NUMBER).value
            return Literal(value, "number")
        elif self.current.type == TokenType.STRING:
            value = self.eat(TokenType.STRING).value
            return Literal(value, "string")
        elif self.current.type == TokenType.BOOL:
            value = self.eat(TokenType.BOOL).value
            return Literal(value, "bool")
        elif self.current.type == TokenType.IDENTIFIER:
            return Identifier(self.eat(TokenType.IDENTIFIER).value)
        elif self.current.value == "(":
            self.eat(TokenType.SYMBOL)
            expr = self.expression()
            self.eat(TokenType.SYMBOL)
            return expr
        else:
            raise SyntaxError(f"Unexpected token in expression: {self.current.value}")

    def if_stmt(self):
        self.eat(TokenType.KEYWORD)  # check
        cond = self.expression()
        then_block = self.block()

        else_block = None
        if self.current.value == "else":
            self.eat(TokenType.KEYWORD)
            if self.current.value == "check":
                else_block = self.if_stmt()  # else-if as recursive if
            else:
                else_block = self.block()
        return IfStatement(cond, then_block, else_block)

    def for_loop(self):
        self.eat(TokenType.KEYWORD)  # for
        iterator = self.eat(TokenType.IDENTIFIER).value
        self.eat(TokenType.KEYWORD)  # in
        iterable = self.expression()
        body = self.block()
        return ForLoop(iterator, iterable, body)
