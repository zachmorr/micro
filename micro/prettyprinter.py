from pyclbr import Function

from lark import Tree
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
    for declaration in node.external_declarations:
        prettyprint(declaration, indent)

def visit_Code(node: Code, indent: int = 0):
    prettyprint(node.declaration, indent)
    prettyprint(node.definition, indent)

def visit_CodeDeclaration(node: CodeDeclaration, indent: int = 0):
    prettyprint(node.declaration, indent)
    for arg in node.args:
        indented_print(indent, "Argument")
        prettyprint(arg, indent+1)

def visit_CodeDefinition(node: CodeDefinition, indent: int = 0):
    for statement in node.body:
        prettyprint(statement, indent)

def visit_AssignmentExpression(node: AssignmentExpression, indent: int = 0):
    prettyprint(node.lvalue, indent)
    prettyprint(node.rvalue, indent)

def visit_Return(node: Return, indent: int = 0):
    prettyprint(node.expression, indent)

def visit_FunctionCall(node: FunctionCall, indent: int = 0):
    prettyprint(node.identifier, indent)
    for arg in node.args:
        indented_print(indent, "Argument")
        prettyprint(arg, indent+1)

def visit_VarDeclaration(node: VarDeclaration, indent: int = 0):
    prettyprint(node.declaration, indent)

def visit_Declaration(node: Declaration, indent: int = 0):
    prettyprint(node.identifier, indent)
    prettyprint(node.type, indent)

def visit_Identifier(node: Identifier, indent: int = 0):
    indented_print(indent, node)

def visit_Type(node: Type, indent: int = 0):
    indented_print(indent, node)

def visit_int(node: int, indent: int = 0):
    indented_print(indent, node)

def visit_str(node: str, indent: int = 0):
    indented_print(indent, node)

def visit_BinaryOperation(node: BinaryOperation, indent: int = 0):
    prettyprint(node.left, indent)
    prettyprint(node.op, indent)
    prettyprint(node.right, indent)





