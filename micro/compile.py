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
    transformed_ast = MicroTransformer().transform(ast)
    # print(transformed_ast)
    compiler = IRGenerator(module_name)
    compiled_ir = compiler.codegen(transformed_ast)
    print(compiled_ir)


class IRGenerator:
    types = {
        "byte": ir.IntType(8),
        "int": ir.IntType(32),
    }

    symbol_table = {}

    def __init__(self, module: str):
        self.module = ir.Module(module)

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
        return_type = self.types[code.declaration.type]
        arg_types = []
        for arg in code.arguments:
            type = self.types[arg.type]
            arg_types.append(type)
        
        function_type = ir.FunctionType(return_type, arg_types)
        function = ir.Function(self.module, function_type, name=code.declaration.identifier)
        for index, arg in enumerate(code.arguments):
            name = arg.identifier
            function.args[index].name = name

        self.codegen(code.body, function)

    def visit_CodeDefinition(self, definition: CodeDefinition, func: ir.Function):
        block = func.append_basic_block(name="entry")
        builder = ir.IRBuilder(block)
        a, b = func.args
        result = builder.fadd(a, b, name="res")
        
        builder.ret(result)
