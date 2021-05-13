#!/usr/bin/env pipenv-shebang

import sys, os
import fire
import lexical, syntactical, semantical, optimizer

lexical_grammar = "lexical.grammar.csv"
syntax_grammar = "syntax.grammar.txt"

def main(program, debug=0) :
    if not(os.path.isfile(program)) :
        print("Invalid program file!")

    debug = str(bin(debug))[2::]
    debug = (4-len(debug))*'0'+debug
    lexical_debug = int(debug[3])
    syntactical_debug = int(debug[2])
    semantical_debug = int(debug[1])
    optimizer_debug = int(debug[0])


    if not(lexical.lexical(lexical_grammar, program, lexical_debug)) :
        print("Lexical error(s), leaving...")
        os.remove("out.lex")
        sys.exit(1)
        
    if not(syntactical.syntactical(syntax_grammar, program, syntactical_debug)) :
        print("Syntactical error(s), leaving...")
        os.remove("out.lex")
        os.remove("out.sdt")
        os.remove("out.ic")
        sys.exit(1)

    if not(semantical.semantical("out.sdt", program, semantical_debug)) :
        print("Semantical error(s), leaving...")
        os.remove("out.lex")
        os.remove("out.sdt")
        os.remove("out.ic")
        sys.exit(1)

    optimizer.optimize("out.ic", optimizer_debug)

    if not(syntactical_debug) :
        os.remove("out.sdt")
        os.remove("out.ic")
    if not(lexical_debug) :
        os.remove("out.lex")
        

    print("Ok")

if __name__=="__main__" :
    fire.Fire(main)
else :
    print("Please do not import this file")
    sys.exit(1)
