import sys
import linecache

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

def get_type(symbol, variables, cur, program, l, c) :
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
        semantical_error(program, int(l), int(c))
        return False

def semantical_error(file, l, c) :
    line = linecache.getline(file, l+1)
    while line[0]==' ' :
        line = line[1::]
        c-=1
    line = line.strip()
    print("At line %d:"%(l+1))
    print(line)
    print(" "*c+'^')

def semantical(file, program, debug=False) :
    variables = {}
    cur = None

    symbolt_f = open(file, "r")

    while (line:=symbolt_f.readline()) :
        line = line.split()
        if line[0]=="O" :
            typea = get_type(line[2], variables, cur, program, line[4], line[5])
            typeb = get_type(line[3], variables, cur, program, line[4], line[5])

            if not(typea) or not(typeb) : return False

            if line[1] not in operations_supported[typea][typeb] :
                print(f"Semantical error: Can't use operation {line[1]} between {line[2]} ({typea}) and {line[3]} ({typeb})")
                semantical_error(program, int(line[4]), int(line[5]))
                return False
            cur = operations_supported[typea][typeb][line[1]]

        elif line[0]=="D" :
            variables[line[1]] = {
                "type": line[2]
            }

        elif line[0]=="S" :
            typea = get_type(line[1], variables, cur, program, line[3], line[4])
            typeb = get_type(line[2], variables, cur, program, line[3], line[4])

            if typeb not in compatible[typea] :
                print(f"Semantical error: Can't store {line[2]} ({typeb}) in {line[1]} ({typea})")
                semantical_error(program, int(line[3]), int(line[4]))
                return False
    
    return True
    
    symbolt_f.close()

if __name__=="__main__" :
    if semantical("out.sdt", sys.argv[1], True) :
        print("Recognized!")
    else :
        sys.exit(1)
