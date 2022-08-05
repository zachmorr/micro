from pyclbr import Function
import sys
from typing import Iterable
from sly import Parser
from sly.yacc import YaccProduction
from sly.lex import Token

from .error import print_error
from .lexer import MicroLexer
from .ast import *


class MicroParser(Parser):
    tokens = MicroLexer.tokens
    debugfile = 'parser.out'
    start = 'Module'

    ### Top Level Rules
    @_("Module : globals")
    def expr(self, p: YaccProduction):
        return Module(p.globals)

    @_("globals : global")
    def expr(self, p: YaccProduction):
        return [p[0]]

    @_("globals : globals global")
    def expr(self, p: YaccProduction):
        return p[0] + [p[1]]
    
    ### global
    @_("global : statement")
    def expr(self, p: YaccProduction):
        return p.statement
    
    @_("global : Code")
    def expr(self, p: YaccProduction):
        return p.Code

    ### Code
    @_("Code : CodeDeclaration CodeDefinition")
    def expr(self, p: YaccProduction):
        return Code(p.CodeDeclaration, p.CodeDefinition)

    @_("CodeDeclaration : CODE Declaration '(' arg_declaration_list ')'")
    def expr(self, p: YaccProduction):
        return CodeDeclaration(p.Declaration, p.arg_declaration_list)
    
    @_("CodeDeclaration : CODE Declaration '(' ')'")
    def expr(self, p: YaccProduction):
        return CodeDeclaration(p.Declaration, [])

    @_("CodeDefinition : '{' statements '}'")
    def expr(self, p: YaccProduction):
        return CodeDefinition(p.statements)

    @_("CodeDefinition : '{' '}'")
    def expr(self, p: YaccProduction):
        return CodeDefinition([])

    ### function argument list definition
    @_("arg_declaration : Declaration")
    def expr(self, p: YaccProduction):
        return p.Declaration

    @_("arg_declaration : Declaration ','")
    def expr(self, p: YaccProduction):
        return p.Declaration

    @_("arg_declaration_list : arg_declaration_list arg_declaration")
    def expr(self, p: YaccProduction):
        return p[0] + [p[1]]

    @_("arg_declaration_list : arg_declaration")
    def expr(self, p: YaccProduction):
        return [p[0]]

    ### statement definiton (aka allowed code)
    @_("statements : statement")
    def expr(self, p: YaccProduction):
        return [p[0]]    

    @_("statements : statements statement")
    def expr(self, p: YaccProduction):
        return p[0] + [p[1]]
    
    @_("statement : Return")
    def expr(self, p: YaccProduction):
        return p.Return

    @_("statement : AssignmentExpression")
    def expr(self, p: YaccProduction):
        return p.AssignmentExpression

    @_("statement : VarDeclaration")
    def expr(self, p: YaccProduction):
        return p.VarDeclaration

    ### Assignment operation
    @_("AssignmentExpression : lvalue '=' rvalue")
    def expr(self, p: YaccProduction):
        return AssignmentExpression(p.lvalue, p.rvalue)

    @_("AssignmentExpression : lvalue '=' lvalue")
    def expr(self, p: YaccProduction):
        return AssignmentExpression(p.lvalue0, p.lvalue1)

    ### Return
    @_("Return : RETURN rvalue")
    def expr(self, p: YaccProduction):
        return Return(p.rvalue)

    @_("Return : RETURN lvalue")
    def expr(self, p: YaccProduction):
        return Return(p.lvalue)

    ### LValues
    @_("lvalue : VarDeclaration")
    def expr(self, p: YaccProduction):
        return p.VarDeclaration

    @_("lvalue : Identifier")
    def expr(self, p: YaccProduction):
        return p.Identifier
    
    ### RValues
    @_("rvalue : FunctionCall")
    def expr(self, p: YaccProduction):
        return p.FunctionCall

    @_("rvalue : Expression")
    def expr(self, p: YaccProduction):
        return p.Expression

    # @_("rvalue : ConstExpression")
    # def expr(self, p: YaccProduction):
    #     return p.ConstExpression

    ### Function call 
    @_("FunctionCall : Identifier '(' arg_list ')'")
    def expr(self, p: YaccProduction):
        return FunctionCall(p.Identifier, p.arg_list)

    @_("FunctionCall : Identifier '(' ')'")
    def expr(self, p: YaccProduction):
        return FunctionCall(p.Identifier, [])

    ### Allowed Function call arguments
    @_("arg_list : arg")
    def expr(self, p: YaccProduction):
        return [p[0]]

    @_("arg_list : arg_list arg")
    def expr(self, p: YaccProduction):
        return p[0] + [p[1]]
    
    @_("arg : Identifier")
    def expr(self, p: YaccProduction):
        return p.Identifier

    @_("arg : Identifier ','")
    def expr(self, p: YaccProduction):
        return p.Identifier

    ### Expressions
    @_("Expression : '(' Expression ')'")
    def expr(self, p: YaccProduction):
        return p.Expression

    @_("Expression : addative")
    def expr(self, p: YaccProduction):
        return p.BinaryOperation
        
    @_("Expression : ConstNum")
    def expr(self, p: YaccProduction):
        return p.ConstNum
        
    ### Constant Expressions
    @_("ConstNum : NUMBER")
    def expr(self, p: YaccProduction):
        return p.NUMBER

    # Binary Operations (+,-,/,*)
    @_("addative : multiplicative")
    def expr(self, p: YaccProduction):
        return p.multiplicative

    @_("multiplicative : addative '+' multiplicative")
    def expr(self, p: YaccProduction):
        return BinaryOperation(p.addative, '+', p.multiplicative)

    @_("multiplicative : addative '-' multiplicative")
    def expr(self, p: YaccProduction):
        return BinaryOperation(p.addative, '-', p.multiplicative)

    @_("multiplicative : ConstNum")
    def expr(self, p: YaccProduction):
        return p.ConstNum

    @_("multiplicative : multiplicative '*' ConstNum")
    def expr(self, p: YaccProduction):
        return BinaryOperation(p.multiplicative, '*', p.ConstNum)

    @_("multiplicative : multiplicative '/' ConstNum")
    def expr(self, p: YaccProduction):
        return BinaryOperation(p.multiplicative, '/', p.ConstNum)

    ### Variable declaration
    @_("VarDeclaration : VAR Declaration")
    def expr(self, p: YaccProduction):
        return VarDeclaration(p.Declaration)
    
    ### Low level definitions
    @_("Declaration : Identifier ':' Type ")
    def expr(self, p: YaccProduction):
        return Declaration(p.Identifier, p.Type)
    
    @_("Type : ID")
    def expr(self, p: YaccProduction):
        return Type(p.ID)

    @_("Identifier : ID")
    def expr(self, p: YaccProduction):
        return Identifier(p.ID)

    def error(self, p: YaccProduction):
        print("Parse error!")
        if p is None: p = "$end"
        print(f"Offending Token: {p}")

    def parse(self, path: str) -> ASTNode:
        with open(path) as file:
            self.source = file.read()

        lexer = MicroLexer()
        tokens = lexer.tokenize(self.source)

        return super().parse(tokens)

        
