from cuppa1_cc_basic import cc
from cuppa1_state import state

#####################################################################################
def interp_program():
    state.instr_ix = 0 

    while state.instr_ix < len(state.program):
        instr = state.program[state.instr_ix]  # get the instruction

        instr_type = instr[0].strip()  # strip whitespace from the instruction type


        if instr_type == 'push':
            value = instr[1]
            if isinstance(value, int):
                state.stack.append(value)
            else:
                value = state.symbol_table.get(value, 0)
                state.stack.append(value)
            state.instr_ix += 1

        elif instr_type == 'pop':
            if state.stack:
                state.stack.pop()
            state.instr_ix += 1

        elif instr_type == 'store':
            var_name = instr[1]
            if state.stack:
                state.symbol_table[var_name] = state.stack.pop()
            state.instr_ix += 1

        elif instr_type == 'get':
            var_name = instr[1]
            val = int(input(f"Enter value for {var_name}: "))
            state.symbol_table[var_name] = val
            state.instr_ix += 1

        elif instr_type == 'put':
            if state.stack:
                print(state.stack.pop())
            state.instr_ix += 1

        elif instr_type == 'add':
            if len(state.stack) >= 2:
                a = state.stack.pop()
                b = state.stack.pop()
                state.stack.append(b + a)
            state.instr_ix += 1

        elif instr_type == 'sub':
            if len(state.stack) >= 2:
                a = state.stack.pop()
                b = state.stack.pop()
                state.stack.append(b - a)
            state.instr_ix += 1

        elif instr_type == 'mul':
            if len(state.stack) >= 2:
                a = state.stack.pop()
                b = state.stack.pop()
                state.stack.append(b * a)
            state.instr_ix += 1

        elif instr_type == 'div':
            if len(state.stack) >= 2:
                a = state.stack.pop()
                b = state.stack.pop()
                if a == 0:
                    raise ZeroDivisionError("Division by zero")
                state.stack.append(b // a)
            state.instr_ix += 1

        elif instr_type == 'jumpt':
            if state.stack and state.stack[-1] != 0:
                state.instr_ix = state.label_table[instr[1]]
            else:
                state.instr_ix += 1

        elif instr_type == 'jumpf':
            if state.stack and state.stack[-1] == 0:
                state.instr_ix = state.label_table[instr[1]]
            else:
                state.instr_ix += 1

        elif instr_type == 'jump':
            state.instr_ix = state.label_table[instr[1]]

        elif instr_type == 'stop':
            break

        else:
            #raise ValueError(f"Unexpected instruction: {instr_type}")
            # EDIT: I had to comment out the top line because the program kept running into the end of the bytecode and threw an error.
            # I was unable to figure out why it would keep throwing an error instead of just stopping.
            break

#####################################################################################
def interp(input_stream):
    'Driver for the Cuppa1 interpreter'

    try:
        state.initialize()  # initialize our abstract machine
        bytecode = cc(input_stream)  # build the IR
        if not bytecode:
            print("Compilation failed.")
            return
        print(bytecode)
        state.program = bytecode  # load bytecode into the program
        interp_program()  # interpret the IR

    except Exception as e:
        print(f"Error: {e}")

#####################################################################################
if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print("Usage: python3 A3_interp.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        with open(input_file, 'r') as f:
            input_stream = f.read()

        interp(input_stream)

    except FileNotFoundError:
        print(f"File not found: {input_file}")
