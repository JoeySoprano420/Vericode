from llvmlite import ir
from ast_nodes import *

class VericodeIRGenerator:
    def __init__(self):
        self.module = ir.Module(name="vericode_module")
        self.builder = None
        self.funcs = {}
        self.printf = None
        self._declare_printf()

    def _declare_printf(self):
        voidptr_ty = ir.IntType(8).as_pointer()
        printf_ty = ir.FunctionType(ir.IntType(32), [voidptr_ty], var_arg=True)
        self.printf = ir.Function(self.module, printf_ty, name="printf")

    def generate(self, node):
        if isinstance(node, Program):
            for stmt in node.statements:
                self.generate(stmt)
        elif isinstance(node, FunctionDef):
            self._generate_function(node)

    def _generate_function(self, node):
        func_ty = ir.FunctionType(ir.VoidType(), [])
        func = ir.Function(self.module, func_ty, name=node.name)
        block = func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)
        self.funcs[node.name] = func

        for stmt in node.body.statements:
            self.generate_statement(stmt)

        self.builder.ret_void()

    def generate_statement(self, stmt):
        if isinstance(stmt, Output):
            self._generate_output(stmt.expr)
        elif isinstance(stmt, ReturnStatement):
            self.builder.ret_void()
        elif isinstance(stmt, FunctionCall):
            self._generate_func_call(stmt)

    def _generate_output(self, expr):
    if isinstance(expr, Literal):
        if expr.value_type == "string":
            self._print_string(expr.value)
        elif

    def _generate_func_call(self, call):
        callee = self.funcs.get(call.name)
        if callee:
            self.builder.call(callee, [])
