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
    @_("global : AssignmentExpression")
    def expr(self, p: YaccProduction):
        return p.AssignmentExpression
    
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

    @_("rvalue : Identifier")
    def expr(self, p: YaccProduction):
        return p.Identifier

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

    ### Return
    @_("Return : RETURN")
    def expr(self, p: YaccProduction):
        return Return(None)

    @_("Return : RETURN Expression")
    def expr(self, p: YaccProduction):
        return Return(p.Expression)

    # @_("Return : RETURN Identifier")
    # def expr(self, p: YaccProduction):
    #     return Return(p.lvalue)

    ### Unary Expression
    @_("UnaryExpression : NUMBER")
    def expr(self, p: YaccProduction):
        return p.NUMBER

    @_("UnaryExpression : Identifier")
    def expr(self, p: YaccProduction):
        return p.ID

    @_("UnaryExpression : '(' Expression ')'")
    def expr(self, p: YaccProduction):
        return p.Expression

    ### Expressions
    @_("Expression : BinaryOperation")
    def expr(self, p: YaccProduction):
        return p.BinaryOperation

    # Binary Operations (+,-,/,*)
    @_("BinaryOperation : addative")
    def expr(self, p: YaccProduction):
        return p.addative

    @_("addative : multiplicative")
    def expr(self, p: YaccProduction):
        return p.multiplicative

    @_("addative : addative '+' multiplicative")
    def expr(self, p: YaccProduction):
        return BinaryOperation(p.addative, '+', p.multiplicative)

    @_("addative : addative '-' multiplicative")
    def expr(self, p: YaccProduction):
        return BinaryOperation(p.addative, '-', p.multiplicative)

    @_("multiplicative : UnaryExpression")
    def expr(self, p: YaccProduction):
        return p.UnaryExpression

    @_("multiplicative : multiplicative '*' UnaryExpression")
    def expr(self, p: YaccProduction):
        return BinaryOperation(p.multiplicative, '*', p.UnaryExpression)

    @_("multiplicative : multiplicative '/' UnaryExpression")
    def expr(self, p: YaccProduction):
        return BinaryOperation(p.multiplicative, '/', p.UnaryExpression)

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

        
