import llvmlite.binding as llvm
from ctypes import CFUNCTYPE, c_void_p

def run(ir: str):
    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()

    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    backing_mod = llvm.parse_assembly("")
    engine = llvm.create_mcjit_compiler(backing_mod, target_machine)

    module = llvm.parse_assembly(ir)
    module.verify()

    engine.add_module(module)
    engine.finalize_object()
    engine.run_static_constructors()

    main_ptr = engine.get_function_address("main")
    main = CFUNCTYPE(c_void_p)(main_ptr)

    print(f"Executing main() (0x{main_ptr:x}):")
    main()