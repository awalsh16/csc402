
from M_interp_fe import parse
from M_interp_state import state

#####################################################################################
def interp_program():

    state.instr_ix = 0 # start at the first instruction
    
    # keep interpreting until we run out of instructions
    # or we hit a 'stop'
    while True:
        if state.instr_ix == len(state.program):
            break  # no more instructions
        else:
            instr = state.program[state.instr_ix] # fetch instr
        type = instr[0]

        # interpret instruction
        if type == 'PRINT':
            if state.stack:
                print(state.stack.pop())
            state.instr_ix += 1
            
        elif type == 'PUSH':   #discerning whether an argument is either a number or variable was pulled from chatgpt
            value = instr[1]
            if isinstance(value, int): #if argument is a number
                state.stack.append(value)

            else: #otherwise, its a variable name
                value = state.symbol_table.get(value, 0)
                state.stack.append(value)
            state.instr_ix += 1

        elif type == 'POP':
            state.stack.pop()
            state.instr_ix += 1
        
        elif type == 'STORE':
            if state.stack:
                state.symbol_table[instr[1]] = state.stack.pop()
            state.instr_ix += 1

        elif type == 'ASK':
            val = int(input("Please enter an int: "))
            state.stack.append(val)
            state.instr_ix += 1

        elif type == 'ADD':
            if len(state.stack) >= 2: #Checking first if we have two numbers to work with
                a = state.stack.pop()
                b = state.stack.pop()
                state.stack.append(b + a)
            state.instr_ix += 1
            
        elif type == 'SUB':
            if len(state.stack) >= 2: #Checking first if we have two numbers to work with
                a = state.stack.pop()
                b = state.stack.pop()
                state.stack.append(b - a)
            state.instr_ix += 1
        
        elif type == 'DUP':
            a = state.stack.pop()
            state.stack.append(a)
            state.stack.append(a)
            state.instr_ix += 1
            
        elif type == 'MUL':
            if len(state.stack) >= 2: #Checking first if we have two numbers to work with
                a = state.stack.pop()
                b = state.stack.pop()
                state.stack.append(b * a)
            state.instr_ix += 1
            
        elif type == 'DIV':
            if len(state.stack) >= 2: #Checking first if we have two numbers to work with
                a = state.stack.pop()
                b = state.stack.pop()
                if a == 0:
                    raise ZeroDivisionError("Division by Zero") #this line of code was taken from chatgpt
                state.stack.append(b // a)
            state.instr_ix += 1
            
        elif type == 'EQU':
            if len(state.stack) >= 2: #Checking first if we have two numbers to work with
                a = state.stack.pop()
                b = state.stack.pop()
                if a == b:
                    state.stack.append(1)
                else:
                    state.stack.append(0)
            state.instr_ix += 1
        
        elif type == 'LEQ':
            if len(state.stack) >= 2: #Checking first if we have two numbers to work with
                a = state.stack.pop()
                b = state.stack.pop()
                if a <= b:
                    state.stack.append(1)
                else:
                    state.stack.append(0)
            state.instr_ix += 1
        
        elif type == 'JUMPT':
            if state.stack.pop() != 0:
                state.instr_ix = state.label_table[instr[1]]
            else:
                state.instr_ix += 1

        elif type == 'JUMPF':
            if state.stack.pop() == 0:
                state.instr_ix = state.label_table[instr[1]]
            else:
                state.instr_ix += 1

        elif type == 'JUMP':
            state.instr_ix = state.label_table[instr[1]]

        elif type == 'STOP':
            break

        elif type == 'NOOP':
            state.instr_ix += 1

        else:
            raise ValueError("Unexpected instruction: {}"
                             .format(type))



#####################################################################################
def interp(input_stream):
    'driver for our Exp1bytecode interpreter.'

    try:
        state.initialize()  # initialize our abstract machine
        parse(input_stream) # build the IR
        interp_program()    # interpret the IR
    except Exception as e:
        print("error: "+str(e))

#####################################################################################
if __name__ == '__main__':
    import sys
    import os

    if len(sys.argv) == 1: # no args - read stdin
        char_stream = sys.stdin.read()
    else: # last arg is filename to open and read
        input_file = sys.argv[-1]
        if not os.path.isfile(input_file):
            print("unknown file {}".format(input_file))
            sys.exit(0)
        else:
            f = open(input_file, 'r')
            char_stream = f.read()
            f.close()

    interp(char_stream)
    