import matplotlib.pyplot as plt
import numpy as np

class RISCProcessor:
    def __init__(self, num_registers=8, memory_size=256):
        self.registers = [0] * num_registers  # Inisialisasi register
        self.memory = [0] * memory_size  # Inisialisasi memori
        self.instruction_pointer = 0  # Penunjuk instruksi
        self.history = []  # Untuk menyimpan history perubahan

    def record_state(self):
        # Simpan state memori dan register untuk visualisasi
        self.history.append({
            "memory": self.memory[:],
            "registers": self.registers[:]
        })

    def load(self, register, memory_address):
        self.registers[register] = self.memory[memory_address]
        self.record_state()
        print(f"LOAD: R{register} <- Mem[{memory_address}] ({self.memory[memory_address]})")

    def store(self, register, memory_address):
        self.memory[memory_address] = self.registers[register]
        self.record_state()
        print(f"STORE: Mem[{memory_address}] <- R{register} ({self.registers[register]})")

    def add(self, dest_register, src_register1, src_register2):
        self.registers[dest_register] = self.registers[src_register1] + self.registers[src_register2]
        self.record_state()
        print(f"ADD: R{dest_register} <- R{src_register1} + R{src_register2} ({self.registers[dest_register]})")

    def sub(self, dest_register, src_register1, src_register2):
        self.registers[dest_register] = self.registers[src_register1] - self.registers[src_register2]
        self.record_state()
        print(f"SUB: R{dest_register} <- R{src_register1} - R{src_register2} ({self.registers[dest_register]})")

    def run(self, program):
        while self.instruction_pointer < len(program):
            instruction = program[self.instruction_pointer]
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
            else:
                print(f"Unknown instruction: {opcode}")
            
            self.instruction_pointer += 1

    def visualize(self):
        # Membuat visualisasi register dan memori
        fig, axes = plt.subplots(2, 1, figsize=(12, 8))
        fig.suptitle("Visualisasi Perubahan Register dan Memori", fontsize=16)

        # Visualisasi register
        for step, state in enumerate(self.history):
            axes[0].plot(state["registers"], label=f"Step {step}")
        axes[0].set_title("Register")
        axes[0].set_xlabel("Register Index")
        axes[0].set_ylabel("Value")
        axes[0].legend()

        # Visualisasi memori (hanya 20 memori pertama untuk kesederhanaan)
        for step, state in enumerate(self.history):
            axes[1].plot(state["memory"][:20], label=f"Step {step}")
        axes[1].set_title("Memori (20 slot pertama)")
        axes[1].set_xlabel("Memory Address")
        axes[1].set_ylabel("Value")
        axes[1].legend()

        plt.tight_layout()
        plt.show()

# Program contoh
program = [
    ("LOAD", 0, 10),  # LOAD R0 dari Mem[10]
    ("LOAD", 1, 11),  # LOAD R1 dari Mem[11]
    ("ADD", 2, 0, 1), # ADD R2 = R0 + R1
    ("STORE", 2, 12), # STORE R2 ke Mem[12]
    ("SUB", 3, 2, 0)  # SUB R3 = R2 - R0
]

# Inisialisasi prosesor dan memori
processor = RISCProcessor()
processor.memory[10] = 5
processor.memory[11] = 7

print("Sebelum eksekusi:")
print("Memori:", processor.memory[:15])
print("Register:", processor.registers)

# Jalankan program
processor.run(program)

print("\nSetelah eksekusi:")
print("Memori:", processor.memory[:15])
print("Register:", processor.registers)

# Visualisasi
processor.visualize()
