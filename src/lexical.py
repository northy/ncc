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
        reading = ''
        jinit = -1
        for j in range(len(lines[i])) :
            if lines[i][j] == ' ' :
                if jinit == -1 : continue
                lexemes.append((reading, i, jinit))
                reading = ''
                jinit=-1
                continue
            if jinit == -1 : jinit = j
            reading+=lines[i][j]
        if jinit == -1 : continue
        lexemes.append((reading, i, jinit))
    
    #line col token value
    tape = open("out.lex", "w+")

    success = True
    c_l = -1
    for (lexeme,l,c) in lexemes :
        c_prod_old = errorstate
        c_prod = initial
        if (c_l!=l) :
            i_c = c
            c_c = c
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
                        success = False
                        write_tape(tape,c_l,i_c,c_prod,c_read+char)
                        c_prod = initial
                        i_c+=1
                        c_c+=1
                        continue
                else :
                    lexic_error(c_l,lines[c_l],i_c)
                    success = False
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
        c_l = -1
    
    write_tape(tape, len(lines), 0, '$', '$')
    
    tape.close()
    return success

def lexic_error(l, line, column) :
    print("Lexic error at line %d:"%(l+1))
    while line[0]==' ' :
        line = line[1::]
        column-=1
    line = line.strip()
    print(line)
    print(" "*column+'^')

def write_tape(tape, line, col, token, value) :
    tape.write(str(token)+' '+str(line)+' '+str(col)+' '+str(value)+'\n')

def lexical(dfa, input, debugMode=False) :
    table, final, initial = construct(dfa, debugMode)
    return read(table, final, initial, input, debugMode)

if __name__=="__main__" :
    if lexical(sys.argv[1], sys.argv[2], True) :
        print("Recognized!")
