from .ast import *


def indented_print(indent: int, *args, **kwargs):
    print("  "*indent, end="")
    print(*args, **kwargs)

def prettyprint(node: ASTNode, indent: int = 0):
    type_str = type(node).__name__
    function_name = f"visit_{type_str}"
    if function_name in globals():
        globals()[function_name](node, indent)
    else:
        print(f"No {function_name} prettyprinter implemented")

def visit_Module(node: Module, indent: int = 0):
    indented_print(indent, f"Module: {node.name}")
    for glob in node.globals:
        prettyprint(glob, indent+1)

def visit_GlobalVar(node: GlobalVar, indent: int = 0):
    indented_print(indent, f"GlobalVar:")
    prettyprint(node.declaration, indent+1)
    if node.initializer:
        prettyprint(node.initializer, indent+1)
    else:
        indented_print(indent+1, f"initializer: None")

def visit_Var(node: Var, indent: int = 0):
    indented_print(indent, f"Var:")
    prettyprint(node.declaration, indent+1)
    if node.initializer:
        prettyprint(node.initializer, indent+1)
    else:
        indented_print(indent+1, f"initializer: None")

def visit_CodeDef(node: CodeDef, indent: int = 0):
    indented_print(indent, f"CodeDef:")
    indented_print(indent+1, f"Type: {node.type}")
    indented_print(indent+1, f"Name: {node.name}")
    if node.args:
        indented_print(indent+1, f"Arguments:")
        for arg in node.args:
            prettyprint(arg, indent+2)

def visit_Code(node: Code, indent: int = 0):
    indented_print(indent, f"Code:")
    prettyprint(node.declaration, indent+1)
    if node.body:
        indented_print(indent+1, f"Body:")
        for line in node.body:
            prettyprint(line, indent+2)

def visit_Declaration(node: Declaration, indent: int = 0):
    indented_print(indent, f"Declaration:")
    indented_print(indent+1, f"Type: {node.type}")
    indented_print(indent+1, f"Name: {node.name}")

def visit_ConstExpr(node: ConstExpr, indent: int = 0):
    indented_print(indent, f"Value: {node.value}")
