# Simulasi memori dan CPU
memory = [0] * 256  # Memori dengan 256 lokasi
register = {'ACC': 0}  # Register akumulator (ACC)

# Instruksi berbasis opcode
def execute_instruction(opcode, operand):
    if opcode == "LOAD":
        # LOAD data ke register ACC
        register['ACC'] = memory[operand]
        print(f"LOAD: ACC <- Memory[{operand}] ({memory[operand]})")
    elif opcode == "STORE":
        # STORE nilai ACC ke lokasi memori
        memory[operand] = register['ACC']
        print(f"STORE: Memory[{operand}] <- ACC ({register['ACC']})")
    elif opcode == "ADD":
        # Tambahkan nilai dari memori ke ACC
        register['ACC'] += memory[operand]
        print(f"ADD: ACC <- ACC + Memory[{operand}] ({memory[operand]})")
    elif opcode == "SUB":
        # Kurangi nilai dari memori dengan ACC
        register['ACC'] -= memory[operand]
        print(f"SUB: ACC <- ACC - Memory[{operand}] ({memory[operand]})")
    elif opcode == "JUMP":
        # Lompati instruksi ke alamat tertentu
        return operand
    elif opcode == "HALT":
        # Menghentikan eksekusi
        print("HALT: Program dihentikan.")
        return -1
    else:
        print("Invalid Opcode!")
    return None

# Program sederhana: LOAD, ADD, STORE
program = [
    ("LOAD", 10),  # LOAD nilai dari Memory[10]
    ("ADD", 11),   # ADD nilai dari Memory[11] ke ACC
    ("STORE", 12), # STORE hasil ACC ke Memory[12]
    ("HALT", 0)    # Hentikan program
]

# Memasukkan nilai ke memori untuk eksekusi
memory[10] = 5
memory[11] = 15

# Simulasi eksekusi program
def run_program(program):
    pc = 0  # Program counter
    while pc < len(program):
        opcode, operand = program[pc]
        next_pc = execute_instruction(opcode, operand)
        if next_pc == -1:
            break
        pc = next_pc if next_pc is not None else pc + 1

    print("\nFinal State:")
    print(f"Register: {register}")
    print(f"Memory: {memory[:20]}")  # Menampilkan sebagian memori

run_program(program)
