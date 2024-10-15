def instr_list(stream):
    while stream.pointer().type in ['LABEL', 'PRINT', 'PUSH', 'POP', 'STORE', 'ASK', 'DUP', 'ADD', 'SUB', 'MUL', 'DIV', 'EQU', 'LEQ', 'JUMPT', 'JUMPF', 'JUMP', 'STOP', 'NOOP']:
        labeled_instr(stream)
    return

def labeled_instr(stream):
    token = stream.pointer()
    if(token.type in ['LABEL']):
        label_def(stream)
        instr(stream)
        return
    
    elif(token.type in ['PRINT']):
        instr(stream)
        return
    
    elif(token.type in ['PUSH']):
        instr(stream)
        return
    
    elif(token.type in ['POP']):
        instr(stream)
        return
    
    elif(token.type in ['STORE']):
        instr(stream)
        return
    
    elif(token.type in ['ASK']):
        instr(stream)
        return
    
    elif(token.type in ['DUP']):
        instr(stream)
        return
    
    elif(token.type in ['ADD']):
        instr(stream)
        return
    
    elif(token.type in ['SUB']):
        instr(stream)
        return
    
    elif(token.type in ['MUL']):
        instr(stream)
        return
    
    elif(token.type in ['DIV']):
        instr(stream)
        return
    
    elif(token.type in ['EQU']):
        instr(stream)
        return
    
    elif(token.type in ['LEQ']):
        instr(stream)
        return
    
    elif(token.type in ['JUMPT']):
        instr(stream)
        return
    
    elif(token.type in ['JUMPF']):
        instr(stream)
        return
    
    elif(token.type in ['JUMP']):
        instr(stream)
        return
    
    elif(token.type in ['STOP']):
        instr(stream)
        return
    
    elif(token.type in ['NOOP']):
        instr(stream)
        return

    else:
        raise SyntaxError("exp: syntax at {}".format(token.value))


def label_def(stream):
    token = stream.pointer()
    if(token.type in ['LABEL']):
        stream.match('LABEL')
        stream.match('COLON')
        return
    
    else:
        raise SyntaxError("exp: syntax at {}".format(token.value))


def instr(stream):
    token = stream.pointer()
    if(token.type in ['PRINT']):
        stream.match('PRINT')
        stream.match('SEMI')
        return
    
    elif(token.type in ['PUSH']):
        stream.match('PUSH')
        arg(stream)
        stream.match('SEMI')
        return
    
    elif(token.type in ['POP']):
        stream.match('POP')
        stream.match('SEMI')
        return
    
    elif(token.type in ['STORE']):
        stream.match('STORE')
        stream.match('VAR')
        stream.match('SEMI')
        return
    
    elif(token.type in ['ASK']):
        stream.match('ASK')
        stream.match('SEMI')
        return
    
    elif(token.type in ['DUP']):
        stream.match('DUP')
        stream.match('SEMI')
        return
    
    elif(token.type in ['ADD']):
        stream.match('ADD')
        stream.match('SEMI')
        return
    
    elif(token.type in ['SUB']):
        stream.match('SUB')
        stream.match('SEMI')
        return
    
    elif(token.type in ['MUL']):
        stream.match('MUL')
        stream.match('SEMI')
        return
    
    elif(token.type in ['DIV']):
        stream.match('DIV')
        stream.match('SEMI')
        return
    
    elif(token.type in ['EQU']):
        stream.match('EQU')
        stream.match('SEMI')
        return
    
    elif(token.type in ['LEQ']):
        stream.match('LEQ')
        stream.match('SEMI')
        return
    
    elif(token.type in ['JUMPT']):
        stream.match('JUMPT')
        stream.match('LABEL')
        stream.match('SEMI')
        return
    
    elif(token.type in ['JUMPF']):
        stream.match('JUMPF')
        stream.match('LABEL')
        stream.match('SEMI')
        return
    
    elif(token.type in ['JUMP']):
        stream.match('JUMP')
        stream.match('LABEL')
        stream.match('SEMI')
        return
    
    elif(token.type in ['STOP']):
        stream.match('STOP')
        stream.match('SEMI')
        return
    
    elif(token.type in ['NOOP']):
        stream.match('NOOP')
        stream.match('SEMI')
        return
    
    else:
        raise SyntaxError("exp: syntax at {}".format(token.value))

def arg(stream):
    token = stream.pointer()
    if(token.type in ['NUM']):
        stream.match('NUM')
        return
    elif(token.type in ['VAR']):
        stream.match('VAR')
        return
    else:
        raise SyntaxError("exp: syntax at {}".format(token.value))




def parse():
    from M_lexer import Lexer
    from sys import stdin
    try:
        char_stream = stdin.read() # read from stdin
        token_stream = Lexer(char_stream)
        instr_list(token_stream) # call the parser function for start symbol
        if token_stream.end_of_file():
            print("parse successful")
        else:
            raise SyntaxError("bad syntax at {}"
                              .format(token_stream.pointer()))
    except Exception as e:
        print("error: " + str(e))


if __name__ == "__main__":
    parse()