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

class items:
    def __init__(self, items: list):
        self.items = items # <- list
        self.byteType = "LST" # -> list

    def append(self,item):
        self.items.append(item)

class keyword:
    arg = None
    name = ""
    def __init__(self,keyword):
        self.keyword = keyword
        self.byteType = "KEYWORD"

class function:
    block = []
    args = None
    
    def __init__(self,name,return_type):
        self.name = name
        self.type = return_type
        self.byteType = "FUNC"


class integer:
    def __init__(self,number):
        self.number = number
        self.byteType = "int32"

class float32:
    def __init__(self,number):
        self.number = number
        self.byteType = "float32"

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
    def __init__(self,name, equals, type):
        self.name = name
        self.equals = equals
        self.type = type
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

def closed_last_loc(order_line, start: int, letter=None, func= lambda x: x[0]) -> int:
    end_at: int = 0
    at_location = start
    for _ in order_line[start:]:       
        if func(order_line[at_location]) == letter:
            end_at = at_location
        at_location += 1
    return end_at

def all_letter_location(order_line, start = 0, letter=None, func= lambda x: x[0],end = -1 ) -> list[int]:
    locations = []
    at_location = start
    
    for _ in order_line[start:end]:
        if func(order_line[at_location]) == letter:
            locations.append(at_location)
        at_location += 1
    
    return locations

def AST_builder(ordered_line: list):
    # lowest num finder

    if ordered_line == []:
        return None

    current_EOL = 0
    loc1 = 0
    Node_main = None

    
    
    location_target = 0
    loc = 0
    lowest_target = 200
    
    for ord_token in ordered_line:
        if ord_token[0] != None:
            if lowest_target > ord_token[0]:
                lowest_target = ord_token[0]
                location_target = loc
                
        loc += 1
    for tok in ordered_line:
        if tok[1] == "EOL":
            if ordered_line[location_target][0] != None and ordered_line[location_target][1] != "EOL":
                if tok[3] - tok[3] % 100 >= ordered_line[location_target][0] - ordered_line[location_target][0] % 100:
                    current_EOL = loc1
                    break
        loc1 += 1   
    
    
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
                print("No element behind")
                exit(1)

            elif ordered_line[location_target-1][1] != "elm":
                print("No element behind")
                exit(1)
            elif ordered_line[location_target-2][1] != "keyword":
                print("No type specevide")
                exit(1)
            elif ordered_line[location_target-2][2] not in ["str","int","float"]:
                print("Keyword not exact")
                exit(1)
            type_asset = ""
            if ordered_line[location_target-2][2] == "str":
                type_asset = "str"
            elif ordered_line[location_target-2][2] == "int":
                type_asset = "int32"
            elif ordered_line[location_target-2][2] == "int":
                type_asset = "float32"
            Node_main = identifier(ordered_line[location_target-1][2], AST_builder(ordered_line[location_target+1:current_EOL+1]),type_asset)

         
        
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
            Node_main = function(ordered_line[location_target+1][2],ordered_line[location_target+2][2])
            location, start_loc = nerest_end_sep(ordered_line,location_target,current_EOL)
            if location+1 != start_loc:
                Node_main.arg = AST_builder(ordered_line[location+1:start_loc+1])
            Node_main.block = combiner(ordered_line[location_target+3:len(ordered_line)])[0]
            
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
            Node_main = BLOCK(combiner(ordered_line[location_target+1:location_end])[0])
            return Node_main

        elif ordered_line[location_target][2] == ",":
            Node_main = items([])
            item_end = closed_last_loc(ordered_line,location_target,",",lambda x: x[2])
            all_item_locations = all_letter_location(ordered_line,location_target,",",lambda x: x[2],item_end+1)
            location = 0
            last_loc = location
            
            while location < len(all_item_locations):
                
                Node_main.append(AST_builder(ordered_line[last_loc:all_item_locations[location]]))
                last_loc = all_item_locations[location]+1
                location += 1
                
            
    elif ordered_line[location_target][1] == "int":
        Node_main = integer(int(ordered_line[location_target][2]))

    elif ordered_line[location_target][1] == "float":
        Node_main = float32(float(ordered_line[location_target][2]))

    elif ordered_line[location_target][1] == "str":
        Node_main = string(ordered_line[location_target][2])
    return Node_main

def combiner(order_line: list):
    all_eol_locations = []
    loc1 = 0
    first_letter = order_line[0]
    for tok in order_line: 
        if tok[0] != None:
            first_letter = tok
            break

    for or_l in order_line:
        #print(first_letter[0],or_l)
        if (or_l[0] == None) and (or_l[1] == 'EOL') and (first_letter[0] - first_letter[0] % 100) == (or_l[3] - or_l[3] % 100) and (or_l[2] == ''):
            all_eol_locations.append(loc1)
        loc1 += 1

    last_eol_location = 0
    list_eols = []
    
    

    for loc in all_eol_locations:
        if order_line[loc][3] - order_line[loc][3] % 100 == first_letter[0] - first_letter[0] % 100: 
            list_eols.append(AST_builder(order_line[last_eol_location:loc+1]))
        last_eol_location = loc
    return list_eols