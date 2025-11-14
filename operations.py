from tokenizer import tokenizer
from order import ordered_line
from ast_builder import combiner
from compiling_llvm import compiling_to_IR
from llvmlite import ir
import sys

file = open(sys.argv[1],"r")
output_name = sys.argv[2]
keywords = ["int", "str", "float","func"]
token = tokenizer(file.read(),keywords)
ord_line = ordered_line(token)
AST = combiner(ord_line) # the ast
Modle = ir.Module("MAIN")
compiling_to_IR(AST,Module=Modle)
output = open(output_name,"w")
output.write(str(Modle))
output.close()