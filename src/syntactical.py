import sys
from sys import exit
from collections import deque
import linecache

from sdt import sdt_mapping

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

def tailq_pop(tailq, count) :
    for i in range(count) : tailq.pop(len(tailq)-1)

def stack_pop(stack, count) :
    for i in range(count) : stack.pop()
    return stack_top(stack)

def stack_top(stack) :
    top = stack.pop()
    stack.append(top)
    return top

def stack_push(stack, val) :
    stack.append(val)
    return val

def syntactical_ops(tape, program, productions, production_sizes, actions, transitions, debug) :
    tape_f = open(tape, "r")

    sem_tailq = []
    sem_global = {"memshift": 0, "namegen_t": 0, "ids": {}}
    sdt_outfile = open("out.sdt", "w+")
    ic_outfile = open("out.ic", "w+")
    stack = deque()
    stack.append(0)

    while (line:=tape_f.readline().split()) :
        c_state = stack_top(stack)
        if c_state not in actions or line[0] not in actions[c_state] :
            if debug :
                if c_state in actions:
                    print("Syntax error:", c_state, "doesn't have an action from", line[0])
                else :
                    print("Syntax error:", c_state, "has no actions")
            syntactical_error(program, int(line[1]), int(line[2]))
            return False
        act = actions[c_state][line[0]]
        while act[0]=='r' :
            #Syntax Directed Translation
            cur_sdt_stack = sem_tailq[-production_sizes[act[1]]:]
            if debug : print(act[1], cur_sdt_stack)
            tailq_pop(sem_tailq, production_sizes[act[1]])

            if act[1] in sdt_mapping :
                sem_tailq.append(sdt_mapping[act[1]](sem_global, cur_sdt_stack, sdt_outfile, ic_outfile))
            else :
                sem_tailq.append(act[1])

            if debug : print("Reducing", production_sizes[act[1]], "elements of production", act[1], "from", line[0])

            c_state = stack_pop(stack, production_sizes[act[1]]) #reduce
            if debug : print("Transitioning from", c_state, "with", productions[act[1]])
            if c_state not in transitions or productions[act[1]] not in transitions[c_state] :
                if debug :
                    if c_state in transitions:
                        print("Syntax error:", c_state, "doesn't transition from", productions[act[1]])
                    else :
                        print("Syntax error:", c_state, "has no transitions")
                syntactical_error(program, int(line[1]), int(line[2]))
                return False
            c_state = stack_push(stack, transitions[c_state][productions[act[1]]])
            if c_state not in actions or line[0] not in actions[c_state] :
                if debug :
                    if c_state in actions:
                        print("Syntax error:", c_state, "doesn't have an action from", line[0])
                    else :
                        print("Syntax error:", c_state, "has no actions")
                syntactical_error(program, int(line[1]), int(line[2]))
                return False
            act = actions[c_state][line[0]]
            continue
        if act[0]=='a' :
            return True #accept
        if debug : print("Shifting",act[1],"from",line[0])
        sem_tailq.append({"lexval": line[3], "line": line[1], "column": line[2]})
        stack_push(stack, act[1]) #shift

    if debug : print("Syntax error:", line[0], "isn't final!")
    syntactical_error(program, int(line[1]), int(line[2]))
    return False

    sdt_outfile.close()
    ic_outfile.close()
    tape_f.close()

def syntactical_error(file, l, c) :
    line = linecache.getline(file, l+1)
    while len(line)>0 and line[0]==' ' :
        line = line[1::]
        c-=1
    if len(line)==0 :
        print("Syntactical error near the end of line %d (maybe missing ';'?)"%(l))
        return
    line = line.strip()
    print("Syntactical error near line %d:"%(l+1))
    print(line)
    print(" "*c+'^')

def syntactical(grammar, program, debug) :
    productions, production_sizes, actions, transitions = read_grammar(grammar)
    return syntactical_ops("out.lex", program, productions, production_sizes, actions, transitions, debug)

if __name__=="__main__" :
    if syntactical(sys.argv[1], sys.argv[2], True) :
        print("Recognized!")
