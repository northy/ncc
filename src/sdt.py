def __operand_number(semantical_global, sdt_stack, symbol_table) :
    obj = {}
    obj["value"] = int(sdt_stack[0]["lexval"])
    return obj

def __mulexp_mulexp1_mulexpd(semantical_global, sdt_stack, symbol_table) :
    obj = {}
    if sdt_stack[1]["type"] == "*" :
        obj["value"] = sdt_stack[0]["value"] * sdt_stack[1]["value"]
    return obj

def __mulexp_termexp(semantical_global, sdt_stack, symbol_table) :
    obj = {}
    obj["value"] = sdt_stack[0]["value"]
    return obj

def __mulexpd_mult_termexp(semantical_global, sdt_stack, symbol_table) :
    obj = {}
    obj["type"] = "*"
    obj["value"] = sdt_stack[1]["value"]
    return obj

def __termexp_operand(semantical_global, sdt_stack, symbol_table) :
    obj = {}
    obj["value"] = sdt_stack[0]["value"]
    return obj

sdt_mapping = {
    9: __operand_number, #<operand>::= number
    26: __mulexp_mulexp1_mulexpd, #<mulexp>::= <mulexp1> <mulexp'>
    27: __mulexp_termexp, #<mulexp>::= <termexp>
    28: __mulexpd_mult_termexp, #<mulexp'>::= '*' <termexp>
    30: __termexp_operand, #<termexp> ::= <operand>
}
