from sys import exit

operations_supported = {
    "int": {
        "int": {
            "+": "int",
            "-": "int",
            "*": "int",
            "/": "int"
        }
    }
}

compatible = {
    "int": {
        "int"
    }
}

def get_type(symbol, variables, cur) :
    if symbol == "%" :
        return cur

    try :
        int(symbol)
        return "int"
    except : pass

    try :
        return variables[symbol]["type"]
    except :
        print("Semantical error: variable used but not declared:", symbol)
        exit(1)

def semantical(file, debug=False) :
    variables = {}
    cur = None

    symbolt_f = open(file, "r")

    while (line:=symbolt_f.readline()) :
        line = line.split()
        if line[0]=="O" :
            typea = get_type(line[2], variables, cur)
            typeb = get_type(line[3], variables, cur)

            if line[1] not in operations_supported[typea][typeb] :
                print(f"Semantical error: Can't use operation {line[1]} between {line[2]} ({typea}) and {line[3]} ({typeb})")
                return False
            cur = operations_supported[typea][typeb][line[1]]

        elif line[0]=="D" :
            variables[line[1]] = {
                "type": line[2]
            }

        elif line[0]=="S" :
            typea = get_type(line[1], variables, cur)
            typeb = get_type(line[2], variables, cur)

            if typeb not in compatible[typea] :
                print(f"Semantical error: Can't store {line[2]} ({typeb}) in {line[1]} ({typea})")
    
    return True
    
    symbolt_f.close()

if __name__=="__main__" :
    if semantical("out.sdt", True) :
        print("Recognized!")
    else :
        exit(1)
