import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.animation import FuncAnimation

class RISCProcessor:
    def __init__(self, num_registers=8, memory_size=256):
        self.registers = [0] * num_registers  # Inisialisasi register
        self.memory = [0] * memory_size  # Inisialisasi memori
        self.program = []  # Menyimpan program yang akan dieksekusi
        self.instruction_pointer = 0

    def generate_random_program(self, length=20):
        instructions = ["LOAD", "STORE", "ADD", "SUB"]
        for _ in range(length):
            opcode = random.choice(instructions)
            if opcode == "LOAD":
                self.program.append(("LOAD", random.randint(0, 7), random.randint(0, 255)))
            elif opcode == "STORE":
                self.program.append(("STORE", random.randint(0, 7), random.randint(0, 255)))
            elif opcode == "ADD":
                self.program.append(("ADD", random.randint(0, 7), random.randint(0, 7), random.randint(0, 7)))
            elif opcode == "SUB":
                self.program.append(("SUB", random.randint(0, 7), random.randint(0, 7), random.randint(0, 7)))

    def load(self, register, memory_address):
        self.registers[register] = self.memory[memory_address]
        print(f"LOAD: R{register} <- Mem[{memory_address}] ({self.memory[memory_address]})")

    def store(self, register, memory_address):
        self.memory[memory_address] = self.registers[register]
        print(f"STORE: Mem[{memory_address}] <- R{register} ({self.registers[register]})")

    def add(self, dest_register, src_register1, src_register2):
        self.registers[dest_register] = self.registers[src_register1] + self.registers[src_register2]
        print(f"ADD: R{dest_register} <- R{src_register1} + R{src_register2} ({self.registers[dest_register]})")

    def sub(self, dest_register, src_register1, src_register2):
        self.registers[dest_register] = self.registers[src_register1] - self.registers[src_register2]
        print(f"SUB: R{dest_register} <- R{src_register1} - R{src_register2} ({self.registers[dest_register]})")

    def execute_step(self):
        if self.instruction_pointer < len(self.program):
            instruction = self.program[self.instruction_pointer]
            opcode = instruction[0]
            operands = instruction[1:]
            
            if opcode == "LOAD":
                self.load(*operands)
            elif opcode == "STORE":
                self.store(*operands)
            elif opcode == "ADD":
                self.add(*operands)
            elif opcode == "SUB":
                self.sub(*operands)
                
            self.instruction_pointer += 1
        else:
            print("Program selesai.")

# Inisialisasi prosesor
processor = RISCProcessor()
processor.generate_random_program(20)

# Visualisasi Real-Time
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
fig.suptitle("Simulasi Prosesor RISC: Register dan Memori")

register_line, = ax1.plot(processor.registers, 'b-o', label='Registers')
ax1.set_title('Register Values')
ax1.set_ylim(-50, 100)
ax1.set_xlim(0, len(processor.registers) - 1)
ax1.legend()

memory_line, = ax2.plot(processor.memory[:20], 'r-o', label='Memory (First 20)')
ax2.set_title('Memory Values')
ax2.set_ylim(-50, 100)
ax2.set_xlim(0, 19)
ax2.legend()

def update(frame):
    processor.execute_step()
    register_line.set_ydata(processor.registers)
    memory_line.set_ydata(processor.memory[:20])
    return register_line, memory_line

ani = FuncAnimation(fig, update, frames=range(20), interval=1000, repeat=False)
plt.show()
