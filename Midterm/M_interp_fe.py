
from M_interp_state import state

# lookahead sets for parser
instr_lookahead = ['PRINT', 'PUSH','POP', 'STORE','ASK','DUP','ADD','SUB','MUL','DIV','EQU','LEQ','JUMPT','JUMPF','JUMP','STOP','NOOP']
labeled_instr_lookahead = instr_lookahead + ['LABEL']

#instr_list : {label, print, pop, store, ask, dup, add, sub, mul, div, equ, leq, jumpt, jumpf, jump, stop, noop}(labeled_instr)*
def instr_list(stream):
  while stream.pointer().type in labeled_instr_lookahead:
    labeled_instr(stream)
  return None

#labeled_instr : {label} label_def instr
#    |   {print, pop, store var, ask, dup, add, sub, mul, div, equ, leq, jumpt label, jumpf label, jump label, stop, noop} instr
def labeled_instr(stream):
    token = stream.pointer()
    if token.type in ['LABEL']:
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

# label_def : {LABEL} label COLON
def label_def(stream):
    token = stream.pointer()
    if token.type in ['LABEL']:
        l = label(stream)
        stream.match('COLON')
        return l
    else:
        raise SyntaxError("label_def: syntax error at {}"
                          .format(token.value))

#instr : print ;        all the lookaheads would just be itself, no need to write it
#    | push arg ;
#    | pop ;
#    | store var ;
#    | ask ;
#    | dup ;
#    | add ;
#    | sub ;
#    | mul ;
#    | div ;
#    | equ ;
#    | leq ;
#    | jumpt label ;
#    | jumpf label ;
#    | jump label ;
#    | stop ;
#    | noop ;
def instr(stream):
    token = stream.pointer()
    if token.type in ['PRINT']:
        stream.match('PRINT')
        stream.match('SEMI')
        return ('PRINT',)
    
    elif token.type in ['PUSH']:
        stream.match('PUSH')
        value = arg(stream)
        stream.match('SEMI')
        return ('PUSH', value)
    
    elif token.type in ['POP']:
        stream.match('POP')
        stream.match('SEMI')
        return('POP',)
        
    elif token.type in ['STORE']:
        stream.match('STORE')
        value = var(stream)
        stream.match('SEMI')
        return('STORE', value)
    
    elif token.type in ['ASK']:
        stream.match('ASK')
        stream.match('SEMI')
        return('ASK',)
    
    elif token.type in ['DUP']:
        stream.match('DUP')
        stream.match('SEMI')
        return('DUP',)
    
    elif token.type in ['ADD']:
        stream.match('ADD')
        stream.match('SEMI')
        return('ADD',)
    
    elif token.type in ['SUB']:
        stream.match('SUB')
        stream.match('SEMI')
        return('SUB',)
    
    elif token.type in ['MUL']:
        stream.match('MUL')
        stream.match('SEMI')
        return('MUL',)
    
    elif token.type in ['DIV']:
        stream.match('DIV')
        stream.match('SEMI')
        return('DIV',)
    
    elif token.type in ['EQU']:
        stream.match('EQU')
        stream.match('SEMI')
        return('EQU',)
    
    elif token.type in ['LEQ']:
        stream.match('LEQ')
        stream.match('SEMI')
        return('LEQ',)
    
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
        stream.match('SEMI')
        return ('STOP',)
    
    elif token.type in ['NOOP']:
        stream.match('NOOP')
        stream.match('SEMI')
        return ('NOOP',)
    else:
        print("this")
        raise SyntaxError("instr: syntax error at {}"
                          .format(token.value))

#arg : {num} num
#    | {var} var
def arg(stream):
    token = stream.pointer()
    if token.type in ['NUM']:
        stream.match('NUM')
        return (int(token.value))
    if token.type in ['VAR']:
        stream.match('VAR')
        return (token.value)

def label(stream):
    token = stream.pointer()
    if token.type in ['LABEL']:
        label_name = token.value
        stream.match('LABEL')
        return label_name
    else:
        raise SyntaxError("label: syntax error at {}"
                          .format(token.value))

# var : {VAR} VAR
def var(stream):
    token = stream.pointer()
    if token.type in ['VAR']:
        stream.match('VAR')
        return token.value
    else:
        
        raise SyntaxError("var: syntax error at {}"
                          .format(token.value))

# num : {NUMBER} NUMBER
def num(stream):
    token = stream.pointer()
    if token.type in ['NUM']:
        stream.match('NUM')
        return token.value
    else:
        
        raise SyntaxError("num: syntax error at {}"
                          .format(token.value))

# parser top-level driver
def parse(stream):
    from M_lexer import Lexer

    token_stream = Lexer(stream)

    instr_list(token_stream) # call the parser function for start symbol
    if not token_stream.end_of_file():
        raise SyntaxError("parse: syntax error at {}"
                          .format(token_stream.pointer().value))
