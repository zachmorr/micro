import sys
from argparse import ArgumentParser

from .parser import parser
from .compile import compile
from .transformer import MicroTransformer
from .prettyprinter import prettyprint
from .jit import run

def main():
    argparser = ArgumentParser(prog='Micro')
    argparser.add_argument("file", help='File to run parser on', default='')
    argparser.add_argument("--lark", help="Display generated Lark Tree", action="store_true")
    argparser.add_argument("--rawlark", help="Display generated Lark Tree", action="store_true")
    argparser.add_argument("--ast", help="Display AST", action="store_true")
    argparser.add_argument("--ir", help="Display LLVM IR", action="store_true")
    args = argparser.parse_args()
    
    if len(sys.argv) < 2:
        argparser.print_help()
        sys.exit(0)

    with open(args.file) as file:
        text = file.read()
    lark_ast = parser.parse(text)

    if args.lark:
        print(lark_ast.pretty())
    elif args.rawlark:
        print(lark_ast)
    
    ast = MicroTransformer().transform(lark_ast)
    if args.ast:
        prettyprint(ast)

    ir = compile(args.file, ast)
    if args.ir:
        print(ir)

    run(ir)

if __name__ == "__main__":
    main()