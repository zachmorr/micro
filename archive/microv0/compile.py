from lib2to3.pygram import Symbols
import logging
from typing import List
from llvmlite import ir
from .transformer import MicroTransformer
from .ast import *

format = logging.Formatter('%(name)s:%(levelname)s:%(message)s')
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(format)
logger = logging.getLogger("IRGenerator")
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def compile(module_name: str, ast: tuple):
    compiler = IRGenerator(module_name)
    compiled_ir = compiler.codegen(ast)
    return str(compiled_ir)


class IRGenerator:
    # Default types
    types = {
        "byte": ir.IntType(8),
        "int": ir.IntType(32),
        "void": ir.VoidType(),
    }

    # Defined symbols
    symbol_table = {}

    context: ir.Context
    module: ir.Module
    builder: ir.IRBuilder
    constcounter: int = 0

    def __init__(self, module: str):
        self.module = ir.Module(module)
        self.builder = ir.IRBuilder()

        # import printf
        func_type = ir.FunctionType(ir.IntType(32), [ir.PointerType(ir.IntType(8))], var_arg=True)
        printf = ir.Function(self.module, func_type, "printf")
        self.symbol_table["printf"] = printf

    def codegen(self, node, *args):
        type_str = type(node).__name__
        function_name = f"visit_{type_str}"
        if function_name in dir(self):
            function = getattr(self, function_name)
            logger.debug(f"Calling {function_name}")
            return function(node, *args)
        else:
            logger.warn(f"No {function_name} code generator implemented")

    def visit_Module(self, module: Module):
        for extern in module.external_declarations:
            self.codegen(extern)

        return self.module

    def visit_Code(self, code: Code):
        # Create function
        function = self.codegen(code.declaration)
        entry_block = function.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(entry_block)

        # Add arguments to stack
        for arg in function.args:
            name = arg.name
            ptr = self.builder.alloca(arg.type, name=name)
            self.builder.store(arg, ptr)
            self.symbol_table[name] = ptr

        # Save current symbol table
        old_symbols = self.symbol_table.copy()

        self.codegen(code.definition)

        # Revert to old symbol table
        self.symbol_table = old_symbols

    def visit_CodeDeclaration(self, code_declaration: CodeDeclaration):
        identifier = code_declaration.declaration.identifier
        return_type = code_declaration.declaration.type
        return_type = self.types[return_type]

        arg_types = []
        for arg in code_declaration.args:
            type = self.types[arg.type]
            arg_types.append(type)

        function_type = ir.FunctionType(return_type, arg_types)
        function = ir.Function(self.module, function_type, name=identifier)

        # give names to arguments
        for index, arg in enumerate(code_declaration.args):
            name = arg.identifier
            function.args[index].name = name

        self.symbol_table[identifier] = function
        return function

    def visit_CodeDefinition(self, definition: CodeDefinition):
        for statement in definition.body:
            self.codegen(statement)

    def visit_FunctionCall(self, function_call: FunctionCall):
        args = []
        for arg in function_call.args:
            args.append(self.codegen(arg))

        name = function_call.identifier
        function = self.symbol_table[name]
        self.builder.call(function, args)

    def visit_Constant(self, constant: Constant):
        value = constant.value
        if isinstance(value, bytes):
            string = bytearray(value)
            stringtype = ir.ArrayType(ir.IntType(8), len(string))
            const = ir.Constant(stringtype,string)

            var = ir.GlobalVariable(self.module, stringtype, f"const{self.constcounter}")
            var.global_constant = True
            var.initializer = const
            self.constcounter += 1

            index = ir.IntType(32)(0)
            ptr = self.builder.gep(var, [index, index])
            return ptr
        elif isinstance(value, int):
            return ir.IntType(32)(value)

    def visit_AssignmentExpression(self, assignment: AssignmentExpression):
        rvalue = self.codegen(assignment.rvalue)
        lvalue = self.codegen(assignment.lvalue)

        self.builder.store(rvalue, lvalue)

    def visit_Return(self, ret: Return):
        if ret.expression is None:
            self.builder.ret_void()
        else:
            rvalue = self.codegen(ret.expression)
            self.builder.ret(rvalue)

    def visit_Identifier(self, identifier: Identifier):
        ptr = self.symbol_table[identifier]
        return self.builder.load(ptr, name=identifier)

    def visit_VarDeclaration(self, declaration: VarDeclaration):
        name = declaration.declaration.identifier
        type = declaration.declaration.type

        if isinstance(type, ArrayType):
            arr_type = self.types[type.type]
            arr_size = type.size
            type = ir.ArrayType(arr_type, arr_size)
        else:
            type = self.types[type]
        
        var = self.builder.alloca(type, name=name)
        self.symbol_table[name] = var
        return var