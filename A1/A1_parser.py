'''
Develop an sLL(1) parser together with a lexer for the language
dened above in Python based on your extended grammar. The parser
must be based on the techniques developed in class (Hint: you can use the
code calc parser and lexer developed in class as a starting point. This code
is available in the github.com/lutzhamel/plipy-code repository). Demon-
strate that your parser works by parsing the ve example programs above
- note, your parser should reject the last program with an error message.
'''


from sys import stdin

def prog(stream):
    while stream.pointer().type in ['LPAREN', 'VAR', 'NUM']:
        sexp(stream)
    return
    
def sexp(stream):
    token = stream.pointer()
    if token.type in ['LPAREN']:
        stream.match('LPAREN')
        exp(stream)
        stream.match('RPAREN')
        return
    
    if token.type in ['VAR']:
        stream.match('VAR')
        return
    
    if token.type in ['NUM']:
        stream.match('NUM')
        return
    
    else:
        raise SyntaxError("exp: syntax at {}".format(token.value))
    
def exp(stream):
    token = stream.pointer()
    if token.type in ['PLUS']:
        stream.match('PLUS')
        sexp(stream)
        sexp(stream)
        return
    
    if token.type in ['MINUS']:
        stream.match('MINUS')
        sexp(stream)
        sexp(stream)
        return
        
    if token.type in ['MULT']:
        stream.match('MULT')
        sexp(stream)
        sexp(stream)
        return
    
    if token.type in ['DIV']:
        stream.match('DIV')
        sexp(stream)
        sexp(stream)
        return
    
    if token.type in ['STORE']:
        stream.match('STORE')
        stream.match('VAR')
        sexp(stream)
        return
        
    if token.type in ['PRINT']:
        stream.match('PRINT')
        sexp(stream)
        return
        
    else:
        raise SyntaxError("exp: syntax at {}".format(token.value))
    
def parse():
    from A1_lexer import Lexer
    from sys import stdin
    try:
        char_stream = stdin.read() # read from stdin
        token_stream = Lexer(char_stream)
        prog(token_stream) # call the parser function for start symbol
        if token_stream.end_of_file():
            print("parse successful")
        else:
            raise SyntaxError("bad syntax at {}"
                              .format(token_stream.pointer()))
    except Exception as e:
        print("error: " + str(e))


if __name__ == "__main__":
    parse()