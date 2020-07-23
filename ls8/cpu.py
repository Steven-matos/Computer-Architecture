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
        self.sp = 7
        self.reg[self.sp] = 0xF4
        self.flag = 0b00000000
        self.ir = {
            0b00000001: 'HTL',
            0b10000010: 'LDI',
            0b01000111: 'PRN',
            0b10100010: 'MUL',
            0b10100000: 'ADD',
            0b01000101: 'PUSH',
            0b01000110: 'POP',
            0b01010000: 'CALL',
            0b00010001: 'RET',
        }

    def load(self, file_name):
        """Load a program into memory."""

        with open(file_name) as file:
            idx = 0
            for address, line in enumerate(file):
                line = line.split('#')

                try:
                    value = int(line[0], 2)
                except ValueError:
                    continue

                self.ram[idx] = value

                idx = idx + 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        value = op >> 6
        value = value + 0b00000001

        op = self.ir[op]

        if op == 'ADD':
            self.reg[reg_a] += self.reg[reg_b]
            self.pc += value
        elif op == 'MUL':
            print(self.reg[reg_a] * self.reg[reg_b])
            self.pc = self.pc + 2
        elif op == 'CALL':
            return_address = self.pc + value
            self.reg[self.sp] -= 1

            memory_address = self.reg[self.sp]

            self.ram[memory_address] = return_address

            sub_routin_address = self.reg[reg_a]

            self.pc = sub_routin_address
        elif op == 'RET':
            stack_address = self.reg[self.sp]

            reg_value = self.ram[stack_address]

            self.reg[self.sp] = self.reg[self.sp] + 1
            self.pc = reg_value
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

            elif op == 'PRN':
                print(self.reg[reg_a])
                self.pc = self.pc + 2
            elif op == 'PUSH':
                self.reg[self.sp] -= 1

                reg_value = self.reg[reg_a]

                stack_address = self.reg[self.sp]
                self.ram[stack_address] = reg_value
                self.pc = self.pc + 2
            elif op == 'POP':
                stack_address = self.reg[self.sp]

                reg_value = self.ram_read(stack_address)
                self.reg[self.sp] = self.reg[self.sp] + 1

                self.reg[reg_a] = reg_value

                self.pc = self.pc + 2
            elif op == 'HTL':
                self.running = False
                sys.exit(1)
            else:
                self.alu(self.ram_read(self.pc), reg_a, reg_b)
