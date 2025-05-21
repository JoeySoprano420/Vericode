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
