#!/usr/bin/env python3

import sys, os
import lexical, syntactical, semantical

lexical_grammar = "lexical.grammar.csv"
syntax_grammar = "syntax.grammar.txt"

if __name__=="__main__" :
    if len(sys.argv)!=2 :
        print("Please use: python ncc.py <program>")
        sys.exit(1)
    program = sys.argv[1]
    if not(os.path.isfile(program)) :
        print("Invalid program file!")

    debug = False

    if not(lexical.lexical(lexical_grammar, program, debug)) :
        print("Lexical error(s), leaving...")
        os.remove("out.lex")
        sys.exit(1)
    if not(syntactical.syntactical(syntax_grammar, program, debug)) :
        print("Syntactical error(s), leaving...")
        os.remove("out.lex")
        os.remove("out.sdt")
        os.remove("out.ic")
        sys.exit(1)
    if not(semantical.semantical("out.sdt", program, debug)) :
        print("Syntactical error(s), leaving...")
        os.remove("out.lex")
        os.remove("out.sdt")
        os.remove("out.ic")
        sys.exit(1)
    os.remove("out.lex")
    os.remove("out.sdt")

    print("Ok")

else :
    print("Please do not import this file")
    sys.exit(1)
