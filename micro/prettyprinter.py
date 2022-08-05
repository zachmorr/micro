from .ast import *


def indented_print(indent: int, *args, **kwargs):
    print("  "*indent, end="")
    print(*args, **kwargs)

def prettyprint(node: ASTNode, indent: int = 0):
    if node is None:
        return
    
    type_str = type(node).__name__
    function_name = f"visit_{type_str}"
    if function_name in globals():
        indented_print(indent, type_str)
        globals()[function_name](node, indent+1)
    else:
        print(f"No {function_name} prettyprinter implemented")

def visit_Module(node: Module, indent: int = 0):
    indented_print(indent, f"Name: {node.name}")
    for declaration in node.declarations:
        prettyprint(declaration, indent)

def visit_GlobalVar(node: GlobalVar, indent: int = 0):
    prettyprint(node.declaration, indent)

def visit_Code(node: Code, indent: int = 0):
    prettyprint(node.declaration, indent)
    prettyprint(node.definition, indent)

def visit_CodeDeclaration(node: CodeDeclaration, indent: int = 0):
    prettyprint(node.declaration, indent)
    indented_print(indent, "Arguments")
    for arg in node.args:
        prettyprint(arg, indent+1)

def visit_CodeDefinition(node: CodeDefinition, indent: int = 0):
    for statement in node.body:
        prettyprint(statement, indent+1)

def visit_VarDeclaration(node: VarDeclaration, indent: int = 0):
    prettyprint(node.declaration, indent)

def visit_Declaration(node: Declaration, indent: int = 0):
    indented_print(indent, f"Identifier: {node.identifier}")
    indented_print(indent, f"Type: {node.type}")

