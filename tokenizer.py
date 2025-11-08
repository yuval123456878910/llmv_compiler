def tokenizer(line: str,keyword) -> list:
    loc = 0
    # stuct = [["string","hi"]]
    token_line = []
    word = ""
    current_type = ""
    is_text = False
    seperators = ["(",")","[","]",".",",","{","}"]
    ending_letter = None
    
    while loc < len(line):
        digit = line[loc]

        is_a_number = digit.isnumeric()
        is_a_text = digit.isalpha()
        is_a_operator = not is_a_text and not is_a_number

        if word in keyword:
            current_type = "keyword"

        if digit == '"' or digit == "'":
            if ending_letter == digit or ending_letter == None:
                is_text = not is_text

                if is_text:
                    if current_type != "str" and word != "":
                        token_line.append([current_type,word])
                        word = ""
                    current_type = "str"

                if not is_text:
                    token_line.append([current_type,word])
                    digit = ""
                    word = ""
                    current_type = ""
            else:
                word += digit

            loc += 1
            continue
        
        elif (digit == " "  or digit == "") and not is_text:
            if word and current_type:
               token_line.append([current_type,word])
               digit = ""
               word = ""
               digit = ""
               current_type = ""

            loc += 1
            continue
        
        elif current_type == "int" and digit == ".":
            current_type = "float"

        elif is_text:
            current_type = "str"
        
        elif digit in seperators:
            if word != "":
                token_line.append([current_type,word])
            word = ""
            current_type = "sep"
            token_line.append([current_type,digit])
            loc += 1
            continue

        elif is_a_number:
            if current_type != "int" and word != "" and current_type != "elm" and current_type != "float":
                token_line.append([current_type,word])
                word = ""
                current_type = "int"
            else:
                if current_type != "elm" and current_type != "float": 
                    current_type = "int"
                

        elif is_a_text and digit != "":
            if current_type != "elm" and word != "":
                token_line.append([current_type,word])
                word = ""
                current_type = "elm"
            current_type = "elm"

        elif is_a_operator:
            if digit == ";":
                if word != "": 
                    token_line.append([current_type,word])
                word = ""
                current_type = "EOL"
                token_line.append([current_type,word])
                word = ""
                current_type = ""
                loc += 1
                continue
                

            elif current_type != "opr" and word != "":
                token_line.append([current_type,word])
                word = ""
                current_type = "opr"
                
            else:
                current_type = "opr"
        
        
            

        word += digit
        loc += 1

    return token_line
