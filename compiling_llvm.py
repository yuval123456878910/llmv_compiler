from llvmlite import ir

verubles = dict()
total_veubles_complitions = 0 # count all the prosses like var2, a1
def compiling_to_IR(ASTs, block= ir.Block, Module = ir.Module, building = ir.IRBuilder):
    global verubles, total_veubles_complitions
    for key in ASTs:
        if key.byteType == "FUNC":
            type_ret = ""
            if key.type == "int":
                type_ret = ir.IntType(32)
            elif key.type == "float":
                type_ret = ir.DoubleType()
            ll_term = ir.FunctionType(type_ret,[])
            func = ir.Function(Module, ll_term, key.name)
            entry_block = func.append_basic_block("entry")
            builder = ir.IRBuilder(entry_block)
            compiling_to_IR([key.block],entry_block,Module,builder)
        
        elif key.byteType == "BLOCK":            
            compiling_to_IR(key.lines,block,Module,building)

        
        elif key.byteType == "OPR":
            if key.fourse == "ADDI":
                
                ver1 = compiling_to_IR([key.right],block,Module=Module,building=building)
                ver2 = compiling_to_IR([key.left],block,Module=Module,building=building)

                verubles[f"{total_veubles_complitions}Cal"] = building.add(lhs=ver2,rhs=ver1,name=f"{total_veubles_complitions}Cal")
                r = verubles[f"{total_veubles_complitions}Cal"]

                total_veubles_complitions += 1
                return r
            
            elif key.fourse == "SUPT":
                ver1 = compiling_to_IR([key.right],block,Module=Module,building=building)
                
                ver2 = compiling_to_IR([key.left],block,Module=Module,building=building)
                verubles[f"{total_veubles_complitions}Cal"] = building.sub(lhs=ver2,rhs=ver1,name=f"{total_veubles_complitions}Cal")

                r = verubles[f"{total_veubles_complitions}Cal"]

                total_veubles_complitions += 1
                return r
            
            elif key.fourse == "MULT":
                ver1 = compiling_to_IR([key.right],block,Module=Module,building=building)
                
                ver2 = compiling_to_IR([key.left],block,Module=Module,building=building)
                verubles[f"{total_veubles_complitions}Cal"] = building.mul(lhs=ver2,rhs=ver1,name=f"{total_veubles_complitions}Cal")

                r = verubles[f"{total_veubles_complitions}Cal"]

                total_veubles_complitions += 1
                return r
            
            elif key.fourse == "DIVI":
                ver1 = compiling_to_IR([key.right],block,Module=Module,building=building)
                
                ver2 = compiling_to_IR([key.left],block,Module=Module,building=building)
                verubles[f"{total_veubles_complitions}Cal"] = building.sdiv(lhs=ver2,rhs=ver1,name=f"{total_veubles_complitions}Cal")

                r = verubles[f"{total_veubles_complitions}Cal"]

                total_veubles_complitions += 1
                return r
            
            elif key.fourse == "MODL":
                ver1 = compiling_to_IR([key.right],block,Module=Module,building=building)
                
                ver2 = compiling_to_IR([key.left],block,Module=Module,building=building)
                verubles[f"{total_veubles_complitions}Cal"] = building.urem(lhs=ver2,rhs=ver1,name=f"{total_veubles_complitions}Cal")

                r = verubles[f"{total_veubles_complitions}Cal"]

                total_veubles_complitions += 1
                return r
            
        elif key.byteType == "IDEN":
            eqr = compiling_to_IR([key.equals],block,Module=Module,building=building)
            if key.type == "int32":   
                ptr = building.alloca(typ=ir.IntType(32),name=key.name)
                verubles[key.name] = ptr
                building.store(eqr,ptr=ptr)

            if key.type == "float32":   
                ptr = building.alloca(typ=ir.DoubleType(),name=key.name)
                verubles[key.name] = ptr
                building.store(eqr,ptr=ptr)

        elif key.byteType == "CHAN":
            eqr = compiling_to_IR([key.equals],block,Module=Module,building=building)
            building.store(eqr,verubles[key.name])

        elif key.byteType == "int32":
            verubles[f"{total_veubles_complitions}Cal"] = ir.IntType(32)(key.number)
            old = f"{total_veubles_complitions}Cal"
            total_veubles_complitions += 1
            return verubles[old]
        
        elif key.byteType == "float32":
            verubles[f"{total_veubles_complitions}Cal"] = ir.DoubleType()(key.number)
            old = f"{total_veubles_complitions}Cal"
            total_veubles_complitions += 1
            return verubles[old]
        
        elif key.byteType == "ELM":
            
            ptr = verubles[key.name]
            o = building.load(ptr,f"{total_veubles_complitions}Cal")
            verubles[f"{total_veubles_complitions}load"] = o
            old = f"{total_veubles_complitions}load"
            total_veubles_complitions += 1
            return verubles[old]
        
        elif key.byteType == "RETURN":
            ret = compiling_to_IR([key.rt],block,Module,building)
            building.ret(ret)
        
