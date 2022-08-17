from llvmlite import ir
import llvmlite.binding as llvm


llvmir = """
; ModuleID = ".\sample.micro"
target triple = "unknown-unknown-unknown"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

%arrtype = type {i8, [0 x i8]}

define void @"test"(%arrtype* %arg)
{
entry:
  ; Load Size
  %0 = getelementptr %arrtype, %arrtype* %arg, i32 0, i32 0 
  %1 = load i8, i8* %0

  ; Print Size
  %"2" = getelementptr [11 x i8], [11 x i8]* @"const0", i32 0, i32 0
  call i32 (i8*, ...) @"printf"(i8* %"2", i8 %1)

  ; Print arg[0]
  %3 = getelementptr %arrtype, %arrtype* %arg, i32 0, i32 1, i32 0
  %4 = load i8, i8* %3
  call i32 (i8*, ...) @"printf"(i8* %"2", i8 %4)

  ; Print arg[1]
  %6 = getelementptr %arrtype, %arrtype* %arg, i32 0, i32 1, i32 1
  %7 = load i8, i8* %6
  call i32 (i8*, ...) @"printf"(i8* %"2", i8 %7)

  ; Print arg[2]
  %9 = getelementptr %arrtype, %arrtype* %arg, i32 0, i32 1, i32 2
  %10 = load i8, i8* %9
  call i32 (i8*, ...) @"printf"(i8* %"2", i8 %10)
  call i32 (i8*, ...) @"printf"(i8* %"2", i8 %10)
  ret void
}

define void @"main"()
{
entry:
  %arr = alloca {i8, [3 x i8]}

  ; Store length
  %0 = bitcast {i8, [3 x i8]}* %arr to i8*
  store i8 3, i8* %0

  ; Store value in arr[0]
  %1 = getelementptr {i8, [3 x i8]}, {i8, [3 x i8]}* %arr, i32 0, i32 1, i32 0
  store i8 1, i8* %1

  ; Store value in arr[1]
  %2 = getelementptr {i8, [3 x i8]}, {i8, [3 x i8]}* %arr, i32 0, i32 1, i32 1
  store i8 2, i8* %2

  ; Store value in arr[2]
  %3 = getelementptr {i8, [3 x i8]}, {i8, [3 x i8]}* %arr, i32 0, i32 1, i32 2
  store i8 3, i8* %3

  ; Call test()
  %4 = bitcast {i8, [3 x i8]}* %arr to %arrtype*
  call void @"test"(%arrtype* %4)
  ret void
}

@"const0" = constant [11 x i8] c"Num: %hhx\n\\00"
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