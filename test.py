import sys
from lexer import tokenize

def main():
    progTokens = tokenize("prog.pf")
    print(progTokens)

main()
