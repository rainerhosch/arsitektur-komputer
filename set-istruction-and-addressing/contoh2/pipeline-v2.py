import os
import time

# Memori, register, dan tumpukan
memory = [0] * 256  # Memori utama
register = {'ACC': 0, 'PC': 0, 'R1': 0, 'R2': 0, 'SP': 255}  # SP: Stack Pointer
pipeline = {'FETCH': None, 'DECODE': None, 'EXECUTE': None}  # Pipeline sederhana
memory_changes = {}  # Catatan perubahan memori

# Peta opcode dan mode pengalamatan
opcode_map = {"LOAD": "0001", "STORE": "0010", "ADD": "0011", "SUB": "0100", 
              "MUL": "0101", "DIV": "0110", "PUSH": "0111", "POP": "1000", 
              "JUMP": "1001", "JZ": "1010", "JNZ": "1011", "HLT": "1111"}
addressing_mode_map = {"immediate": "0001", "direct": "0010", "indirect": "0011", 
                       "register": "0100", "register_indirect": "0101", 
                       "displacement": "0110", "stack": "0111"}

# Fungsi untuk membersihkan layar
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Fungsi untuk menampilkan visualisasi
def visualize(binary_instruction=None, decode_details=None):
    clear_screen()
    print(f"{'='*90}")
    print(f"{'PROGRAM STATUS':^90}")
    print(f"{'='*90}")
    print("\nPipeline Status:")
    for stage, value in pipeline.items():
        print(f"{stage:10}: {value}")
    
    print("\nRegister Status:")
    for reg, value in register.items():
        print(f"{reg:10}: {value}")
    
    print("\nMemory (first 50 locations):")
    for i in range(0, 50, 10):
        print(" ".join(f"[{j:02d}]:\033[92m{memory[j]:03}\033[0m" if j in memory_changes else f"[{j:02d}]:{memory[j]:03}" for j in range(i, i+10)))

    print("\nMemory Changes:")
    if memory_changes:
        for addr, value in memory_changes.items():
            print(f"Memory[{addr:02d}] -> {value:03}")
    
    if binary_instruction:
        print("\nInstruction in Binary:")
        print(f"{binary_instruction}\n")
    
    if decode_details:
        print("\nDecode Details:")
        for key, value in decode_details.items():
            print(f"{key:15}: {value}")
    
    print(f"{'='*90}\n")
    time.sleep(0.5)

# Fungsi untuk mengonversi instruksi menjadi biner
def encode_instruction(opcode, operand=None, addressing_mode="immediate"):
    opcode_binary = opcode_map[opcode]
    addressing_binary = addressing_mode_map[addressing_mode]
    operand_binary = format(operand if operand is not None else 0, "08b")
    return f"{opcode_binary} {addressing_binary} {operand_binary}"

# Eksekusi instruksi dengan berbagai mode pengalamatan
def execute_instruction(opcode, operand=None, addressing_mode="immediate"):
    global memory_changes
    effective_address = None
    value = None

    if addressing_mode == "immediate":
        value = operand
    elif addressing_mode == "direct":
        effective_address = operand
        value = memory[effective_address]
    elif addressing_mode == "indirect":
        effective_address = memory[operand]
        value = memory[effective_address]
    elif addressing_mode == "register":
        value = register.get(operand, 0)
    elif addressing_mode == "register_indirect":
        effective_address = register[operand]
        value = memory[effective_address]
    elif addressing_mode == "displacement":
        base, offset = operand
        effective_address = register[base] + offset
        value = memory[effective_address]
    elif addressing_mode == "stack":
        if opcode == "PUSH":
            register['SP'] -= 1
            memory[register['SP']] = register['ACC']
            memory_changes[register['SP']] = register['ACC']
            return None
        elif opcode == "POP":
            value = memory[register['SP']]
            register['SP'] += 1
            return value

    if opcode == "LOAD":
        register['ACC'] = value
    elif opcode == "STORE":
        memory[effective_address] = register['ACC']
        memory_changes[effective_address] = register['ACC']
    elif opcode == "ADD":
        register['ACC'] += value
    elif opcode == "SUB":
        register['ACC'] -= value
    elif opcode == "MUL":
        register['ACC'] *= value
    elif opcode == "DIV":
        if value != 0:
            register['ACC'] //= value
    elif opcode == "MOV":
        if addressing_mode == "register":
            register[operand] = register['ACC']
    elif opcode == "JUMP":
        return operand
    elif opcode == "JZ":
        if register['ACC'] == 0:
            return operand
    elif opcode == "JNZ":
        if register['ACC'] != 0:
            return operand
    elif opcode == "HLT":
        return -1
    return None

# Pipeline
def pipeline_execution(program):
    global pipeline, memory_changes
    while True:
        # Visualisasi awal siklus
        visualize()
        memory_changes = {}  # Reset perubahan memori untuk siklus ini

        # Tahap EXECUTE
        if pipeline['EXECUTE']:
            opcode, operand, addressing_mode = pipeline['EXECUTE']
            binary_instruction = encode_instruction(opcode, operand, addressing_mode)
            decode_details = {
                "Opcode": opcode,
                "Operand": operand,
                "Addressing Mode": addressing_mode,
                "Binary": binary_instruction,
            }
            next_pc = execute_instruction(opcode, operand, addressing_mode)
            visualize(binary_instruction, decode_details)
            pipeline['EXECUTE'] = None  # Tahap ini selesai

            # Jika program selesai
            if next_pc == -1:
                visualize()
                print("Program Selesai.")
                break
            elif next_pc is not None:
                register['PC'] = next_pc

        # Tahap DECODE -> EXECUTE
        if pipeline['DECODE']:
            pipeline['EXECUTE'] = pipeline['DECODE']
            pipeline['DECODE'] = None

        # Tahap FETCH -> DECODE
        if pipeline['FETCH']:
            # opcode, operand, addressing_mode = (*pipeline['FETCH'], "immediate")
            fetch_data = pipeline['FETCH']
            opcode = fetch_data[0]
            operand = fetch_data[1]
            addressing_mode = fetch_data[2] if len(fetch_data) == 3 else "immediate"
            if len(pipeline['FETCH']) == 3:
                addressing_mode = pipeline['FETCH'][2]
            pipeline['DECODE'] = (opcode, operand, addressing_mode)
            pipeline['FETCH'] = None

        # Tahap FETCH baru
        if pipeline['FETCH'] is None and register['PC'] < len(program):
            pipeline['FETCH'] = program[register['PC']]
            register['PC'] += 1

# Program dengan berbagai mode pengalamatan
program = [
    ("LOAD", 10, "direct"),           # LOAD nilai dari Memory[10]
    ("ADD", 11, "direct"),            # ADD nilai dari Memory[11]
    ("STORE", 20, "direct"),          # STORE nilai ACC ke Memory[20]
    ("PUSH", None, "stack"),          # PUSH ACC ke stack
    ("LOAD", 2, "immediate"),         # LOAD nilai langsung
    # ("ADD", 'R1', "register"),        # ADD nilai dari R1
    ("POP", None, "stack"),           # POP nilai dari stack ke ACC
    ("STORE", 21, "direct"),          # STORE nilai ACC ke Memory[21]
    ("LOAD", 5, "indirect"),          # LOAD nilai dari alamat tidak langsung
    ("JZ", 15, "immediate"),          # Lompat ke alamat 15 jika ACC == 0
    ("HLT", None),                    # Hentikan program
]

# Mengisi memori dan register dengan nilai awal
memory[10] = 5
memory[11] = 3
memory[12] = 8
memory[20] = 0
memory[21] = 0
memory[5] = 15  # Alamat untuk pengalamatan tidak langsung
# register['R1'] = 4

# Jalankan program
pipeline_execution(program)
