import sys
from lexer import tokenize

def run():
    progTokens = tokenize("prog.pf")
    print(progTokens)

run()
