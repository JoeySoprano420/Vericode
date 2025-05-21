from lexer import Lexer
from parser import Parser
import sys

if __name__ == "__main__":
    with open("hello_world.vc", "r") as f:
        code = f.read()

    lexer = Lexer(code)
    parser = Parser(lexer)
    ast = parser.parse()

    import json

    def print_ast(node, indent=0):
        pad = "  " * indent
        print(f"{pad}{node.node_type}")
        for attr in vars(node):
            if attr == "node_type":
                continue
            val = getattr(node, attr)
            if isinstance(val, list):
                for item in val:
                    if isinstance(item, ASTNode):
                        print_ast(item, indent + 1)
                    else:
                        print(f"{pad}  {attr}: {item}")
            elif isinstance(val, ASTNode):
                print_ast(val, indent + 1)
            else:
                print(f"{pad}  {attr}: {val}")

    print_ast(ast)
