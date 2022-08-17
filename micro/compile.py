from lib2to3.pygram import Symbols
import logging
from typing import List
from llvmlite import ir
from .ast import *

format = logging.Formatter('%(name)s:%(levelname)s:%(message)s')
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(format)
logger = logging.getLogger("IRGenerator")
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


def compile(module_name: str, ast: tuple):
    compiler = IRGenerator(module_name)
    compiled_ir = compiler.codegen(ast)
    return str(compiled_ir)


class CompileError(Exception): pass

class IRGenerator:
    word_size = 32

    # Default types
    defined_types = {
        "u8": ir.IntType(8),
        "u32": ir.IntType(32),
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
            retval = function(node, *args)
            return retval
        else:
            logger.warn(f"No {function_name} code generator implemented")

    def get_type(self, type_name: str) -> ir.Type:
        type = self.defined_types.get(type_name)
        if type is None:
            raise CompileError(f"Type {type_name} is not defined")

        return type


    def visit_Module(self, module: Module):
        for extern in module.external_declarations:
            self.codegen(extern)

        return self.module

    def visit_Function(self, function: Function):
        # Create function
        function_declaration: ir.Function = self.codegen(function.declaration)
        entry_block = function_declaration.append_basic_block(name="entry")
        self.builder.position_at_start(entry_block)

        # Add arguments function arguments to symbol table
        for arg in function_declaration.args:
            # name = arg.name
            # ptr = self.builder.alloca(arg.type, name=name)
            # self.builder.store(arg, ptr)
            self.symbol_table[arg.name] = arg

        ### Replace with context manager
        # Save current symbol table
        old_symbols = self.symbol_table.copy()

        self.codegen(function.definition)

        # Automatically add return if return type is void
        return_type = function_declaration.return_value
        if return_type.type == ir.VoidType():
            self.builder.ret_void()

        # Revert to old symbol table
        self.symbol_table = old_symbols

    def visit_FunctionDeclaration(self, declaration: FunctionDeclaration):
        name = declaration.name
        return_type = self.codegen(declaration.return_type)

        arg_types = []
        for arg in declaration.args:
            type = self.codegen(arg.type)
            arg_types.append(type)

        function_type = ir.FunctionType(return_type, arg_types)
        function = ir.Function(self.module, function_type, name=name)

        # give names to arguments
        for index, arg in enumerate(declaration.args):
            name = arg.name
            function.args[index].name = name
        
        return function
    
    def visit_ArrayType(self, array: ArrayType):
        type = self.codegen(array.data_type)
        size_type = ir.IntType(self.word_size)
        struct = ir.LiteralStructType([
            size_type,
            ir.ArrayType(type, 0),
        ])

        ptr = ir.PointerType(struct)
        # logger.info(f"Generating IR for ArrayType({array.data_type}): {ptr}")
        return ptr

    def visit_Type(self, type: Type):
        llvm_type = self.get_type(type)
        # logger.info(f"Generating IR for Type({type}): {llvm_type}")
        return llvm_type
