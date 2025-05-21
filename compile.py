from lexer import Lexer
from parser import Parser
from irgen import VericodeIRGenerator

def compile_vericode(file_path):
    with open(file_path, 'r') as f:
        code = f.read()

    lexer = Lexer(code)
    parser = Parser(lexer)
    ast = parser.parse()

    irgen = VericodeIRGenerator()
    irgen.generate(ast)

    with open("out.ll", "w") as f:
        f.write(str(irgen.module))

    print("LLVM IR written to out.ll")
