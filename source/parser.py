import sys
from lexer import tokenize

## parser is meant to take the tokens and make sure that they're in the correct spots and such

KEYWORDS = ["if", "for", "while", "func", "class", "new", "show", "give"]

class Error:
    def __init__(self, type, message):
        self.type = type
        self.msg = message
    def __repr__(self):
        return f'{self.type}: {self.msg}'

def throwError(err):
    print(err)
    exit()

def parseTokens(fileName):
    allTokens = tokenize(fileName)
    t = 0
    while t < len(allTokens):
        t++
