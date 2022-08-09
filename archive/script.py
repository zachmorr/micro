from llvmlite import ir
import llvmlite.binding as llvm

# module = ir.Module("test")
# builder = ir.IRBuilder()

# string = b'Output: %d'
# string = bytearray(string)
# stringtype = ir.ArrayType(ir.IntType(8), len(string))
# consttype = ir.Constant(stringtype,string)
# fmt = ir.GlobalVariable(module, stringtype, 'fmt')
# fmt.global_constant = True
# fmt.initializer = consttype

# func_type = ir.FunctionType(ir.IntType(32), [ir.PointerType(ir.IntType(8))], var_arg=True)
# printf = ir.Function(module, func_type, "printf")

# func_type = ir.FunctionType(ir.VoidType(), [])
# main = ir.Function(module, func_type, "main")

# block = main.append_basic_block("entry")
# builder.position_at_start(block)
# index = ir.IntType(32)(0)
# ptr = builder.gep(fmt, [index, index])

# number = ir.IntType(32)(10)
# builder.call(printf, [ptr, number])
# builder.ret_void()

# llvmir = str(module)
llvmir = """
; ModuleID = ".\sample.micro"
target triple = "unknown-unknown-unknown"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

define void @"main"()
{
entry:
  %"local" = alloca i32
  store i32 2, i32* %"local"
  %".3" = getelementptr [4 x i8], [4 x i8]* @"const0", i32 0, i32 0
  %".5" = call i32 (i8*, ...) @"printf"(i8* %".3")
  ret void
}

@"const0" = constant [4 x i8] c"one\\00"
@"const1" = constant [3 x i8] c"two"
"""
print(llvmir)

llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

target = llvm.Target.from_default_triple()
target_machine = target.create_target_machine()
# And an execution engine with an empty backing module
backing_mod = llvm.parse_assembly("")
engine = llvm.create_mcjit_compiler(backing_mod, target_machine)

module = llvm.parse_assembly(llvmir)
module.verify()

engine.add_module(module)
engine.finalize_object()
engine.run_static_constructors()

main_ptr = engine.get_function_address("main")

print("Executing Main:")
from ctypes import CFUNCTYPE, c_int32, c_void_p
cfunc = CFUNCTYPE(c_void_p)(main_ptr)
result = cfunc()
# print(result)