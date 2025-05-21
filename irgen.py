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
                self._emit_string_output(expr.value)
            elif expr.value_type == "number":
                if '.' in expr.value:
                    self._emit_float_output(float(expr.value))
                else:
                    self._emit_int_output(int(expr.value))
        elif isinstance(expr, Identifier):
            self._emit_var_output(expr.name)

    def _emit_string_output(self, text):
        fmt = text + "\n\0"
        string_val = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                                 bytearray(fmt.encode("utf8")))
        global_str = ir.GlobalVariable(self.module, string_val.type, name=f"str_{len(self.module.global_values)}")
        global_str.linkage = 'internal'
        global_str.global_constant = True
        global_str.initializer = string_val
        str_ptr = self.builder.bitcast(global_str, ir.IntType(8).as_pointer())
        self.builder.call(self.printf, [str_ptr])

    def _emit_int_output(self, value):
        fmt = "%d\n\0"
        self._call_printf(fmt, [ir.Constant(ir.IntType(32), value)])

    def _emit_float_output(self, value):
        fmt = "%f\n\0"
        self._call_printf(fmt, [ir.Constant(ir.DoubleType(), value)])

    def _emit_var_output(self, name):
        var = self.builder.load(self.named_vars[name])
        if isinstance(var.type, ir.IntType):
            fmt = "%d\n\0"
        elif isinstance(var.type, ir.DoubleType):
            fmt = "%f\n\0"
        else:
            raise ValueError("Unsupported variable type for output")
        self._call_printf(fmt, [var])

    def _call_printf(self, fmt_str, args):
        fmt_val = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt_str)),
                              bytearray(fmt_str.encode("utf8")))
        global_fmt = ir.GlobalVariable(self.module, fmt_val.type, name=f"fmt_{len(self.module.global_values)}")
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = fmt_val
        fmt_ptr = self.builder.bitcast(global_fmt, ir.IntType(8).as_pointer())
        self.builder.call(self.printf, [fmt_ptr] + args)


    def _generate_func_call(self, call):
        callee = self.funcs.get(call.name)
        if callee:
            self.builder.call(callee, [])
