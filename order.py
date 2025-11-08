def ordered_line(tokened_line) -> list:
    loc = 0
    ordered_line_return = []
    order_num = 0 

    while loc < len(tokened_line):
        tokened_letter = tokened_line[loc] 

        if tokened_letter[0] == "sep":
            if tokened_letter[1] == "(":
                order_num += 100
            elif tokened_letter[1] == ")":
                order_num -= 100
            elif tokened_letter[1] in ["{" ,"}"]:
                ordered_line_return.append([order_num+5,tokened_letter[0],tokened_letter[1]])
                if tokened_letter[1] == "{":
                    order_num += 100
                else:
                    order_num -= 100
                order_num = max(0,order_num)

            elif tokened_letter[1] in [","]:
                ordered_line_return.append([order_num+2,tokened_letter[0],tokened_letter[1]])
                
        elif tokened_letter[0] == "keyword":
            ordered_line_return.append([order_num+1,tokened_letter[0],tokened_letter[1]])

        elif tokened_letter[0] == "opr":
            if tokened_letter[1] == "+":
                ordered_line_return.append([order_num+10,tokened_letter[0],tokened_letter[1]])
            elif tokened_letter[1] == "-":
                ordered_line_return.append([order_num+10,tokened_letter[0],tokened_letter[1]])
            
            elif tokened_letter[1] == "*":
                ordered_line_return.append([order_num+40,tokened_letter[0],tokened_letter[1]])
            elif tokened_letter[1] == "/":
                ordered_line_return.append([order_num+40,tokened_letter[0],tokened_letter[1]])
            elif tokened_letter[1] == "%":
                ordered_line_return.append([order_num+40,tokened_letter[0],tokened_letter[1]])
            
            elif tokened_letter[1] == "=":
                ordered_line_return.append([order_num+5,tokened_letter[0],tokened_letter[1]])
        else:
            if tokened_letter[0] == "EOL":
                ordered_line_return.append([None,tokened_letter[0],tokened_letter[1],order_num])
            else:
                ordered_line_return.append([None,tokened_letter[0],tokened_letter[1]])
        loc += 1
    return ordered_line_return