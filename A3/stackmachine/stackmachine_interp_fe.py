'''
Frontend for our stack machine interpreter

instr_list : ({NAME,PRINT,PUSH,POP,STORE,ASK,DUP,ADD,SUB,MUL,DIV,EQU,LEQ,JUMPT,JUMPF,JUMP,STOP,NOOP} labeled_instr)*

labeled_instr : {NAME} label_def instr
              | {PRINT,PUSH,POP,STORE,ASK,DUP,ADD,SUB,MUL,DIV,EQU,LEQ,JUMPT,JUMPF,JUMP,STOP,NOOP} instr

label_def : {NAME} label COLON

instr : {PRINT} PRINT ({MSG}MSG)? SEMI
      | {PUSH} PUSH ({NUMBER}num|{NAME}var) SEMI
      | {POP} POP SEMI
      | {STORE} STORE var SEMI
      | {ASK} ASK ({MSG}MSG)? SEMI
      | {DUP} DUP SEMI
      | {ADD} ADD SEMI
      | {SUB} SUB SEMI
      | {MUL} MUL SEMI
      | {DIV} DIV SEMI
      | {EQU} EQU SEMI
      | {LEQ} LEQ SEMI
      | {JUMPT} JUMPT label SEMI
      | {JUMPF} JUMPF label SEMI
      | {JUMP} JUMP label SEMI
      | {STOP} STOP ({MSG}MSG)? SEMI
      | {NOOP} NOOP SEMI

label : {NAME} NAME
var : {NAME} NAME
num : {NUMBER} NUMBER


'''

from stackmachine_interp_state import state

# lookahead sets for parser
instr_lookahead = [
    'PRINT',
    'PUSH',
    'POP',
    'STORE',
    'ASK',
    'DUP',
    'ADD',
    'SUB',
    'MUL',
    'DIV',
    'EQU',
    'LEQ',
    'JUMPT',
    'JUMPF',
    'JUMP',
    'STOP',
    'NOOP',
    ]
labeled_instr_lookahead = instr_lookahead + ['NAME']

# instr_list : ({NAME,PRINT,PUSH,POP,STORE,ASK,DUP,ADD,SUB,MUL,DIV,EQU,LEQ,JUMPT,JUMPF,JUMP,STOP,NOOP} labeled_instr)*
def instr_list(stream):
  while stream.pointer().type in labeled_instr_lookahead:
    labeled_instr(stream)
  return None

# labeled_instr : {NAME} label_def instr
#               | {PRINT,PUSH,POP,STORE,ASK,DUP,ADD,SUB,MUL,DIV,EQU,LEQ,JUMPT,JUMPF,JUMP,STOP,NOOP} instr
def labeled_instr(stream):
    token = stream.pointer()
    if token.type in ['NAME']:
        l = label_def(stream)
        i = instr(stream)
        state.label_table[l] = state.instr_ix
        state.program.append(i)
        state.instr_ix += 1
        return None
    elif token.type in instr_lookahead:
        i = instr(stream)
        state.program.append(i)
        state.instr_ix += 1
        return None
    else:
        raise SyntaxError("labeled_instr: syntax error at {}"
                          .format(token.value))

# label_def : {NAME} label COLON
def label_def(stream):
    token = stream.pointer()
    if token.type in ['NAME']:
        l = label(stream)
        stream.match('COLON')
        return l
    else:
        raise SyntaxError("label_def: syntax error at {}"
                          .format(token.value))

# instr : {PRINT} PRINT ({MSG}MSG)? SEMI
#       | {PUSH} PUSH ({NUMBER}num|{NAME}var) SEMI
#       | {POP} POP SEMI
#       | {STORE} STORE var SEMI
#       | {ASK} ASK ({MSG}MSG)? SEMI
#       | {DUP} DUP SEMI
#       | {ADD} ADD SEMI
#       | {SUB} SUB SEMI
#       | {MUL} MUL SEMI
#       | {DIV} DIV SEMI
#       | {EQU} EQU SEMI
#       | {LEQ} LEQ SEMI
#       | {JUMPT} JUMPT label SEMI
#       | {JUMPF} JUMPF label SEMI
#       | {JUMP} JUMP label SEMI
#       | {STOP} STOP ({MSG}MSG)? SEMI
#       | {NOOP} NOOP SEMI
def instr(stream):
    token = stream.pointer()
    if token.type in ['PRINT']:
        stream.match('PRINT')
        if stream.pointer().type == 'MSG':
            tk = stream.match('MSG')
            t = ('PRINT', tk.value)
        else:
            t = ('PRINT', None)
        stream.match('SEMI')
        return t
    elif token.type in ['PUSH']:
        stream.match('PUSH')
        if stream.pointer().type == 'NUMBER':
            e = num(stream)
        elif stream.pointer().type == 'NAME':
            e = var(stream)
        else:
            raise SyntaxError("push: syntax error at {}"
                              .format(stream.pointer().value))
        stream.match('SEMI')
        return ('PUSH', e)
    elif token.type in ['POP']:
        stream.match('POP')
        return ('POP',)
    elif token.type in ['STORE']:
        stream.match('STORE')
        v = var(stream)
        stream.match('SEMI')
        return ('STORE',v)
    elif token.type in ['ASK']:
        stream.match('ASK')
        if stream.pointer().type == 'MSG':
            tk = stream.match('MSG')
            t = ('ASK', tk.value)
        else:
            t = ('ASK', None)
        stream.match('SEMI')
        return t
    elif token.type in ['DUP']:
        stream.match('DUP')
        stream.match('SEMI')
        return ('DUP',)
    elif token.type in ['ADD']:
        stream.match('ADD')
        stream.match('SEMI')
        return ('ADD',)
    elif token.type in ['SUB']:
        stream.match('SUB')
        stream.match('SEMI')
        return ('SUB',)
    elif token.type in ['MUL']:
        stream.match('MUL')
        stream.match('SEMI')
        return ('MUL',)
    elif token.type in ['DIV']:
        stream.match('DIV')
        stream.match('SEMI')
        return ('DIV',)
    elif token.type in ['EQU']:
        stream.match('EQU')
        stream.match('SEMI')
        return ('EQU',)
    elif token.type in ['LEQ']:
        stream.match('LEQ')
        stream.match('SEMI')
        return ('LEQ',)
    elif token.type in ['JUMPT']:
        stream.match('JUMPT')
        l = label(stream)
        stream.match('SEMI')
        return ('JUMPT', l)
    elif token.type in ['JUMPF']:
        stream.match('JUMPF')
        l = label(stream)
        stream.match('SEMI')
        return ('JUMPF', l)
    elif token.type in ['JUMP']:
        stream.match('JUMP')
        l = label(stream)
        stream.match('SEMI')
        return ('JUMP', l)
    elif token.type in ['STOP']:
        stream.match('STOP')
        if stream.pointer().type == 'MSG':
            tk = stream.match('MSG')
            t = ('STOP', tk.value)
        else:
            t = ('STOP', None)
        stream.match('SEMI')
        return t
    elif token.type in ['NOOP']:
        stream.match('NOOP')
        stream.match('SEMI')
        return ('NOOP',)
    else:
        raise SyntaxError("instr: syntax error at {}"
                          .format(token.value))


# label : {NAME} NAME
def label(stream):
    token = stream.pointer()
    if token.type in ['NAME']:
        stream.match('NAME')
        return token.value
    else:
        raise SyntaxError("label: syntax error at {}"
                          .format(token.value))

# var : {NAME} NAME
def var(stream):
    token = stream.pointer()
    if token.type in ['NAME']:
        stream.match('NAME')
        return ('NAME', token.value)
    else:
        raise SyntaxError("var: syntax error at {}"
                          .format(token.value))

# num : {NUMBER} NUMBER
def num(stream):
    token = stream.pointer()
    if token.type in ['NUMBER']:
        stream.match('NUMBER')
        return ('NUMBER', int(token.value))
    else:
        raise SyntaxError("num: syntax error at {}"
                          .format(token.value))

# parser top-level driver
def parse(stream):
    from stackmachine_lexer import Lexer
    token_stream = Lexer(stream)
    instr_list(token_stream) # call the parser function for start symbol
    if not token_stream.end_of_file():
        raise SyntaxError("parse: syntax error at {}"
                          .format(token_stream.pointer().value))
