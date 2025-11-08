from llvmlite import ir



def compiling_to_IR(ASTs, block= ir.Block, Module = ir.Module) ->  ir.Module:
    for key in ASTs:
        if key.byteType == "FUNC":
            ll_term = ir.FunctionType(ir.IntType(32),[])
            func = ir.Function(Module, ll_term, key.name)
            entry_block = func.append_basic_block("entry")
            build = ir.IRBuilder(entry_block)
            compiling_to_IR(key.block,block,Module)
        if key.byteType == "BLOCK":
            pass