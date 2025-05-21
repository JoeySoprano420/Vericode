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
        self.named_vars = {}

        for stmt in node.body.statements:
            self.generate_statement(stmt)

        self.builder.ret_void()

    def generate_statement(self, stmt):
        if isinstance(stmt, Declaration):
            val = self._eval_literal(stmt.value)
            if isinstance(val.type, ir.IntType):
                var = self.builder.alloca(ir.IntType(32), name=stmt.name)
            elif isinstance(val.type, ir.DoubleType):
                var = self.builder.alloca(ir.DoubleType(), name=stmt.name)
            else:
                raise ValueError("Unsupported declaration type")
            self.builder.store(val, var)
            self.named_vars[stmt.name] = var
        elif isinstance(stmt, Output):
            self._generate_output(stmt.expr)
        elif isinstance(stmt, ReturnStatement):
            self.builder.ret_void()
        elif isinstance(stmt, FunctionCall):
            self._generate_func_call(stmt)
                def generate_statement(self, stmt):
        if isinstance(stmt, Declaration):
            val = self._eval_literal(stmt.value)
            var_type = val.type
            var = self.builder.alloca(var_type, name=stmt.name)
            self.builder.store(val, var)
            self.named_vars[stmt.name] = var

        elif isinstance(stmt, Assignment):
            value = self._eval_expression(stmt.value)
            var = self.named_vars[stmt.name]
            self.builder.store(value, var)

        elif isinstance(stmt, Output):
            self._generate_output(stmt.expr)

        elif isinstance(stmt, IfStatement):
            self._generate_if(stmt)

        elif isinstance(stmt, WhileLoop):
            self._generate_while(stmt)

        elif isinstance(stmt, ReturnStatement):
            self.builder.ret_void()

        elif isinstance(stmt, FunctionCall):
            self._generate_func_call(stmt)

        def _eval_expression(self, expr):
        if isinstance(expr, Literal):
            return self._eval_literal(expr)
        elif isinstance(expr, Identifier):
            return self.builder.load(self.named_vars[expr.name])
        elif isinstance(expr, BinaryOp):
            left = self._eval_expression(expr.left)
            right = self._eval_expression(expr.right)
            if expr.op == "+":
                return self.builder.add(left, right)
            elif expr.op == "-":
                return self.builder.sub(left, right)
            elif expr.op == "*":
                return self.builder.mul(left, right)
            elif expr.op == "/":
                return self.builder.sdiv(left, right)
            elif expr.op == "==":
                return self.builder.icmp_signed("==", left, right)
            elif expr.op == "!=":
                return self.builder.icmp_signed("!=", left, right)
            elif expr.op == ">":
                return self.builder.icmp_signed(">", left, right)
            elif expr.op == "<":
                return self.builder.icmp_signed("<", left, right)
            elif expr.op == ">=":
                return self.builder.icmp_signed(">=", left, right)
            elif expr.op == "<=":
                return self.builder.icmp_signed("<=", left, right)
            else:
                raise ValueError(f"Unsupported binary op: {expr.op}")

        def _generate_if(self, stmt):
        cond_val = self._eval_expression(stmt.condition)
        cond_bool = self.builder.icmp_signed("!=", cond_val, ir.Constant(cond_val.type, 0))

        then_bb = self.builder.append_basic_block("if_then")
        else_bb = self.builder.append_basic_block("if_else") if stmt.else_block else None
        end_bb = self.builder.append_basic_block("if_end")

        self.builder.cbranch(cond_bool, then_bb, else_bb or end_bb)

        # Then block
        self.builder.position_at_start(then_bb)
        for s in stmt.then_block.statements:
            self.generate_statement(s)
        self.builder.branch(end_bb)

        # Else block
        if stmt.else_block:
            self.builder.position_at_start(else_bb)
            for s in stmt.else_block.statements:
                self.generate_statement(s)
            self.builder.branch(end_bb)

        self.builder.position_at_start(end_bb)

        def _generate_while(self, stmt):
        cond_bb = self.builder.append_basic_block("while_cond")
        body_bb = self.builder.append_basic_block("while_body")
        end_bb = self.builder.append_basic_block("while_end")

        self.builder.branch(cond_bb)

        self.builder.position_at_start(cond_bb)
        cond_val = self._eval_expression(stmt.condition)
        cond_bool = self.builder.icmp_signed("!=", cond_val, ir.Constant(cond_val.type, 0))
        self.builder.cbranch(cond_bool, body_bb, end_bb)

        self.builder.position_at_start(body_bb)
        for s in stmt.body.statements:
            self.generate_statement(s)
        self.builder.branch(cond_bb)

        self.builder.position_at_start(end_bb)
    
    def _eval_literal(self, literal):
        if literal.value_type == "number":
            if '.' in literal.value:
                return ir.Constant(ir.DoubleType(), float(literal.value))
            else:
                return ir.Constant(ir.IntType(32), int(literal.value))
        elif literal.value_type == "string":
            raise NotImplementedError("Can't evaluate raw string to value yet")


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

    def generate_statement(self, stmt):
        # ... existing cases ...
        elif isinstance(stmt, ForLoop):
            self._generate_for(stmt)

    def _generate_for(self, stmt):
        loop_var_name = stmt.iterator
        iterable = self._eval_expression(stmt.iterable)

        start_val = ir.Constant(ir.IntType(32), 0)
        end_val = iterable

        ptr = self.builder.alloca(ir.IntType(32), name=loop_var_name)
        self.builder.store(start_val, ptr)
        self.named_vars[loop_var_name] = ptr

        cond_bb = self.builder.append_basic_block("for_cond")
        body_bb = self.builder.append_basic_block("for_body")
        end_bb = self.builder.append_basic_block("for_end")

        self.builder.branch(cond_bb)

        # Condition check
        self.builder.position_at_start(cond_bb)
        index_val = self.builder.load(ptr)
        cmp = self.builder.icmp_signed("<", index_val, end_val)
        self.builder.cbranch(cmp, body_bb, end_bb)

        # Body
        self.builder.position_at_start(body_bb)
        for s in stmt.body.statements:
            self.generate_statement(s)

        # Increment
        next_val = self.builder.add(index_val, ir.Constant(ir.IntType(32), 1))
        self.builder.store(next_val, ptr)
        self.builder.branch(cond_bb)

        self.builder.position_at_start(end_bb)

class VericodeIRGenerator:
    def __init__(self):
        self.module = ir.Module(name="vericode_module")
        self.builder = None
        self.funcs = {}
        self.printf = None
        self.named_vars = {}
        self.loop_context = []  # stack of (continue_block, break_block)
        self._declare_printf()

    def generate_statement(self, stmt):
        # ... existing cases ...
        elif isinstance(stmt, BreakStatement):
            if not self.loop_context:
                raise SyntaxError("break used outside loop")
            _, break_bb = self.loop_context[-1]
            self.builder.branch(break_bb)

        elif isinstance(stmt, ContinueStatement):
            if not self.loop_context:
                raise SyntaxError("continue used outside loop")
            continue_bb, _ = self.loop_context[-1]
            self.builder.branch(continue_bb)
    def _generate_while(self, stmt):
        cond_bb = self.builder.append_basic_block("while_cond")
        body_bb = self.builder.append_basic_block("while_body")
        end_bb = self.builder.append_basic_block("while_end")

        self.loop_context.append((cond_bb, end_bb))
        self.builder.branch(cond_bb)

        self.builder.position_at_start(cond_bb)
        cond_val = self._eval_expression(stmt.condition)
        cond_bool = self.builder.icmp_signed("!=", cond_val, ir.Constant(cond_val.type, 0))
        self.builder.cbranch(cond_bool, body_bb, end_bb)

        self.builder.position_at_start(body_bb)
        for s in stmt.body.statements:
            self.generate_statement(s)
        self.builder.branch(cond_bb)

        self.builder.position_at_start(end_bb)
        self.loop_context.pop()

    def _generate_for(self, stmt):
        loop_var_name = stmt.iterator
        iterable = self._eval_expression(stmt.iterable)

        start_val = ir.Constant(ir.IntType(32), 0)
        end_val = iterable

        ptr = self.builder.alloca(ir.IntType(32), name=loop_var_name)
        self.builder.store(start_val, ptr)
        self.named_vars[loop_var_name] = ptr

        cond_bb = self.builder.append_basic_block("for_cond")
        body_bb = self.builder.append_basic_block("for_body")
        end_bb = self.builder.append_basic_block("for_end")

        self.loop_context.append((cond_bb, end_bb))
        self.builder.branch(cond_bb)

        self.builder.position_at_start(cond_bb)
        index_val = self.builder.load(ptr)
        cmp = self.builder.icmp_signed("<", index_val, end_val)
        self.builder.cbranch(cmp, body_bb, end_bb)

        self.builder.position_at_start(body_bb)
        for s in stmt.body.statements:
            self.generate_statement(s)

        next_val = self.builder.add(index_val, ir.Constant(ir.IntType(32), 1))
        self.builder.store(next_val, ptr)
        self.builder.branch(cond_bb)

        self.builder.position_at_start(end_bb)
        self.loop_context.pop()

    def _generate_function(self, node: FunctionDef):
        param_types = [ir.IntType(32) for _ in node.params]  # all int32 for now
        return_ty = ir.IntType(32) if node.return_type != "void" else ir.VoidType()

        func_ty = ir.FunctionType(return_ty, param_types)
        func = ir.Function(self.module, func_ty, name=node.name)
        self.funcs[node.name] = func

        block = func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)
        self.named_vars = {}

        # Store arguments
        for i, name in enumerate(node.params):
            arg = func.args[i]
            var = self.builder.alloca(ir.IntType(32), name=name)
            self.builder.store(arg, var)
            self.named_vars[name] = var

        ret_val = None
        for stmt in node.body.statements:
            if isinstance(stmt, ReturnStatement):
                ret_val = self._eval_expression(stmt.value) if stmt.value else None
                break
            self.generate_statement(stmt)

        if node.return_type != "void":
            self.builder.ret(ret_val or ir.Constant(ir.IntType(32), 0))
        else:
            self.builder.ret_void()

    def _generate_func_call(self, call):
        callee = self.funcs.get(call.name)
        args = [self._eval_expression(arg) for arg in call.args]
        return self.builder.call(callee, args)

    def _eval_expression(self, expr):
        if isinstance(expr, Literal):
            return self._eval_literal(expr)
        elif isinstance(expr, Identifier):
            return self.builder.load(self.named_vars[expr.name])
        elif isinstance(expr, BinaryOp):
            # already handled
            ...
        elif isinstance(expr, FunctionCall):
            return self._generate_func_call(expr)

    def _generate_function(self, node: FunctionDef):
        param_types = [ir.IntType(32) for _ in node.params]  # all int32 for now
        return_ty = ir.IntType(32) if node.return_type != "void" else ir.VoidType()

        func_ty = ir.FunctionType(return_ty, param_types)
        func = ir.Function(self.module, func_ty, name=node.name)
        self.funcs[node.name] = func

        block = func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)
        self.named_vars = {}

        # Store arguments
        for i, name in enumerate(node.params):
            arg = func.args[i]
            var = self.builder.alloca(ir.IntType(32), name=name)
            self.builder.store(arg, var)
            self.named_vars[name] = var

        ret_val = None
        for stmt in node.body.statements:
            if isinstance(stmt, ReturnStatement):
                ret_val = self._eval_expression(stmt.value) if stmt.value else None
                break
            self.generate_statement(stmt)

    def _generate_func_call(self, call):
        callee = self.funcs.get(call.name)
        args = [self._eval_expression(arg) for arg in call.args]
        return self.builder.call(callee, args)


        if node.return_type != "void":
            self.builder.ret(ret_val or ir.Constant(ir.IntType(32), 0))
        else:
            self.builder.ret_void()

class VericodeIRGenerator:
    def __init__(self):
        ...
        self.struct_types = {}  # name: LLVMType

    def generate(self, node):
        if isinstance(node, StructDef):
            self._define_struct(node)
        elif isinstance(node, Program):
            for stmt in node.statements:
                self.generate(stmt)

    def _define_struct(self, node):
        field_types = []
        for _, t in node.fields:
            if t == "int":
                field_types.append(ir.IntType(32))
            elif t == "float":
                field_types.append(ir.DoubleType())
        struct_type = ir.LiteralStructType(field_types)
        self.struct_types[node.name] = struct_type

    def _eval_expression(self, expr):
        if isinstance(expr, StructInit):
            struct_type = self.struct_types[expr.struct_name]
            values = [self._eval_expression(v) for v in expr.values]
            struct_val = ir.Constant(struct_type, values)
            ptr = self.builder.alloca(struct_type)
            self.builder.store(struct_val, ptr)
            return ptr

        elif isinstance(expr, StructAccess):
            base_ptr = self.named_vars[expr.instance.name]
            struct_type = base_ptr.type.pointee
            idx = self._get_struct_field_index(expr.instance.name, expr.field)
            gep = self.builder.gep(base_ptr, [ir.Constant(ir.IntType(32), 0),
                                              ir.Constant(ir.IntType(32), idx)])
            return self.builder.load(gep)

    def _get_struct_field_index(self, struct_name, field_name):
        struct_def = next(s for s in self.struct_types if s == struct_name)
        struct_fields = list(self.struct_types[struct_def].elements)
        field_names = [f[0] for f in struct_fields]
        return field_names.index(field_name)

def _generate_function(self, node: FunctionDef):
    # Map Vericode types to LLVM types
    def map_type(vtype):
        if vtype == "int":
            return ir.IntType(32)
        elif vtype == "float":
            return ir.DoubleType()
        elif vtype == "void":
            return ir.VoidType()
        raise ValueError(f"Unknown type: {vtype}")

    llvm_param_types = [map_type(t) for _, t in node.params]
    return_ty = map_type(node.return_type)

    func_ty = ir.FunctionType(return_ty, llvm_param_types)
    func = ir.Function(self.module, func_ty, name=node.name)
    self.funcs[node.name] = func

    block = func.append_basic_block(name="entry")
    self.builder = ir.IRBuilder(block)
    self.named_vars = {}

    # Allocate and store params
    for i, (pname, ptype) in enumerate(node.params):
        arg = func.args[i]
        var = self.builder.alloca(map_type(ptype), name=pname)
        self.builder.store(arg, var)
        self.named_vars[pname] = var

    # Emit body
    retval = None
    for stmt in node.body.statements:
        if isinstance(stmt, ReturnStatement):
            retval = self._eval_expression(stmt.value)
            self.builder.ret(retval)
            return  # exit early
        self.generate_statement(stmt)

    if node.return_type == "void":
        self.builder.ret_void()

def _generate_func_call(self, call):
    callee = self.funcs.get(call.name)
    args = [self._eval_expression(arg) for arg in call.args]
    return self.builder.call(callee, args)

elif isinstance(expr, FunctionCall):
    return self._generate_func_call(expr)

    def generate_statement(self, stmt):
        if isinstance(stmt, Declaration):
            if isinstance(stmt.value, ListInit):
                array_vals = [self._eval_expression(v) for v in stmt.value.elements]
                el_type = array_vals[0].type
                array_type = ir.ArrayType(el_type, len(array_vals))
                const_array = ir.Constant(array_type, array_vals)
                var = self.builder.alloca(array_type, name=stmt.name)
                self.builder.store(const_array, var)
                self.named_vars[stmt.name] = var
            else:
                val = self._eval_expression(stmt.value)
                var = self.builder.alloca(val.type, name=stmt.name)
                self.builder.store(val, var)
                self.named_vars[stmt.name] = var

    def _eval_expression(self, expr):
        # ... existing
        elif isinstance(expr, ListAccess):
            arr_ptr = self.named_vars[expr.list_name.name]
            index = self._eval_expression(expr.index_expr)
            gep = self.builder.gep(arr_ptr, [ir.Constant(ir.IntType(32), 0), index])
            return self.builder.load(gep)
