from llvmlite import ir

from .irgenerator import IRGenerator
from .parser import MicroParser
from .lexer import MicroLexer



def compile(file: str):
    parser = MicroParser()
    ast = parser.parse_file(file)

    module = ir.Module(file)
    generator = IRGenerator()
    generator.codegen(ast, module)

    print("Compiled IR:")
    print(module)

