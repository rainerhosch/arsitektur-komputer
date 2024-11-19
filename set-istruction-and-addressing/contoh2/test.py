# Simulasi memori dan register
memory = [0] * 256  # Memori utama
register = {'ACC': 0, 'PC': 0}  # Akumulator dan Program Counter

# Instruksi berbasis opcode
def execute_instruction(opcode, operand=None):
    if opcode == "LOAD":
        # Memuat nilai dari memori ke ACC
        register['ACC'] = memory[operand]
        print(f"LOAD: ACC <- Memory[{operand}] ({memory[operand]})")
    elif opcode == "STORE":
        # Menyimpan nilai dari ACC ke memori
        memory[operand] = register['ACC']
        print(f"STORE: Memory[{operand}] <- ACC ({register['ACC']})")
    elif opcode == "ADD":
        # Menambahkan nilai dari memori ke ACC
        register['ACC'] += memory[operand]
        print(f"ADD: ACC <- ACC + Memory[{operand}] ({memory[operand]})")
    elif opcode == "SUB":
        # Mengurangi nilai dari memori dengan ACC
        register['ACC'] -= memory[operand]
        print(f"SUB: ACC <- ACC - Memory[{operand}] ({memory[operand]})")
    elif opcode == "MUL":
        # Mengalikan nilai dari memori dengan ACC
        register['ACC'] *= memory[operand]
        print(f"MUL: ACC <- ACC * Memory[{operand}] ({memory[operand]})")
    elif opcode == "DIV":
        # Membagi ACC dengan nilai dari memori
        if memory[operand] != 0:
            register['ACC'] //= memory[operand]
            print(f"DIV: ACC <- ACC // Memory[{operand}] ({memory[operand]})")
        else:
            print("DIV: Error! Division by zero.")
    elif opcode == "AND":
        # Operasi logika AND
        register['ACC'] &= memory[operand]
        print(f"AND: ACC <- ACC & Memory[{operand}] ({memory[operand]})")
    elif opcode == "OR":
        # Operasi logika OR
        register['ACC'] |= memory[operand]
        print(f"OR: ACC <- ACC | Memory[{operand}] ({memory[operand]})")
    elif opcode == "NOT":
        # Operasi logika NOT
        register['ACC'] = ~register['ACC']
        print(f"NOT: ACC <- ~ACC ({register['ACC']})")
    elif opcode == "JUMP":
        # Lompat ke alamat tertentu
        print(f"JUMP: PC <- {operand}")
        return operand
    elif opcode == "JZ":
        # Lompat jika ACC adalah nol
        if register['ACC'] == 0:
            print(f"JZ: PC <- {operand} (ACC == 0)")
            return operand
    elif opcode == "JNZ":
        # Lompat jika ACC bukan nol
        if register['ACC'] != 0:
            print(f"JNZ: PC <- {operand} (ACC != 0)")
            return operand
    elif opcode == "HLT":
        # Hentikan program
        print("HLT: Program dihentikan.")
        return -1
    else:
        print(f"Invalid Opcode: {opcode}")
    return None

# Program: Demonstrasi set instruksi
program = [
    ("LOAD", 10),   # LOAD nilai dari Memory[10] ke ACC
    ("ADD", 11),    # ADD nilai dari Memory[11] ke ACC
    ("STORE", 12),  # STORE nilai ACC ke Memory[12]
    ("SUB", 13),    # Kurangi nilai dari Memory[13]
    ("MUL", 14),    # Kalikan dengan Memory[14]
    ("DIV", 15),    # Bagi dengan Memory[15]
    ("AND", 16),    # Operasi logika AND dengan Memory[16]
    ("OR", 17),     # Operasi logika OR dengan Memory[17]
    ("NOT", None),  # Operasi logika NOT pada ACC
    ("JZ", 20),     # Lompat ke alamat 20 jika ACC == 0
    ("LOAD", 18),   # (tidak dieksekusi jika lompat)
    ("HLT", None),  # Hentikan program
    ("LOAD", 19),   # Eksekusi jika lompat dari JZ
    ("HLT", None),  # Hentikan program
]

# Mengisi memori dengan nilai untuk simulasi
memory[10] = 5
memory[11] = 3
memory[13] = 2
memory[14] = 4
memory[15] = 1
memory[16] = 0b1101
memory[17] = 0b1011
memory[18] = 99
memory[19] = 42

# Eksekusi program
def run_program(program):
    register['PC'] = 0  # Inisialisasi Program Counter
    while register['PC'] < len(program):
        opcode, operand = program[register['PC']]
        next_pc = execute_instruction(opcode, operand)
        if next_pc == -1:
            break
        register['PC'] = next_pc if next_pc is not None else register['PC'] + 1

    print("\nFinal State:")
    print(f"Register: {register}")
    print(f"Memory: {memory[:20]}")  # Menampilkan sebagian memori

run_program(program)
