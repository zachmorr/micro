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
    current_module = None

    @_("type : ID")
    def expr(self, p: YaccProduction):
        return p.ID

    @_("identifier : ID")
    def expr(self, p: YaccProduction):
        return p.ID
    
    @_("Declaration : identifier ':' type ")
    def expr(self, p: YaccProduction):
        return Declaration(p.identifier, p.type)

    @_("VarDeclaration : VAR Declaration '=' initializer")
    def expr(self, p: YaccProduction):
        return VarDeclaration(p.Declaration, None)

    @_("VarDeclaration : VAR Declaration")
    def expr(self, p: YaccProduction):
        return VarDeclaration(p.Declaration, None)

    @_("statement : VarDeclaration")
    def expr(self, p: YaccProduction):
        return p.VarDeclaration

    @_("statements : statements statement")
    def expr(self, p: YaccProduction):
        return p[0] + [p[1]]

    @_("statements : statement")
    def expr(self, p: YaccProduction):
        return [p[0]]

    @_("CodeDefinition : '{' statements '}'")
    def expr(self, p: YaccProduction):
        return CodeDefinition(p.statements)

    @_("CodeDefinition : '{' '}'")
    def expr(self, p: YaccProduction):
        return CodeDefinition([])

    @_("arg : Declaration")
    def expr(self, p: YaccProduction):
        return p.Declaration

    @_("arg : Declaration ','")
    def expr(self, p: YaccProduction):
        return p.Declaration

    @_("arg_list : arg_list arg")
    def expr(self, p: YaccProduction):
        return p[0] + [p[1]]

    @_("arg_list : arg")
    def expr(self, p: YaccProduction):
        return [p[0]]

    @_("CodeDeclaration : CODE Declaration '(' arg_list ')'")
    def expr(self, p: YaccProduction):
        return CodeDeclaration(p.Declaration, p.arg_list)
    
    @_("CodeDeclaration : CODE Declaration '(' ')'")
    def expr(self, p: YaccProduction):
        return CodeDeclaration(p.Declaration, [])
    
    @_("Code : CodeDeclaration CodeDefinition")
    def expr(self, p: YaccProduction):
        return Code(p.CodeDeclaration, p.CodeDefinition)

    @_("GlobalVar : VarDeclaration")
    def expr(self, p: YaccProduction):
        return GlobalVar(p.VarDeclaration)

    @_("global : Code")
    def expr(self, p: YaccProduction):
        return p.Code

    @_("global : GlobalVar")
    def expr(self, p: YaccProduction):
        return p.GlobalVar

    @_("globals : globals global")
    def expr(self, p: YaccProduction):
        return p[0] + [p[1]]

    @_("globals : global")
    def expr(self, p: YaccProduction):
        return [p[0]]

    @_("module : globals")
    def expr(self, p: YaccProduction):
        return Module(p.globals, self.current_module)

    def error(self, p: YaccProduction):
        print("Parse error!")
        if p is None: p = "$end"
        print(f"Offending Token: {p}")

    def parse(self, path: str) -> ASTNode:
        self.current_module = path
        with open(path) as file:
            self.source = file.read()

        lexer = MicroLexer()
        tokens = lexer.tokenize(self.source)

        return super().parse(tokens)

        
