import sys

def read_grammar(file) :
    productions = []
    production_sizes = []
    actions = {}
    transitions = {}

    grammar_f = open(file, "r")

    for i in range(int(grammar_f.readline())) :
        line = grammar_f.readline().split()
        production_sizes.append(len(line)-2)
        productions.append(line[0])

    while (line:=grammar_f.readline().split()) : 
        if line[2]=='g' :
            if line[0] not in transitions :
                transitions[line[0]] = {}
            transitions[line[0]][line[1]] = line[3]
        else :
            if line[0] not in actions :
                actions[line[0]] = {}
            if line[2]=='a' :
                actions[line[0]][line[1]] = line[2]
            else :
                actions[line[0]][line[1]] = (line[2],line[3])
        
    grammar_f.close()

    return production_sizes, actions, transitions

if __name__=="__main__" :
    read_grammar(sys.argv[1])
