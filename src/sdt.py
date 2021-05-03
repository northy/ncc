def generate_name(semantical_global) :
    semantical_global["namegen_t"]+=1
    return "%T"+str(semantical_global["namegen_t"])

def __operand_ID(semantical_global, sdt_stack, symbol_table, intermediate_code) :
    obj = {}
    obj["operandtype"] = "memory"
    obj["operandowner"] = sdt_stack[0]["lexval"]
    obj["operand"] = semantical_global["ids"][sdt_stack[0]["lexval"]]["memshift"] if sdt_stack[0]["lexval"] in semantical_global["ids"] else -1
    obj["line"] = sdt_stack[0]["line"]
    obj["column"] = sdt_stack[0]["column"]
    return obj

def __operand_number(semantical_global, sdt_stack, symbol_table, intermediate_code) :
    obj = {}
    obj["operandtype"] = "numeric"
    obj["operandowner"] = None
    obj["operand"] = int(sdt_stack[0]["lexval"])
    obj["line"] = sdt_stack[0]["line"]
    obj["column"] = sdt_stack[0]["column"]
    return obj

def __operand_minus_number(semantical_global, sdt_stack, symbol_table, intermediate_code) :
    obj = {}
    obj["operandtype"] = "numeric"
    obj["operandowner"] = None
    obj["operand"] = -int(sdt_stack[1]["lexval"])
    obj["line"] = sdt_stack[1]["line"]
    obj["column"] = sdt_stack[1]["column"]
    return obj

def __cmpexp_boolexp(semantical_global, sdt_stack, symbol_table, intermediate_code) :
    obj = {}
    obj["operandtype"] = sdt_stack[0]["operandtype"]
    obj["operandowner"] = sdt_stack[0]["operandowner"]
    obj["operand"] = sdt_stack[0]["operand"]
    obj["line"] = sdt_stack[0]["line"]
    obj["column"] = sdt_stack[0]["column"]
    return obj

def __boolexp_addexp(semantical_global, sdt_stack, symbol_table, intermediate_code) :
    obj = {}
    obj["operandtype"] = sdt_stack[0]["operandtype"]
    obj["operandowner"] = sdt_stack[0]["operandowner"]
    obj["operand"] = sdt_stack[0]["operand"]
    obj["line"] = sdt_stack[0]["line"]
    obj["column"] = sdt_stack[0]["column"]
    return obj

def __addexp_addexp1_addexpd(semantical_global, sdt_stack, symbol_table, intermediate_code) :
    obj = {}

    name_t = generate_name(semantical_global)

    symbol_table.write("O " + sdt_stack[1]["type"] + ' ' + name_t + ' ')

    if sdt_stack[0]["operandtype"]=="memory" :
        symbol_table.write(sdt_stack[0]["operandowner"] + ' ')
        intermediate_code.write(name_t + " = $" + sdt_stack[0]["operandowner"] + ' ' + sdt_stack[1]["type"] + " ")
    if sdt_stack[0]["operandtype"]=="numeric" :
        symbol_table.write(str(sdt_stack[0]["operand"]) + ' ')
        intermediate_code.write(name_t + " = " + str(sdt_stack[0]["operand"]) + ' ' + sdt_stack[1]["type"] + " ")
    if sdt_stack[0]["operandtype"]=="register" :
        symbol_table.write(sdt_stack[0]["operand"] + ' ')
        intermediate_code.write(name_t + " = " + sdt_stack[0]["operand"] + ' ' + sdt_stack[1]["type"] + " ")
    
    if sdt_stack[1]["operandtype"]=="memory" :
        symbol_table.write(sdt_stack[1]["operandowner"] + ' ' + sdt_stack[1]["line"] + ' ' + sdt_stack[1]["column"] + '\n')
        intermediate_code.write('$' + sdt_stack[1]["operandowner"] + "\n")
    if sdt_stack[1]["operandtype"]=="numeric" :
        symbol_table.write(str(sdt_stack[1]["operand"]) + ' ' + sdt_stack[1]["line"] + ' ' + sdt_stack[1]["column"] + '\n')
        intermediate_code.write(str(sdt_stack[1]["operand"]) + "\n")
    if sdt_stack[1]["operandtype"]=="register" :
        symbol_table.write(sdt_stack[1]["operand"] + ' ' + sdt_stack[1]["line"] + ' ' + sdt_stack[1]["column"] + "\n")
        intermediate_code.write(sdt_stack[1]["operand"] + "\n")
    
    obj["operandtype"] = "register"
    obj["operandowner"] = None
    obj["operand"] = name_t
    obj["line"] = sdt_stack[1]["line"]
    obj["column"] = sdt_stack[1]["column"]
    return obj

def __addexp_mulexp(semantical_global, sdt_stack, symbol_table, intermediate_code) :
    obj = {}
    obj["operandtype"] = sdt_stack[0]["operandtype"]
    obj["operandowner"] = sdt_stack[0]["operandowner"]
    obj["operand"] = sdt_stack[0]["operand"]
    obj["line"] = sdt_stack[0]["line"]
    obj["column"] = sdt_stack[0]["column"]
    return obj

def __addexpd_plus_mulexp(semantical_global, sdt_stack, symbol_table, intermediate_code) :
    obj = {}
    obj["type"] = "+"
    obj["operandtype"] = sdt_stack[1]["operandtype"]
    obj["operandowner"] = sdt_stack[1]["operandowner"]
    obj["operand"] = sdt_stack[1]["operand"]
    obj["line"] = sdt_stack[0]["line"]
    obj["column"] = sdt_stack[0]["column"]
    return obj

def __addexpd_minus_mulexp(semantical_global, sdt_stack, symbol_table, intermediate_code) :
    obj = {}
    obj["type"] = "-"
    obj["operandtype"] = sdt_stack[1]["operandtype"]
    obj["operandowner"] = sdt_stack[1]["operandowner"]
    obj["operand"] = sdt_stack[1]["operand"]
    obj["line"] = sdt_stack[0]["line"]
    obj["column"] = sdt_stack[0]["column"]
    return obj

def __mulexp_mulexp1_mulexpd(semantical_global, sdt_stack, symbol_table, intermediate_code) :
    obj = {}

    name_t = generate_name(semantical_global)

    symbol_table.write("O " + sdt_stack[1]["type"] + ' ' + name_t + ' ')

    if sdt_stack[0]["operandtype"]=="memory" :
        symbol_table.write(sdt_stack[0]["operandowner"] + ' ')
        intermediate_code.write(name_t + " = $" + sdt_stack[0]["operandowner"] + ' ' + sdt_stack[1]["type"] + " ")
    if sdt_stack[0]["operandtype"]=="numeric" :
        symbol_table.write(str(sdt_stack[0]["operand"]) + ' ')
        intermediate_code.write(name_t + " = " + str(sdt_stack[0]["operand"]) + ' ' + sdt_stack[1]["type"] + " ")
    if sdt_stack[0]["operandtype"]=="register" :
        symbol_table.write(sdt_stack[0]["operand"] + ' ')
        intermediate_code.write(name_t + " = " + sdt_stack[0]["operand"] + ' ' + sdt_stack[1]["type"] + " ")
    
    if sdt_stack[1]["operandtype"]=="memory" :
        symbol_table.write(sdt_stack[1]["operandowner"] + ' ' + sdt_stack[1]["line"] + ' ' + sdt_stack[1]["column"] + '\n')
        intermediate_code.write('$' + sdt_stack[1]["operandowner"] + "\n")
    if sdt_stack[1]["operandtype"]=="numeric" :
        symbol_table.write(str(sdt_stack[1]["operand"]) + ' ' + sdt_stack[1]["line"] + ' ' + sdt_stack[1]["column"] + '\n')
        intermediate_code.write(str(sdt_stack[1]["operand"]) + "\n")
    if sdt_stack[1]["operandtype"]=="register" :
        symbol_table.write(sdt_stack[1]["operand"] + ' ' + sdt_stack[1]["line"] + ' ' + sdt_stack[1]["column"] + "\n")
        intermediate_code.write(sdt_stack[1]["operand"] + "\n")
    
    obj["operandtype"] = "register"
    obj["operandowner"] = None
    obj["operand"] = name_t
    obj["line"] = sdt_stack[1]["line"]
    obj["column"] = sdt_stack[1]["column"]
    return obj

def __mulexp_termexp(semantical_global, sdt_stack, symbol_table, intermediate_code) :
    obj = {}
    obj["operandtype"] = sdt_stack[0]["operandtype"]
    obj["operandowner"] = sdt_stack[0]["operandowner"]
    obj["operand"] = sdt_stack[0]["operand"]
    obj["line"] = sdt_stack[0]["line"]
    obj["column"] = sdt_stack[0]["column"]
    return obj

def __mulexpd_mult_termexp(semantical_global, sdt_stack, symbol_table, intermediate_code) :
    obj = {}
    obj["type"] = "*"
    obj["operandtype"] = sdt_stack[1]["operandtype"]
    obj["operandowner"] = sdt_stack[1]["operandowner"]
    obj["operand"] = sdt_stack[1]["operand"]
    obj["line"] = sdt_stack[0]["line"]
    obj["column"] = sdt_stack[0]["column"]
    return obj

def __mulexpd_div_termexp(semantical_global, sdt_stack, symbol_table, intermediate_code) :
    obj = {}
    obj["type"] = "/"
    obj["operandtype"] = sdt_stack[1]["operandtype"]
    obj["operandowner"] = sdt_stack[1]["operandowner"]
    obj["operand"] = sdt_stack[1]["operand"]
    obj["line"] = sdt_stack[0]["line"]
    obj["column"] = sdt_stack[0]["column"]
    return obj

def __termexp_operand(semantical_global, sdt_stack, symbol_table, intermediate_code) :
    obj = {}
    obj["operandtype"] = sdt_stack[0]["operandtype"]
    obj["operandowner"] = sdt_stack[0]["operandowner"]
    obj["operand"] = sdt_stack[0]["operand"]
    obj["line"] = sdt_stack[0]["line"]
    obj["column"] = sdt_stack[0]["column"]
    return obj

def __termexp_p_expression_p(semantical_global, sdt_stack, symbol_table, intermediate_code) :
    obj = {}
    obj["operandtype"] = sdt_stack[1]["operandtype"]
    obj["operandowner"] = sdt_stack[1]["operandowner"]
    obj["operand"] = sdt_stack[1]["operand"]
    obj["line"] = sdt_stack[1]["line"]
    obj["column"] = sdt_stack[1]["column"]
    return obj

def __expression_cmpex(semantical_global, sdt_stack, symbol_table, intermediate_code) :
    obj = {}

    name_t = None
    obj["line"] = None
    obj["column"] = None

    if not(isinstance(sdt_stack[0], int)) : #not all expressions are implemented
        if (sdt_stack[0]["operandtype"]!="register") : #perform an operation to get the operand on a register
            name_t = generate_name(semantical_global) 
            obj["line"] = sdt_stack[0]["line"]
            obj["column"] = sdt_stack[0]["column"]
            if sdt_stack[0]["operandtype"]=="memory" :
                symbol_table.write("O + " + name_t + ' ' + sdt_stack[0]["operandowner"] + " 0 " + sdt_stack[0]["line"] + ' ' + sdt_stack[0]["column"] + "\n")
                intermediate_code.write(name_t + " = $" + sdt_stack[0]["operandowner"] + "\n")
            if sdt_stack[0]["operandtype"]=="numeric" :
                symbol_table.write("O + " + name_t + ' ' + str(sdt_stack[0]["operand"]) + " 0 " + sdt_stack[0]["line"] + ' ' + sdt_stack[0]["column"] + "\n")
                intermediate_code.write(name_t + " = " + str(sdt_stack[0]["operand"]) + "\n")
        else :
            name_t = sdt_stack[0]["operand"]
    
    obj["operandtype"] = "register"
    obj["operandowner"] = None
    obj["operand"] = name_t
    return obj

def __assignment_assign_expression_semicolon(semantical_global, sdt_stack, symbol_table, intermediate_code) :
    obj = {}
    obj["operandtype"] = sdt_stack[1]["operandtype"]
    obj["operandowner"] = sdt_stack[1]["operandowner"]
    obj["operand"] = sdt_stack[1]["operand"]
    obj["line"] = sdt_stack[0]["line"]
    obj["column"] = sdt_stack[0]["column"]
    return obj

def __attribute_ID_assignment(semantical_global, sdt_stack, symbol_table, intermediate_code) :
    if sdt_stack[1]["operandtype"]=="memory" :
        symbol_table.write("S " + sdt_stack[0]["lexval"] + ' ' + sdt_stack[1]["operandowner"] + ' ' + sdt_stack[1]["line"] + ' ' + sdt_stack[1]["column"] + '\n')
        intermediate_code.write('$' + sdt_stack[0]["lexval"] + " = $" + sdt_stack[1]["operandowner"] + '\n')
    if sdt_stack[1]["operandtype"]=="numeric" :
        symbol_table.write("S " + sdt_stack[0]["lexval"] + ' ' + str(sdt_stack[1]["operand"]) + ' ' + sdt_stack[1]["line"] + ' ' + sdt_stack[1]["column"] + '\n')
        intermediate_code.write('$' + sdt_stack[0]["lexval"] + " = " + str(sdt_stack[1]["operand"]) + '\n')
    if sdt_stack[1]["operandtype"]=="register" :
        symbol_table.write("S " + sdt_stack[0]["lexval"] + ' ' + sdt_stack[1]["operand"] + ' ' + sdt_stack[1]["line"] + ' ' + sdt_stack[1]["column"] + "\n")
        intermediate_code.write('$' + sdt_stack[0]["lexval"] + " = " + sdt_stack[1]["operand"] + '\n')
    
    return {}

def __type_int(semantical_global, sdt_stack, symbol_table, intermediate_code) :
    obj = {}
    obj["type"] = "int"
    obj["size"] = 4
    return obj

def __declaration_type_ID_declarationd(semantical_global, sdt_stack, symbol_table, intermediate_code) :
    symbol_table.write("D " + sdt_stack[1]["lexval"] + ' ' + sdt_stack[0]["type"] + ' ' + str(semantical_global["memshift"]) + '\n')
    semantical_global["ids"][sdt_stack[1]["lexval"]] = {
        "type": sdt_stack[0]["type"],
        "memshift": semantical_global["memshift"]
    }
    if ("type" in sdt_stack[2]) :
        if sdt_stack[2]["operandtype"]=="memory" :
            symbol_table.write("S " + sdt_stack[1]["lexval"] + ' ' + sdt_stack[2]["operandowner"] + ' ' + sdt_stack[2]["line"] + ' ' + sdt_stack[2]["column"] + '\n')
            intermediate_code.write('$' + sdt_stack[1]["lexval"] + " = $" + sdt_stack[2]["operandowner"] + '\n')
        if sdt_stack[2]["operandtype"]=="numeric" :
            symbol_table.write("S " + sdt_stack[1]["lexval"] + ' ' + str(sdt_stack[2]["operand"]) + ' ' + sdt_stack[2]["line"] + ' ' + sdt_stack[2]["column"] + '\n')
            intermediate_code.write('$' + sdt_stack[1]["lexval"] + " = " + str(sdt_stack[2]["operand"]) + '\n')
        if sdt_stack[2]["operandtype"]=="register" :
            symbol_table.write("S " + sdt_stack[1]["lexval"] + ' ' + sdt_stack[2]["operand"] + ' ' + sdt_stack[2]["line"] + ' ' + sdt_stack[2]["column"] + "\n")
            intermediate_code.write('$' + sdt_stack[1]["lexval"] + " = " + sdt_stack[2]["operand"] + '\n')

    semantical_global["memshift"] += sdt_stack[0]["size"]
    return {}

def __declarationd_assignment(semantical_global, sdt_stack, symbol_table, intermediate_code) :
    obj = {}
    obj["type"] = "o"
    obj["operandtype"] = sdt_stack[0]["operandtype"]
    obj["operandowner"] = sdt_stack[0]["operandowner"]
    obj["operand"] = sdt_stack[0]["operand"]
    obj["line"] = sdt_stack[0]["line"]
    obj["column"] = sdt_stack[0]["column"]
    return obj

def __declarationd_semicolon(semantical_global, sdt_stack, symbol_table, intermediate_code) :
    return {}

sdt_mapping = {
    8: __operand_ID, #<operand>::= 'ID'
    9: __operand_number, #<operand>::= 'number'
    10: __operand_minus_number, #<operand>::= '-' 'number'
    13: __cmpexp_boolexp, #<cmpexp>::= <boolexp>
    21: __boolexp_addexp, #<boolexp>::= <addexp>
    22: __addexp_addexp1_addexpd, #<addexp>::= <addexp1> <addexp'>
    23: __addexp_mulexp, #<addexp>::= <mulexp>
    24: __addexpd_plus_mulexp, #<addexp'>::= '+' <mulexp>
    25: __addexpd_minus_mulexp, #<addexp'>::= '-' <mulexp>
    26: __mulexp_mulexp1_mulexpd, #<mulexp>::= <mulexp1> <mulexp'>
    27: __mulexp_termexp, #<mulexp>::= <termexp>
    28: __mulexpd_mult_termexp, #<mulexp'>::= '*' <termexp>
    29: __mulexpd_div_termexp, #<mulexp'>::= '/' <termexp>
    30: __termexp_operand, #<termexp>::= <operand>
    31: __termexp_p_expression_p, #<termexp>::= '(' <expression> ')'
    32: __expression_cmpex, #<expression>::= <cmpexp>
    33: __assignment_assign_expression_semicolon, #<assignment>::= '=' <expression> ';'
    34: __attribute_ID_assignment, #<attribute>::= 'ID' <assignment>
    35: __type_int, #<type> ::= int
    37: __declaration_type_ID_declarationd, #<declaration> ::= <type> ID <declaration'>
    38: __declarationd_assignment, #<declaration'> ::= <assignment>
    39: __declarationd_semicolon, #<declaration'> ::= ';'
}
