from .ast import *


args = [
    ArgumentDeclaration("arr", ArrayType(Type("u8"))),
    ArgumentDeclaration("index", Type("u8")),
]
return_type = ArrayType(Type("u8"))
test = FunctionDeclaration("test", Type("u8"), args)

main_declaration = FunctionDeclaration("main", Type("void"), [])
main_definition = StatementList([])
main = Function(main_declaration, main_definition)
ast = Module([test,main])