'''
Parser for our Register language
'''

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
        stream.match('REGISTER')
        stream.match('COPY')
        exp(stream)
        return
    elif token.type in ['COPY']:
        stream.match('COPY')
        stream.match('REGISTER')
        return
    else:
        raise SyntaxError("syntax error at {}".format(token.value))

# exp : {NUMBER} NUMBER
#     | {REGISTER} REGISTER ({PLUS,MINUS,MULT,DIV} op REGISTER)?
def exp(stream):
    token = stream.pointer()
    if token.type in ['NUMBER']:
        stream.match('NUMBER')
        return
    elif token.type in ['REGISTER']:
        stream.match('REGISTER')
        if stream.pointer().type in ['PLUS','MINUS','MULT','DIV']:
            op(stream)
            stream.match('REGISTER')
        return
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
        return
    elif token.type in ['MINUS']:
        stream.match('MINUS')
        return
    elif token.type in ['MULT']:
        stream.match('MULT')
        return
    elif token.type in ['DIV']:
        stream.match('DIV')
        return
    else:
        raise SyntaxError("syntax error at {}".format(token.value))


# parser top-level driver
def parse(char_stream=None):
    from register_lexer import Lexer
    from sys import stdin
    try:
        if not char_stream:
            char_stream = stdin.read() # read from stdin
        token_stream = Lexer(char_stream)
        prog(token_stream) # call the parser function for start symbol
        if token_stream.end_of_file():
            print("parse successful")
        else:
            raise SyntaxError("syntax error at {}"
                              .format(token_stream.pointer().value))
    except SyntaxError as e:
        print("error: " + str(e))

if __name__ == "__main__":
    parse()
