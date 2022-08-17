from multiprocessing.sharedctypes import RawValue
from typing import Any, List
from dataclasses import dataclass

class ASTNode: pass

class Type(ASTNode, str): pass

@dataclass
class ArrayType(ASTNode):
    data_type: Type

class StatementList(ASTNode, list): pass

@dataclass
class ArgumentDeclaration(ASTNode):
    name: str
    type: Any

@dataclass
class FunctionDeclaration(ASTNode):
    name: str
    return_type: Any
    args: List[ArgumentDeclaration]

@dataclass
class Function(ASTNode):
    declaration: FunctionDeclaration
    definition: StatementList

@dataclass
class Module(ASTNode):
    external_declarations: list

