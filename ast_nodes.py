class ASTNode:
    def __init__(self, node_type):
        self.node_type = node_type

class Program(ASTNode):
    def __init__(self, statements):
        super().__init__('Program')
        self.statements = statements

# === Declarations & Assignments ===
class Declaration(ASTNode):
    def __init__(self, name, value=None, type_=None):
        super().__init__('Declaration')
        self.name = name
        self.value = value
        self.type = type_

class Assignment(ASTNode):
    def __init__(self, name, value):
        super().__init__('Assignment')
        self.name = name
        self.value = value

# === Literals & Identifiers ===
class Literal(ASTNode):
    def __init__(self, value, value_type):
        super().__init__('Literal')
        self.value = value
        self.value_type = value_type

class Identifier(ASTNode):
    def __init__(self, name):
        super().__init__('Identifier')
        self.name = name

# === Binary Operations ===
class BinaryOp(ASTNode):
    def __init__(self, left, op, right):
        super().__init__('BinaryOp')
        self.left = left
        self.op = op
        self.right = right

# === Functions ===
class FunctionDef(ASTNode):
    def __init__(self, name, params, body):
        super().__init__('FunctionDef')
        self.name = name
        self.params = params
        self.body = body

class FunctionCall(ASTNode):
    def __init__(self, name, args):
        super().__init__('FunctionCall')
        self.name = name
        self.args = args

# === Control Flow ===
class IfStatement(ASTNode):
    def __init__(self, condition, then_block, else_block=None):
        super().__init__('IfStatement')
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

class WhileLoop(ASTNode):
    def __init__(self, condition, body):
        super().__init__('WhileLoop')
        self.condition = condition
        self.body = body

class ForLoop(ASTNode):
    def __init__(self, iterator, iterable, body):
        super().__init__('ForLoop')
        self.iterator = iterator
        self.iterable = iterable
        self.body = body

class ReturnStatement(ASTNode):
    def __init__(self, value=None):
        super().__init__('ReturnStatement')
        self.value = value

class BreakStatement(ASTNode):
    def __init__(self):
        super().__init__('BreakStatement')

# === Concurrency ===
class Await(ASTNode):
    def __init__(self, expr):
        super().__init__('Await')
        self.expr = expr

class Go(ASTNode):
    def __init__(self, expr):
        super().__init__('Go')
        self.expr = expr

class Sync(ASTNode):
    def __init__(self, block):
        super().__init__('Sync')
        self.block = block

# === Structures ===
class StructureDef(ASTNode):
    def __init__(self, name, base=None, body=None):
        super().__init__('StructureDef')
        self.name = name
        self.base = base
        self.body = body or []

# === Logic/Assertions ===
class Verify(ASTNode):
    def __init__(self, condition):
        super().__init__('Verify')
        self.condition = condition

class Assert(ASTNode):
    def __init__(self, condition):
        super().__init__('Assert')
        self.condition = condition

class Proof(ASTNode):
    def __init__(self, expression):
        super().__init__('Proof')
        self.expression = expression

class Truth(ASTNode):
    def __init__(self, expression):
        super().__init__('Truth')
        self.expression = expression

# === Exception Handling ===
class Throws(ASTNode):
    def __init__(self, try_block, except_block=None):
        super().__init__('Throws')
        self.try_block = try_block
        self.except_block = except_block

# === Stream I/O ===
class Output(ASTNode):
    def __init__(self, expr):
        super().__init__('Output')
        self.expr = expr

class Input(ASTNode):
    def __init__(self, var):
        super().__init__('Input')
        self.var = var

# === Macros (A.M.S.) ===
class Macro(ASTNode):
    def __init__(self, name, body):
        super().__init__('Macro')
        self.name = name
        self.body = body

# === Misc ===
class Block(ASTNode):
    def __init__(self, statements):
        super().__init__('Block')
        self.statements = statements

class Comment(ASTNode):
    def __init__(self, content):
        super().__init__('Comment')
        self.content = content
class ASTNode:
    def __init__(self, node_type):
        self.node_type = node_type

class Program(ASTNode):
    def __init__(self, statements):
        super().__init__('Program')
        self.statements = statements

class Declaration(ASTNode):
    def __init__(self, name, value):
        super().__init__('Declaration')
        self.name = name
        self.value = value

class Assignment(ASTNode):
    def __init__(self, name, value):
        super().__init__('Assignment')
        self.name = name
        self.value = value

class BinaryOp(ASTNode):
    def __init__(self, left, op, right):
        super().__init__('BinaryOp')
        self.left = left
        self.op = op
        self.right = right

class IfStatement(ASTNode):
    def __init__(self, condition, then_block, else_block=None):
        super().__init__('IfStatement')
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block  # Can be Block or another IfStatement

class ForLoop(ASTNode):
    def __init__(self, iterator, iterable, body):
        super().__init__('ForLoop')
        self.iterator = iterator
        self.iterable = iterable
        self.body = body

class BreakStatement(ASTNode):
    def __init__(self):
        super().__init__('BreakStatement')

class ContinueStatement(ASTNode):
    def __init__(self):
        super().__init__('ContinueStatement')

class FunctionDef(ASTNode):
    def __init__(self, name, params, body, return_type="void"):
        super().__init__('FunctionDef')
        self.name = name
        self.params = params  # list of parameter names
        self.body = body
        self.return_type = return_type

class ReturnStatement(ASTNode):
    def __init__(self, value=None):
        super().__init__('ReturnStatement')
        self.value = value

class FunctionDef(ASTNode):
    def __init__(self, name, params, body, return_type="void"):
        super().__init__('FunctionDef')
        self.name = name
        self.params = params  # list of parameter names
        self.body = body
        self.return_type = return_type

class ReturnStatement(ASTNode):
    def __init__(self, value=None):
        super().__init__('ReturnStatement')
        self.value = value

class StructDef(ASTNode):
    def __init__(self, name, fields):
        super().__init__('StructDef')
        self.name = name
        self.fields = fields  # list of (field_name, type)
        def structure_def(self):
    ...
    methods = []
    fields = []
    while self.current.value != "}":
        if self.current.value == "make":
            self.eat(TokenType.KEYWORD)
            method_name = self.eat(TokenType.IDENTIFIER).value
            self.eat(TokenType.SYMBOL)  # (
            self.eat(TokenType.SYMBOL)  # )
            body = self.block()
            methods.append(MethodDef(name, method_name, body))
        else:
            field_name = self.eat(TokenType.IDENTIFIER).value
            self.eat(TokenType.SYMBOL)
            field_type = self.eat(TokenType.IDENTIFIER).value
            fields.append((field_name, field_type))
    self.eat(TokenType.SYMBOL)  # }

    self.pending_methods += methods
    return StructDef(name, fields)


class StructInit(ASTNode):
    def __init__(self, struct_name, values):
        super().__init__('StructInit')
        self.struct_name = struct_name
        self.values = values  # list of expressions

class StructAccess(ASTNode):
    def __init__(self, instance, field):
        super().__init__('StructAccess')
        self.instance = instance  # Identifier
        self.field = field        # str

class TupleInit(ASTNode):
    def __init__(self, values):
        super().__init__('TupleInit')
        self.values = values  # list of expressions

class TupleAccess(ASTNode):
    def __init__(self, tuple_name, index):
        super().__init__('TupleAccess')
        self.tuple_name = tuple_name
        self.index = index  # int

class ListInit(ASTNode):
    def __init__(self, elements):
        super().__init__('ListInit')
        self.elements = elements  # [expression, ...]

class ListAccess(ASTNode):
    def __init__(self, list_name, index_expr):
        super().__init__('ListAccess')
        self.list_name = list_name  # Identifier
        self.index_expr = index_expr  # Expression

class HeapAlloc(ASTNode):
    def __init__(self, typename, values):
        super().__init__('HeapAlloc')
        self.typename = typename
        self.values = values

class PointerAccess(ASTNode):
    def __init__(self, pointer, field):
        super().__init__('PointerAccess')
        self.pointer = pointer  # Identifier or expression
        self.field = field      # string

class MethodDef(ASTNode):
    def __init__(self, struct_name, method_name, body, receiver_type="value"):
        super().__init__('MethodDef')
        self.struct_name = struct_name
        self.method_name = method_name
        self.body = body
        self.receiver_type = receiver_type  # "value" or "pointer"

