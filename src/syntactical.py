import sys
from collections import deque

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
        if line[2]=='g' :
            if int(line[0]) not in transitions :
                transitions[int(line[0])] = {}
            transitions[int(line[0])][productions[line[1]]] = int(line[3])
        else :
            if int(line[0]) not in actions :
                actions[int(line[0])] = {}
            if line[2]=='a' :
                actions[int(line[0])][line[1]] = (line[2],None)
            else :
                actions[int(line[0])][line[1]] = (line[2],int(line[3]))
        
    grammar_f.close()

    return production_sizes, actions, transitions

def syntactical(tape, production_sizes, actions, transitions) :
    tape_f = open(tape, "r")

    stack = deque()
    stack.append(0)

    while (line:=tape_f.readline().split()) :
        c_state = stack.pop(); stack.append(c_state)
        act = actions[c_state][line[0]]
        while act[0]=='r' :
            for i in range(act[1]) : stack.pop() #reduce
            stack.append(transitions[stack.top()][act[1]])
            c_state = stack.pop(); stack.append(c_state)
            act = actions[c_state][line[0]]
        if act[0]=='a' :
            return True #accept
        stack.append(act[1]) #shift

    return False

    tape_f.close()

if __name__=="__main__" :
    production_sizes, actions, transitions = read_grammar(sys.argv[1])
    if syntactical("out.lex", production_sizes, actions, transitions) :
        print("Recognized!")
    else :
        print("Not recognized :(")
