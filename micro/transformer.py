from lark import Transformer, Tree
from .ast import *


class MicroTransformer(Transformer):
    def start(self, node: Tree):
        return Module(node)

    def code(self, node: Tree):
        return Code(node[0], node[1])

    def code_declaration(self, node: Tree):
        return CodeDeclaration(node[1], node[2])

    def arg_declaration(self, node: Tree):
        return list(node)

    def code_definition(self, node: Tree):
        return CodeDefinition(node)
    
    def assignment_expression(self, node: Tree):
        return AssignmentExpression(node[0], node[1])

    def return_expression(self, node: Tree):
        if len(node) == 1:
            return Return(None)
        else:
            return Return(node[1])

    def var_declaration(self, node: Tree):
        return VarDeclaration(node[1])

    def declaration(self, node: Tree):
        return Declaration(node[0], node[1])
    
    def multiply(self, node: Tree):
        return BinaryOperation(node[0], '*', node[1])

    def divide(self, node: Tree):
        return BinaryOperation(node[0], '/', node[1])
        
    def subtract(self, node: Tree):
        return BinaryOperation(node[0], '-', node[1])

    def add(self, node: Tree):
        return BinaryOperation(node[0], '+', node[1])

    def identifier(self, node: Tree):
        return Identifier(node[0])

    def type(self, node: Tree):
        return Type(node[0])

    def NUMBER(self, node: Tree):
        return int(node[0])
