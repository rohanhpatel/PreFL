import sys

## lexer is meant to tokenize the file and put meaning behind everything

class Token:
    def __init__(self, typ, value=None):
        self.type = typ
        self.val = value
    def __repr__(self):
        if self.val:
            return f'{self.type}: {self.val}'
        return f'{self.type}'
    def isOperator(self):
        if self.type == "ASSIGN" or self.type == "EQ" or self.type.find("GT") != -1 or self.type.find("LT") != -1 or self.type.find("PLUS") != -1 or self.type.find("MINUS") != -1 or self.type.find("MULT") != -1 or self.type.find("DIV") != -1 or self.type.find("MOD") != -1 or self.type.find("NOT") != -1:
            return True
        return False

def isValidNumber(numStr):
    viableChars = "1234567890."
    for c in numStr:
        if not c in viableChars:
            return False
    return True

def eqAfter(nwsStr, i, constant): #helper function for tokenize
    if i+1 < len(nwsStr) and nwsStr[i+1] == '=':
        return [Token(constant + '_EQ'), 1]
    else:
        return [Token(constant), 0]

def createNum(nwsStr, i):
    type = 'int'
    fullNum = ''
    inc = 0
    while i+inc < len(nwsStr) and (nwsStr[i+inc].isdigit() or nwsStr[i+inc] == '.'):
        if nwsStr[i+inc] == '.':
            type = 'float'
        fullNum += nwsStr[i+inc]
        inc += 1
    if type == 'float':
        return [Token("FLOAT", float(fullNum)), inc-1]
    else:
        return [Token("INT", int(fullNum)), inc-1]

def createVar(nwsStr, i):
    varName = ''
    inc = 0
    while i+inc < len(nwsStr) and (nwsStr[i+inc].isalpha() or nwsStr[i+inc].isdigit() or nwsStr[i+inc] == "_"):
        varName += nwsStr[i+inc]
        inc += 1
    return [Token("VAR", varName), inc-1]

def tokenize(fileName):
    tokens = []
    curStr = ""
    nextStrs = []
    parseFile = open(fileName)
    for line in parseFile:
        tmp = line.split(" ")
        nws = [value for value in tmp if value != '' and value != '\n' and value != '\t'] # nws contains all tokens not separated by whitespace
        nwsStr = ''.join(nws)
        tmpTkArr = []
        i = 0
        while i < len(nwsStr):
            # print(i)
            chr = nwsStr[i]
            if chr == '(':
                tmpTkArr.append(Token('LPAREN'))
            elif chr == ')':
                tmpTkArr.append(Token('RPAREN'))
            elif chr == '{':
                tmpTkArr.append(Token('LBRACE'))
            elif chr == '}':
                tmpTkArr.append(Token('RBRACE'))
            elif chr == '[':
                tmpTkArr.append(Token('LBRACKET'))
            elif chr == ']':
                tmpTkArr.append(Token('RBRACKET'))
            elif chr == ';':
                tmpTkArr.append(Token('EOS'))
            elif chr == ',':
                tmpTkArr.append(Token('SEP'))
            elif chr == '=': # could be = or ==
                # did this one differently because assign is a special operator
                if i+1 < len(nwsStr) and nwsStr[i+1] == '=':
                    tmpTkArr.append(Token('EQ'))
                    i += 1
                else:
                    tmpTkArr.append(Token('ASSIGN'))
            elif chr == '+': # could be + or +=
                tmpRes = eqAfter(nwsStr, i, "PLUS")
                tmpTkArr.append(tmpRes[0])
                i += tmpRes[1]
            elif chr == '-': # could be - or -=
                tmpRes = eqAfter(nwsStr, i, "MINUS")
                tmpTkArr.append(tmpRes[0])
                i += tmpRes[1]
            elif chr == '*': # could be * or *=
                tmpRes = eqAfter(nwsStr, i, "MULT")
                tmpTkArr.append(tmpRes[0])
                i += tmpRes[1]
            elif chr == '/': # could be / or /=
                tmpRes = eqAfter(nwsStr, i, "DIV")
                tmpTkArr.append(tmpRes[0])
                i += tmpRes[1]
            elif chr == '%': # could be % or %=
                tmpRes = eqAfter(nwsStr, i, "MOD")
                tmpTkArr.append(tmpRes[0])
                i += tmpRes[1]
            elif chr == '<': # could be < or <=
                tmpRes = eqAfter(nwsStr, i, "LT")
                tmpTkArr.append(tmpRes[0])
                i += tmpRes[1]
            elif chr == '>': # could be < or <=
                tmpRes = eqAfter(nwsStr, i, "GT")
                tmpTkArr.append(tmpRes[0])
                i += tmpRes[1]
            elif chr == '!': # could be ! or !=
                tmpRes = eqAfter(nwsStr, i, "NOT")
                tmpTkArr.append(tmpRes[0])
                i += tmpRes[1]
            elif chr.isdigit(): # we have a number :)))
                tmpRes = createNum(nwsStr, i)
                tmpTkArr.append(tmpRes[0])
                i += tmpRes[1]
            elif chr == '_' or chr.isalpha(): # we have a variable :)))
                tmpRes = createVar(nwsStr, i)
                tmpTkArr.append(tmpRes[0])
                i += tmpRes[1]
            else:
                tmpTkArr.append(chr)
            i += 1
        tmpTkArr.remove('\n')
        tokens += [tmpTkArr]
    return tokens
