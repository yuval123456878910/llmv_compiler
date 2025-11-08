from tokenizer import tokenizer
from order import ordered_line
from ast_builder import combiner
keywords = ["int", "str", "float","func"]
token = tokenizer("func hi int() {1+1; 2*2;};",keywords)
ord_line = ordered_line(token)
AST = combiner(ord_line) # the ast
print((AST[0]))
