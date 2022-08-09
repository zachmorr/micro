from typing import Iterable
from sly import Lexer
from sly.lex import Token
from .error import print_error

class LexingError(Exception): pass

class MicroLexer(Lexer):
    tokens = {
        ID, VAR, CODE, NUMBER, RETURN
    }

    ignore = " \t"
    ignore_comment = r'\#.*'
    literals = [
        '+', '-', '/', '*', '=',
        '{', '}', '[', ']', '(', ')',
        '_', ':', ',', '',
    ]

    ID = r"[a-zA-Z_][a-zA-Z_0-9]*"
    ID['code']  = CODE
    ID['var']   = VAR
    ID['return']   = RETURN

    @_(r"\d+")
    def NUMBER(self, token: Token):
        token.value = int(token.value, 0)
        return token

    @_(r'\n+')
    def ignore_newline(self, token: Token):
        self.lineno += len(token.value)

    def error(self, token: Token):
        line = token.lineno
        print_error(f"Unknown character on line {token.lineno}", self.source, line)

    def tokenize(self, text, lineno=1, index=0) -> Iterable[Token]:
        self.source = text
        return super().tokenize(text, lineno, index)

