from tokenizer import tokenizer
from order import ordered_line
from ast_builder import combiner
from compiling_llvm import compiling_to_IR
from llvmlite import ir
import sys
import os

file = open(sys.argv[1],"r")
output_name = sys.argv[2]
exe_name = sys.argv[3]
text = "int a= 4; a = 5;"
keywords = ["int", "str", "float","func","return"]
token = tokenizer(file.read(),keywords)
ord_line = ordered_line(token)
AST = combiner(ord_line) # the ast
print(AST)
Modle = ir.Module(sys.argv[1])
compiling_to_IR(AST,Module=Modle)
output = open(output_name,"w")
output.write(str(Modle))
output.close()

os.system(f"clang {output_name} -o {exe_name}")