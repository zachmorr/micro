from multiprocessing.sharedctypes import RawValue
from typing import Any, List
from dataclasses import dataclass

class ASTNode: pass

class Identifier(ASTNode, str): 
    pass

class Type(ASTNode, str): 
    pass

@dataclass
class Declaration(ASTNode):
    identifier: Identifier
    type: Type

@dataclass
class BinaryOperation(ASTNode):
    left: Any
    op: str
    right: Any

@dataclass
class VarDeclaration(ASTNode):
    declaration: Declaration

@dataclass
class Return(ASTNode):
    expression: Any

@dataclass
class FunctionCall(ASTNode):
    identifier: Identifier
    args: list

@dataclass
class AssignmentExpression(ASTNode):
    lvalue: Any
    rvalue: Any

@dataclass
class CodeDeclaration(ASTNode):
    declaration: Declaration
    args: List[Declaration]

@dataclass
class CodeDefinition(ASTNode):
    body: List

@dataclass
class Code(ASTNode):
    declaration: CodeDeclaration
    definition: CodeDefinition

@dataclass
class Module(ASTNode):
    external_declarations: List[ASTNode]

