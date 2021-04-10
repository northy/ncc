import sys
from sys import exit
from collections import deque

def read_grammar(file) :
    productions = []
    production_sizes = {}
    actions = {}
    transitions = {}

    try :
        grammar_f = open(file, "r")

        for i in range(int(grammar_f.readline())) :
            line = grammar_f.readline().split()
            if line[0] in production_sizes :
                print("Unexpected error")
                exit(1)
            production_sizes[i] = len(line)-2
            productions.append(line[0])
        
        while (line:=grammar_f.readline().split()) :
            if line[2]=='g' :
                if int(line[0]) not in transitions :
                    transitions[int(line[0])] = {}
                if line[1] in transitions[int(line[0])] :
                    print("Unexpected error")
                    exit(1)
                transitions[int(line[0])][line[1]] = int(line[3])
            else :
                if int(line[0]) not in actions :
                    actions[int(line[0])] = {}
                if line[2]=='a' :
                    actions[int(line[0])][line[1]] = (line[2],None)
                elif line[2]=='r' :
                    actions[int(line[0])][line[1]] = (line[2],int(line[3]))
                else :
                    actions[int(line[0])][line[1]] = (line[2],int(line[3]))
        
        grammar_f.close()
    except Exception as e :
        print("Grammar file error on line {}".format(sys.exc_info()[-1].tb_lineno))
        print(e)
        exit(1)

    return productions, production_sizes, actions, transitions

def syntactical(tape, productions, production_sizes, actions, transitions) :
    try :
        tape_f = open(tape, "r")

        stack = deque()
        stack.append(0)

        while (line:=tape_f.readline().split()) :
            c_state = stack.pop(); stack.append(c_state)
            if c_state not in actions or line[0] not in actions[c_state] :
                if c_state in actions:
                    print("Syntax error:", c_state, "doesn't have an action from", line[0])
                else :
                    print("Syntax error:", c_state, "has no actions")
                return False
            act = actions[c_state][line[0]]
            while act[0]=='r' :
                print("Reducing", production_sizes[act[1]], "elements of production", act[1], "from", line[0])
                for i in range(production_sizes[act[1]]) : stack.pop() #reduce
                c_state = stack.pop(); stack.append(c_state)
                print("Transitioning from", c_state, "with", productions[act[1]])
                if c_state not in transitions or productions[act[1]] not in transitions[c_state] :
                    if c_state in transitions:
                        print("Syntax error:", c_state, "doesn't transition from", productions[act[1]])
                    else :
                        print("Syntax error:", c_state, "has no transitions")
                    return False
                stack.append(transitions[c_state][productions[act[1]]])
                c_state = stack.pop(); stack.append(c_state)
                if c_state not in actions or line[0] not in actions[c_state] :
                    if c_state in actions:
                        print("Syntax error:", c_state, "doesn't have an action from", line[0])
                    else :
                        print("Syntax error:", c_state, "has no actions")
                    return False
                act = actions[c_state][line[0]]
                continue
            if act[0]=='a' :
                return True #accept
            print("Shifting",act[1],"from",line[0])
            stack.append(act[1]) #shift

        return False

        tape_f.close()
    except Exception as e :
        print("Tape file error on line {}".format(sys.exc_info()[-1].tb_lineno))
        print(e)
        exit(1)

if __name__=="__main__" :
    productions, production_sizes, actions, transitions = read_grammar(sys.argv[1])
    if syntactical("out.lex", productions, production_sizes, actions, transitions) :
        print("Recognized!")
