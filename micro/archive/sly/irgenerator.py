import logging
from .ast import *
from llvmlite import ir


format = logging.Formatter('%(name)s:%(levelname)s:%(message)s')
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(format)
logger = logging.getLogger("IRGenerator")
logger.setLevel(logging.INFO)
logger.addHandler(handler)


class IRGenerator:
    types = {
        "byte": ir.IntType(8)
    }

    symbol_table = {}

    def codegen(self, node: ASTNode, module: ir.Module):
        type_str = type(node).__name__
        function_name = f"visit_{type_str}"
        if function_name in dir(self):
            function = getattr(self, function_name)
            logger.debug(f"Calling {function_name}")
            function(node, module)
        else:
            logger.warn(f"No {function_name} code generator implemented")

    def visit_Module(self, node: Module, module: ir.Module):
        for glob in node.globals:
            self.codegen(glob, module)

        return module

    
