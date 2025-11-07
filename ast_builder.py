from sys import exit

class Node:
    left = None
    right = None
    term = None
    fourse = None
    value_term = None
    def __init__(self,expr,byteType):
        self.expr = expr
        self.byteType = byteType

class operator:
    fourse = None
    right = None
    left = None
    def __init__(self, opr):
        self.operator = opr
        self.byteType = "OPR"

class keyword:
    arg = None
    name = ""
    def __init__(self,keyword):
        self.keyword = keyword
        self.byteType = "KEYWORD"

class integer:
    def __init__(self,number):
        self.number = number
        self.byteType = "int32"

class string:
    def __init__(self,text):
        self.text = text
        self.byteType = "str"

class BLOCK:
    def __init__(self,lines_compiled):
        self.expr = "BLOCK"
        self.lines = lines_compiled
        self.byteType = "BLOCK"

class identifier:
    def __init__(self,name, equals):
        self.name = name
        self.equals = equals
        self.byteType = "IDEN"

def nerest_end_sep(order_line,location,end):
    # fix ptoblom
    stop = 0
    loc = 0
    start = 0
    for token in order_line[location:end+1]:
        if token[1] == "sep":
            if stop == 0:
                start = loc
            if token[2] == "(":
                stop += 1
            elif token[2] == ")":
                stop -= 1
            else:
                loc += 1
        else:
            loc += 1 
        
    if stop == 0 and loc != 0:
        return start, loc
    print("the sep did not end.")
    exit(1)

def AST_builder(ordered_line: list):
    # lowest num finder

    if ordered_line == []:
        return None

    current_EOL = 0
    loc = 0
    Node_main = None

    for tok in ordered_line:
        if tok[1] == "EOL":
            current_EOL = loc
            break
        loc += 1    
    del loc

    
    location_target = 0
    loc = 0
    lowest_target = 200
    for ord_token in ordered_line:
        if ord_token[0] != None:
            if lowest_target > ord_token[0]:
                lowest_target = ord_token[0]
                location_target = loc
                
        loc += 1
    if ordered_line[location_target][1] == "opr":
        Node_main = operator(ordered_line[location_target][2])
        
        if ordered_line[location_target][2] == "=":
            Node_main.fourse = "SETV" # set values
        elif ordered_line[location_target][2] == "+":
            Node_main.fourse = "ADDI" # addition
        elif ordered_line[location_target][2] == "-":
            Node_main.fourse = "SUPT" # suptraction
        elif ordered_line[location_target][2] == "*":
            Node_main.fourse = "MULT" # multiplecation
        elif ordered_line[location_target][2] == "/":
            Node_main.fourse = "DIVI" # division
        elif ordered_line[location_target][2] == "%":
            Node_main.fourse = "MODL" # modlue
       
        if Node_main.fourse == "SETV":
            
            if location_target <= 0:
                print("no element behind")
                exit(1)

            elif ordered_line[location_target-1][1] != "elm":
                print("no element behind")
                exit(1)

            Node_main = identifier(ordered_line[location_target-1][2], AST_builder(ordered_line[location_target+1:current_EOL+1]))

         
        
        else:
            Node_main.right = AST_builder(ordered_line[location_target:current_EOL])
            Node_main.left = AST_builder(ordered_line[:location_target])
            if Node_main.right == Node(None,""):
                print("NO astrebute aveible")
                exit(1)
            elif Node_main.left == Node(None,""):
                print("NO astrebute aveible")
                exit(1)

    elif ordered_line[location_target][1] == "keyword":
        Node_main = keyword(ordered_line[location_target][2])
        if ordered_line[location_target][2] == "func":
            location, start_loc = nerest_end_sep(ordered_line,location_target,current_EOL)
            Node_main.arg = AST_builder(ordered_line[location+1:start_loc+1])
            Node_main.name = "func"
            return Node_main
        
    elif ordered_line[location_target][1] == "sep":
        if ordered_line[location_target][2] == "{":
            current_piese = 0
            location_end = location_target
            for find_end in ordered_line[location_end:]:
                if find_end[2]  == "{":
                    current_piese += 1
                elif find_end[2] == "}":
                    current_piese -= 1
                if current_piese == 0:
                    break
                location_end += 1
            
            if current_piese > 0:
                print("BLOCK did not end. the BLOCK start at",location_target)
                exit(1)

            Node_main = BLOCK(AST_builder(ordered_line[location_target+1:location_end]))
            return Node_main


    elif ordered_line[location_target][1] == "int":
        Node_main = integer(ordered_line[location_target][2])
    
    elif ordered_line[location_target][1] == "str":
        Node_main = string(ordered_line[location_target][2])
    return Node_main