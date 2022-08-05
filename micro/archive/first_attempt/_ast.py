from typing import List
from dataclasses import dataclass

class ASTNode: pass

@dataclass
class Declaration(ASTNode):
    name: str
    type: str

@dataclass
class ConstExpr(ASTNode):
    value: int

@dataclass
class CodeDef(ASTNode):
    name: str
    type: str
    args: List[Declaration]

@dataclass
class CodeBody(ASTNode):
    statements : list

@dataclass
class Code(ASTNode):
    declaration: Declaration
    body: list

@dataclass
class Var(ASTNode):
    declaration: Declaration
    initializer: ConstExpr

@dataclass
class GlobalVar(ASTNode):
    declaration: Declaration
    initializer: ConstExpr

@dataclass
class Module(ASTNode):
    globals: List[ASTNode]
    name: str

