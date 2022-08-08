from typing import Any, List
from dataclasses import dataclass

@dataclass
class Declaration:
    identifier: str
    type: str

@dataclass
class BinaryOperation:
    left: Any
    op: str
    right: Any

@dataclass
class Assignment:
    lvalue: Any
    rvalue: Any

class CodeDefinition(list): 
    pass

@dataclass
class Code:
    declaration: Declaration
    arguments: List[Declaration]
    body: Any

@dataclass
class Module:
    external_declarations: list


