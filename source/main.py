import sys
from lexer import tokenize
from parser import parseTokens

def run(debug):
    progTokens = tokenize("prog.pf")
    if debug:
        print(progTokens)

debug = False
if len(sys.argv) >= 2 and sys.argv[1] == 'd':
    debug = True
run(debug)
