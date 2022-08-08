from pathlib import Path
from lark.lark import Lark

grammar_file = Path(__file__).parent / "grammar.lark"
with open(grammar_file) as file:
    grammar = file.read()

parser = Lark(grammar)

