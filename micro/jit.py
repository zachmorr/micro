import llvmlite.binding as llvm

def run(ir: str):
    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()

    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    # And an execution engine with an empty backing module
    backing_mod = llvm.parse_assembly("")
    engine = llvm.create_mcjit_compiler(backing_mod, target_machine)

    module = llvm.parse_assembly(ir)
    module.verify()

    engine.add_module(module)
    engine.finalize_object()
    engine.run_static_constructors()

    main_ptr = engine.get_function_address("main")

    print("Executing Main:")
    from ctypes import CFUNCTYPE, c_int32
    cfunc = CFUNCTYPE(c_int32, c_int32)(main_ptr)
    result = cfunc(3)
    print(result)