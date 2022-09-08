import sys
from lexer import tokenize, Token

## parser is meant to take the tokens and make sure that they're in the correct spots and such

KEYWORDS = ["if", "for", "while", "func", "class", "new", "disp", "ret"]

class Error:
    def __init__(self, type, message):
        self.type = type
        self.msg = message
    def __repr__(self):
        return f'{self.type}: {self.msg}'

def throwError(err):
    print(err)
    exit()

class LineToken:
    def __init__(self, token, line):
        self.token = token
        self.lineNum = line
    def type(self):
        return self.token.type
    def value(self):
        return self.token.value
    def line(self):
        return self.lineNum
    def isOperator(self):
        return self.isOperator()

def parseTokens(fileName, debug):
    tokenLines = tokenize(fileName)
    orderedLineTokens = []
    for lineNum in range(len(tokenLines)):
        line = tokenLines[lineNum]
        for token in line:
            lineToken = LineToken(token, lineNum+1)
            orderedLineTokens.append(lineToken)
    if debug:
        print(tokenLines)
    t = 0
    lineCount = 1
    # check to see if all lines end with either a { or ;
    for line in tokenLines:
        if line[-1].type != 'LBRACE' and line[-1].type != 'EOS':
            eolErr = Error("SyntaxError", "Invalid end of line on line " + str(lineCount))
            throwError(eolErr)
        lineCount += 1
    # check to see if parentheses are good or not
    # first we can check to see if the parens are good and filled in
    missingClose = False
    parenArr = ['LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET']
    buildStr = []
    for lineToken in orderedLineTokens:
        if lineToken.type() in parenArr:
            buildStr.append(lineToken)
        if len(buildStr) > 1:
            size = len(buildStr) - 2
            lineTokenPair = buildStr[size:]
            pair = [lineTokenPair[0].type(), lineTokenPair[1].type()]
            if pair == ['LPAREN', 'RPAREN'] or pair == ['LBRACE', 'RBRACE'] or pair == ['LBRACKET', 'RBRACKET']:
                buildStr = buildStr[:size]
    if debug:
        print(buildStr)
    if buildStr != []:
        missingClose = True
        for rem in buildStr:
            print("Missing pair for " + rem.type() + " at line " + str(rem.line()))
    # now, we can check for correct usage of operators
    for t in range(len(orderedLineTokens)):
        curLineToken = orderedLineTokens[t]
        # initial check to see if LPAREN comes right after an operator type
        if curLineToken.isOperator():
            if orderedLineTokens[t+1].type() != "LPAREN":
                throwError(Error("SyntaxError"), "Need ( after operator")
