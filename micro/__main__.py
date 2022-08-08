import sys
from argparse import ArgumentParser

from .parser import parser
from .compile import compile

def main():
    argparser = ArgumentParser(prog='Micro')
    subargparser = argparser.add_subparsers(help='Select Command', dest='subargparser')

    parse_argparser = subargparser.add_parser('parse')
    parse_argparser.add_argument("file", help='File to run parser on', default='')

    compile_argparser = subargparser.add_parser('compile')
    compile_argparser.add_argument("file", help='File to run compiler on', default='')

    args = argparser.parse_args()
    
    if len(sys.argv) < 2:
        argparser.print_help()
        sys.exit(0)

    with open(args.file) as file:
        text = file.read()
    ast = parser.parse(text)

    if args.subargparser == "parse":
        print(ast.pretty())
    elif args.subargparser == "compile":
        compile(args.file, ast)


if __name__ == "__main__":
    main()