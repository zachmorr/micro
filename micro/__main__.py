import sys
from argparse import ArgumentParser

from .parser import MicroParser
from .lexer import MicroLexer
from .compiler import compile
from .prettyprinter import prettyprint

def main():
    argparser = ArgumentParser(prog='Micro')
    subargparser = argparser.add_subparsers(help='Select Command', dest='subargparser')

    lexer = subargparser.add_parser('lexer')
    lexer.add_argument("file", help='File to run lexer on', default='')

    parser = subargparser.add_parser('parser')
    parser.add_argument("file", help='File to run parser on', default='')

    compiler = subargparser.add_parser('compiler')
    compiler.add_argument("file", help='File to run compiler on', default='')

    args = argparser.parse_args()
    
    if len(sys.argv) < 2:
        argparser.print_help()
    elif args.subargparser == "lexer":
        with open(args.file) as file:
            text = file.read()
        
        lexer = MicroLexer()
        tokens = lexer.tokenize(text)
        for token in tokens:
            print(f'{token.type}("{token.value}")')
    
    elif args.subargparser == "parser":
        parser = MicroParser()
        ast = parser.parse(args.file)
        prettyprint(ast)

    elif args.subargparser == "compiler":
        compile(args.file)


if __name__ == "__main__":
    main()