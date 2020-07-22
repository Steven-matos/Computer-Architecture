"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = True
        self.ir = {
            0b00000001: 'HTL',
            0b10000010: 'LDI',
            0b01000111: 'PRN',
            0b10100010: 'MUL'
        }

    def load(self, file_name):
        """Load a program into memory."""

        address = 0
        program = []
        with open(file_name) as file:
            i = 0
            for address, line in enumerate(file):
                line = line.split('#')

                try:
                    v = int(line[0], 2)
                except ValueError:
                    continue

                self.ram[i] = v

                i = i + 1
        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == 'ADD':
            self.reg[reg_a] += self.reg[reg_b]
            self.pc += value
        elif op == 'MUL':
            print(self.reg[reg_a] * self.reg[reg_b])
            self.pc = self.pc + 2
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, counter):
        return self.ram[counter]

    def ram_write(self, counter, value):
        self.reg[counter] = value

    def run(self):
        """Run the CPU."""
        while self.running:
            op = self.ir[self.ram_read(self.pc)]
            reg_a = self.ram_read(
                self.pc+1)
            reg_b = self.ram_read(self.pc+2)

            if op == 'LDI':
                self.ram_write(reg_a, reg_b)
                self.pc = self.pc + 3
            elif op == 'HTL':
                self.running = False
                sys.exit(1)
            elif op == 'PRN':
                print(self.reg[reg_a])
                self.pc = self.pc + 2
            else:
                self.alu(op, reg_a, reg_b)
