import sys

errorstate = "<ErrorState>"

def construct(file, debugMode) :
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

def read(table, final, initial, file, debugMode) :
    f = open(file, 'r')
    lines = f.read().splitlines()
    f.close()

    lexemes = []
    for i in range(len(lines)) :
        lexemes+=map(lambda x : (x,i), lines[i].split())
    
    #line col token value
    tape = open("out.lex", "w+")

    success = True
    c_l = -1
    for (lexeme,l) in lexemes :
        c_prod_old = errorstate
        c_prod = initial
        if (c_l!=l) :
            i_c = 0
            c_c = 0
            c_l = l
        c_read = ''
        for char in lexeme :
            #print(i_c+1,c_c+1)

            try :
                c_prod_old, c_prod = c_prod, table[c_prod][char]
            except :
                c_prod_old, c_prod = c_prod, errorstate
            if char not in table[c_prod_old] or c_prod==errorstate :
                if c_prod_old!=errorstate and final[c_prod_old] :
                    if (debugMode) : print("Success!(",c_read,"): ",c_prod_old," (l ",c_l+1," c ",i_c+1,')', sep='')
                    write_tape(tape,c_l,i_c,c_prod_old,c_read)
                    c_prod_old = errorstate
                    c_read = ''
                    i_c = c_c
                    try :
                        c_prod = table[initial][char]
                    except :
                        lexic_error(c_l,lines[c_l],c_c)
                        write_tape(tape,c_l,i_c,c_prod,c_read+char)
                        c_prod = initial
                        i_c+=1
                        c_c+=1
                        continue
                else :
                    lexic_error(c_l,lines[c_l],i_c)
                    write_tape(tape,c_l,i_c,c_prod,c_read+char)
                    c_prod_old = errorstate
                    c_read = ''
                    i_c=c_c+1
                    c_c+=1
                    c_prod = initial
                    continue
            c_read+=char
            c_c+=1

        if c_prod == errorstate :
            lexic_error(c_l,lines[c_l],i_c)
            write_tape(tape,c_l,i_c,c_prod,c_read)
            success = False
        elif final[c_prod] :
            if (debugMode) : print("Success!(",c_read,"): ",c_prod," (l ",c_l+1," c ",i_c+1,')', sep='')
            write_tape(tape,c_l,i_c,c_prod,c_read)
        elif c_read!='' :
            lexic_error(c_l,lines[c_l],i_c)
            write_tape(tape,c_l,i_c,errorstate,c_read)
            success = False
        i_c=c_c+1
        c_c+=1
    
    tape.close()
    return success

def lexic_error(l, line, column) :
    print("Lexic error at line %d:"%(l+1))
    print(line)
    print(" "*column+'^')

def write_tape(tape, line, col, token, value) :
    tape.write(str(line)+' '+str(col)+' '+str(token)+' '+str(value)+'\n')

def lexic(dfa, input, debugMode=False) :
    table, final, initial = construct(dfa, debugMode)
    read(table, final, initial, input, debugMode)

if __name__=="__main__" :
    lexic(sys.argv[1], sys.argv[2], True)
