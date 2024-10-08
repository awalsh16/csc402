'''
Develop an sLL(1) parser together with a lexer for the language
dened above in Python based on your extended grammar. The parser
must be based on the techniques developed in class (Hint: you can use the
code calc parser and lexer developed in class as a starting point. This code
is available in the github.com/lutzhamel/plipy-code repository). Demon-
strate that your parser works by parsing the ve example programs above
- note, your parser should reject the last program with an error message.
'''

import re


token_specs = [
    #   type:        value 
    ('LPAREN',       r'\('),
    ('RPAREN',       r'\)'),
    ('STORE',        r'store'),
    ('PRINT',        r'print'),
    ('NUM',          r'[0-9]+'),
    ('VAR',          r'[a-zA-Z][a-zA-Z0-9_]*'),
    ('PLUS',         r'\+'),
    ('MINUS',        r'\-'),
    ('MULT',         r'\*'),
    ('DIV',          r'\/'),
    ('WHITESPACE',   r'[ \t\n]+'),
    ]

token_types = set(type for (type,_) in token_specs)

class Token:
    def __init__(self,type,value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({},{})'.format(self.type,self.value)
    
def tokenize(stream):
    tokens = []
    re_list = ['(?P<{}>{})'.format(type,re) for (type,re) in token_specs]
    combined_re = '|'.join(re_list)
    match_object_list = list(re.finditer(combined_re, stream))
    for mo in match_object_list:
        type = mo.lastgroup
        value = mo.group()
        if type == 'WHITESPACE':
            continue #ignore
        elif type == 'UNKNOWN':
            raise ValueError("unexpected character '{}'".format(value))
        else:
            tokens.append(Token(type, value))
    tokens.append(Token('EOF', '\eof'))
    return tokens


class Lexer:
    def __init__(self, input_string):
        self.tokens = tokenize(input_string)
        # the following is always valid because we will always have
        # at least the EOF token on the tokens list.
        self.curr_token_ix = 0

    def pointer(self):
        return self.tokens[self.curr_token_ix]

    def next(self):
        if not self.end_of_file():
            self.curr_token_ix += 1
        return self.pointer()

    def match(self, token_type):
        if token_type == self.pointer().type:
            tk = self.pointer()
            self.next()
            return tk
        elif token_type not in token_types:
            raise ValueError("unknown token type '{}'".format(token_type))
        else:
            raise SyntaxError('unexpected token {} while parsing, expected {}'
                              .format(self.pointer().type, token_type))

    def end_of_file(self):
        if self.pointer().type == 'EOF':
            return True
        else:
            return False

# test lexer
if __name__ == "__main__":

    prgm = \
    '''
    123
    + 1 2
    (+ 23 45 67)
    '''
    lexer = Lexer(prgm)

    while not lexer.end_of_file():
        tok = lexer.pointer()
        print(tok)
        lexer.match(tok.type)