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

    @_("declaration : ID ':' ID")
    def expr(self, p: YaccProduction):
        return Declaration(p.ID0, p.ID1)

    # @_("arg_list : empty")
    # def expr(self, p: YaccProduction):
    #     return []

    @_("arg_list : declaration")
    def expr(self, p: YaccProduction):
        return [p.declaration]

    @_("arg_list : arg_list ',' declaration")
    def expr(self, p: YaccProduction):
        return p.arg_list + [p.declaration]

    @_("codedef : CODE ID '(' arg_list ')' ':' ID ")
    def exper(self, p: YaccProduction):
        return CodeDef(p.ID0, p.ID1, p.arg_list)

    @_("codedef : CODE ID '(' ')' ':' ID ")
    def exper(self, p: YaccProduction):
        return CodeDef(p.ID0, p.ID1, [])
    
    @_("var : VAR declaration")
    def expr(self, p: YaccProduction):
        return Var(p.declaration, None)

    @_("statement : var")
    def exper(self, p: YaccProduction):
        return p.var

    # @_("statements : empty")
    # def exper(self, p: YaccProduction):
    #     return []

    @_("statements : statement")
    def exper(self, p: YaccProduction):
        return [p.statement]

    @_("statements : statements statement")
    def exper(self, p: YaccProduction):
        return p.statements + [p.statement]

    @_("codebody : '{' statements '}'")
    def exper(self, p: YaccProduction):
        return p.statements

    @_("codebody : '{' '}'")
    def exper(self, p: YaccProduction):
        return []

    @_("code : codedef codebody")
    def exper(self, p: YaccProduction):
        return Code(p.codedef, p.codebody)

    @_("globalvar : GLOBAL declaration")
    def exper(self, p: YaccProduction):
        return GlobalVar(p.declaration, None)

    @_("glob : globalvar")
    def expr(self, p: YaccProduction):
        return p.globalvar

    @_("glob : code")
    def expr(self, p: YaccProduction):
        return p.code

    @_("globals : globals glob")
    def expr(self, p: YaccProduction):
        return p.globals + [p.glob]

    @_("globals : glob")
    def expr(self, p: YaccProduction):
        return [p.glob]

    @_("module : globals")
    def expr(self, p: YaccProduction):
        return Module(p.globals, self.current_module)

    @_("module : error")
    def expr(self, p: YaccProduction):
        print_error('bad module!', self.source, p.lineno)

    # @_("")
    # def empty(self, p: YaccProduction):
    #     pass

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

        
