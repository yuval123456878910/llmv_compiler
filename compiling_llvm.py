from llvmlite import ir

verubles = dict()
total_veubles_complitions = 0 # count all the prosses like var2, a1
def compiling_to_IR(ASTs, block= ir.Block, Module = ir.Module, building = ir.IRBuilder):
    global verubles, total_veubles_complitions
    for key in ASTs:
        if key.byteType == "FUNC":
            ll_term = ir.FunctionType(ir.IntType(32),[])
            func = ir.Function(Module, ll_term, key.name)
            entry_block = func.append_basic_block("entry")
            builder = ir.IRBuilder(entry_block)
            compiling_to_IR([key.block],block,Module,builder)
        
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
                verubles[key.name] = building.alloca(typ=ir.IntType(32),name=key.name)
                building.store(ir.IntType(32)(eqr),verubles[key.name])
            
        elif key.byteType == "int32":
            verubles[f"{total_veubles_complitions}Cal"] = ir.IntType(32)(key.number)
            old = f"{total_veubles_complitions}Cal"
            total_veubles_complitions += 1
            return verubles[old]
        
        
        elif key.byteType == "float32":
            verubles[f"{total_veubles_complitions}Cal"] = ir.FloatType()(key.number)
            old = f"{total_veubles_complitions}Cal"
            total_veubles_complitions += 1
            return verubles[old]
        
