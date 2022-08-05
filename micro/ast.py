from typing import Any, List
from dataclasses import dataclass

class ASTNode: pass


@dataclass
class Declaration(ASTNode):
    identifier: str
    type: str

@dataclass
class VarDeclaration(ASTNode):
    declaration: Declaration
    initializer: Any

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
class GlobalVar(ASTNode):
    declaration: VarDeclaration

@dataclass
class Module(ASTNode):
    declarations: List[ASTNode]
    name: str

