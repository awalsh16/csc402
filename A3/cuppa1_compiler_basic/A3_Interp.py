class Interpreter:
    def __init__(self, instr_stream):
        self.instr_stream = instr_stream  # Bytecode instructions
        self.stack = []                   # Stack for calculations
        self.symbol_table = {}            # Variable storage
        self.instr_ix = 0                 # Instruction pointer
        self.label_table = self.build_label_table()  # Map labels to instruction indices

    def build_label_table(self):
        label_table = {}
        for ix, instr in enumerate(self.instr_stream):
            if instr[0].endswith(':'):  # Check if it's a label
                label_name = instr[0][:-1]  # Strip the colon
                label_table[label_name] = ix
        return label_table

    def run(self):
        while self.instr_ix < len(self.instr_stream):
            instr = self.instr_stream[self.instr_ix]
            self.execute(instr)
            if instr[0] != 'stop':
                self.instr_ix += 1

    def execute(self, instr):
        instr_type = instr[0]

        if instr_type == 'push':
            value = int(instr[1]) if instr[1].isdigit() else self.symbol_table.get(instr[1], 0)
            self.stack.append(value)

        elif instr_type == 'pop':
            if self.stack:
                self.stack.pop()

        elif instr_type == 'store':
            var_name = instr[1]
            if self.stack:
                self.symbol_table[var_name] = self.stack.pop()

        elif instr_type == 'get':
            var_name = instr[1]
            value = int(input(f"Enter value for {var_name}: "))
            self.symbol_table[var_name] = value

        elif instr_type == 'put':
            if self.stack:
                print(self.stack.pop())

        elif instr_type == 'add':
            if len(self.stack) >= 2:
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.append(b + a)

        elif instr_type == 'sub':
            if len(self.stack) >= 2:
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.append(b - a)

        elif instr_type == 'mul':
            if len(self.stack) >= 2:
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.append(b * a)

        elif instr_type == 'div':
            if len(self.stack) >= 2:
                a = self.stack.pop()
                b = self.stack.pop()
                if a == 0:
                    raise ZeroDivisionError("Division by zero")
                self.stack.append(b // a)

        elif instr_type == 'jumpt':
            if self.stack and self.stack[-1] != 0:
                self.instr_ix = self.label_table[instr[2]]

        elif instr_type == 'jumpf':
            if self.stack and self.stack[-1] == 0:
                self.instr_ix = self.label_table[instr[2]]

        elif instr_type == 'jump':
            self.instr_ix = self.label_table[instr[1]]

        elif instr_type == 'stop':
            exit()

        else:
            raise ValueError(f"Unexpected instruction: {instr_type}")
