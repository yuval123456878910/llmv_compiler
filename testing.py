from tokenizer import tokenizer
from order import ordered_line
from ast_builder import AST_builder
token= tokenizer("func('h');",["func"])
ord_line = ordered_line(token)
print(ord_line)
print(AST_builder(ord_line).name)
