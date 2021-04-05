import sys

errorstate = "<ErrorState>"

def construct(file) :
    table = {}
    final = {}
    initial = ""

    f = open(file, 'r')
    lines = f.read().splitlines()
    f.close()

    terminals = lines.pop(0).split(',')[1:]
    t_c = len(terminals)

    for line in lines :
        l_sp = list(line.split(','))
        rule = l_sp.pop(0)
        r_i = False
        if rule.startswith("->") :
            rule = rule[2:]
            r_i = True
        if rule.startswith("*") :
            rule = rule[1:]
            final[rule] = True
        else :
            final[rule] = False

        if r_i : initial = rule

        table[rule] = {}
        for i in range(t_c) :
            table[rule][terminals[i]] = l_sp[i]
    
    return table, final, initial

def read(table, final, initial, file) :
    f = open(file, 'r')
    lines = f.read().splitlines()
    f.close()

    lexemes = []
    for i in range(len(lines)) :
        lexemes+=map(lambda x : (x,i), lines[i].split())

    success = True
    for (lexeme,l) in lexemes :
        c_prod_old = errorstate
        c_prod = initial
        c_read = ''
        for char in lexeme :
            c_prod_old, c_prod = c_prod, table[c_prod][char]
            if (c_prod==errorstate and c_prod_old!=errorstate and final[c_prod_old]) :
                print("Success!(",c_read,"): ",c_prod_old, sep='')
                c_prod_old = errorstate
                c_prod = table[initial][char]
                c_read = ''
            c_read+=char

        if c_prod == errorstate :
            print('Error near "',c_read,'" (line ',l+1,')', sep='')
            success = False
        elif final[c_prod] :
            print("Success!(",c_read,"): ",c_prod, sep='')
        else :
            print('Error near "',c_read,'" (line ',l+1,')', sep='')
            success = False
    
    return success

table, final, initial = construct(sys.argv[1])
read(table, final, initial, sys.argv[2])
