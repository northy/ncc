import sys

def read_grammar(file) :
    productions = {}
    production_sizes = []
    actions = {}
    transitions = {}

    grammar_f = open(file, "r")

    i=0
    for _ in range(int(grammar_f.readline())) :
        line = grammar_f.readline().split()
        production_sizes.append(len(line)-2)
        if line[0] not in productions :
            productions[line[0]] = i
            i+=1

    while (line:=grammar_f.readline().split()) : 
        print(line)
        if line[2]=='g' :
            if int(line[0]) not in transitions :
                transitions[int(line[0])] = {}
            transitions[int(line[0])][productions[line[1]]] = int(line[3])
        else :
            if int(line[0]) not in actions :
                actions[int(line[0])] = {}
            if line[2]=='a' :
                actions[int(line[0])][line[1]] = line[2]
            else :
                actions[int(line[0])][line[1]] = (line[2],int(line[3]))
        
    grammar_f.close()

    print(actions)

    return production_sizes, actions, transitions

def syntactical(production_sizes, ) :
    pass

if __name__=="__main__" :
    read_grammar(sys.argv[1])
