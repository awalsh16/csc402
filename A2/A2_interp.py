'''
Parser for our Register language
'''
symboltable = None

# prog : ({REGISTER,COPY} stmt)*
def prog(stream):
  while stream.pointer().type in ['REGISTER','COPY']:
    stmt(stream)
  return

# stmt : {REGISTER} REGISTER COPY exp
#      | {COPY} COPY REGISTER
def stmt(stream):
    token = stream.pointer()
    if token.type in ['REGISTER']:
        
        global symboltable
        name = token.value
        stream.match('REGISTER')
        stream.match('COPY')
        value = exp(stream)
        symboltable[name] = value
        return None
    elif token.type in ['COPY']:
        
        stream.match('COPY')
        val = exp(stream)
        print(symboltable[val])
        return None
    else:
        raise SyntaxError("syntax error at {}".format(token.value))

# exp : {NUMBER} NUMBER
#     | {REGISTER} REGISTER ({PLUS,MINUS,MULT,DIV} op REGISTER)?
def exp(stream):
    token = stream.pointer()
    
    if token.type in ['NUMBER']:
        stream.match('NUMBER')
        return int(token.value)
    
    elif token.type in ['REGISTER']:
        vleft = token.value
        stream.match('REGISTER')
        if stream.pointer().type in ['PLUS','MINUS','MULT','DIV']:
            opfunc = op(stream)
            #stream.match('REGISTER')
            vright = exp(stream)
            return opfunc(symboltable[vleft], symboltable[vright])
        return token.value
    else:
        raise SyntaxError("syntax error at {}".format(token.value))

# op : {PLUS} PLUS
#    | {MINUS} MINUS
#    | {MULT} MULT
#    | {DIV} DIV
def op(stream):
    token = stream.pointer()
    if token.type in ['PLUS']:
        stream.match('PLUS')
        return lambda x, y: x + y
    elif token.type in ['MINUS']:
        stream.match('MINUS')
        return lambda x, y: x - y
    elif token.type in ['MULT']:
        stream.match('MULT')
        return lambda x, y: x * y
    elif token.type in ['DIV']:
        stream.match('DIV')
        return lambda x, y: x // y
    else:
        raise SyntaxError("syntax error at {}".format(token.value))


# interpreter top-level driver
def interp(char_stream=None):
    from A2_lexer import Lexer
    from sys import stdin
    global symboltable
    try:
        symboltable = dict()
        if not char_stream:
            char_stream = stdin.read() # read from stdin
        token_stream = Lexer(char_stream)
        prog(token_stream) # call the parser function for start symbol
        if token_stream.end_of_file():
            print("done!")
        else:
            raise SyntaxError("parse: syntax error at {}"
                              .format(token_stream.pointer().value))
    except Exception as e:
        print("error: " + str(e))


if __name__ == "__main__":
    interp()
