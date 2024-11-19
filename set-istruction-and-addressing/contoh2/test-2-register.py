# Memori dan register
memory = [0] * 256  # Memori utama
register = {'ACC': 0, 'PC': 0, 'R1': 0, 'R2': 0}  # Tambahan register R1 dan R2

# Pipeline sederhana (Fetch, Decode, Execute)
pipeline = {'FETCH': None, 'DECODE': None, 'EXECUTE': None}

# Debugger untuk melacak langkah eksekusi
debug_mode = True  # Aktifkan debugger


def debugger():
    """Fungsi untuk melacak status pipeline, register, dan memori."""
    if debug_mode:
        print("\n--- DEBUG INFO ---")
        print(f"Pipeline: {pipeline}")
        print(f"Registers: {register}")
        print(f"Memory (first 20): {memory[:20]}")
        print("-------------------\n")


# Eksekusi instruksi
def execute_instruction(opcode, operand=None, addressing_mode="absolute"):
    effective_address = operand
    if addressing_mode == "relative":
        effective_address = register['PC'] + operand
        print(f"Using relative addressing: Effective Address = {effective_address}")

    if opcode == "LOAD":
        register['ACC'] = memory[effective_address]
        print(f"LOAD: ACC <- Memory[{effective_address}] ({memory[effective_address]})")
    elif opcode == "STORE":
        memory[effective_address] = register['ACC']
        print(f"STORE: Memory[{effective_address}] <- ACC ({register['ACC']})")
    elif opcode == "ADD":
        register['ACC'] += memory[effective_address]
        print(f"ADD: ACC <- ACC + Memory[{effective_address}] ({memory[effective_address]})")
    elif opcode == "SUB":
        register['ACC'] -= memory[effective_address]
        print(f"SUB: ACC <- ACC - Memory[{effective_address}] ({memory[effective_address]})")
    elif opcode == "MUL":
        register['ACC'] *= memory[effective_address]
        print(f"MUL: ACC <- ACC * Memory[{effective_address}] ({memory[effective_address]})")
    elif opcode == "DIV":
        if memory[effective_address] != 0:
            register['ACC'] //= memory[effective_address]
            print(f"DIV: ACC <- ACC // Memory[{effective_address}] ({memory[effective_address]})")
        else:
            print("DIV: Error! Division by zero.")
    elif opcode == "MOV":
        # Memindahkan nilai antar register
        if operand == 'R1':
            register['R1'] = register['ACC']
            print(f"MOV: R1 <- ACC ({register['ACC']})")
        elif operand == 'R2':
            register['R2'] = register['ACC']
            print(f"MOV: R2 <- ACC ({register['ACC']})")
        elif operand == 'ACC':
            register['ACC'] = register['R1']
            print(f"MOV: ACC <- R1 ({register['R1']})")
    elif opcode == "JUMP":
        print(f"JUMP: PC <- {effective_address}")
        return effective_address
    elif opcode == "JZ":
        if register['ACC'] == 0:
            print(f"JZ: PC <- {effective_address} (ACC == 0)")
            return effective_address
    elif opcode == "JNZ":
        if register['ACC'] != 0:
            print(f"JNZ: PC <- {effective_address} (ACC != 0)")
            return effective_address
    elif opcode == "HLT":
        print("HLT: Program dihentikan.")
        return -1
    else:
        print(f"Invalid Opcode: {opcode}")
    return None


# Pipeline
def pipeline_execution(program):
    while True:
        # Tahap Fetch
        if pipeline['FETCH'] is None and register['PC'] < len(program):
            pipeline['FETCH'] = program[register['PC']]
            register['PC'] += 1

        # Tahap Decode
        if pipeline['FETCH'] and pipeline['DECODE'] is None:
            # opcode, operand, addressing_mode = (*pipeline['FETCH'], "absolute")
            fetch_data = pipeline['FETCH']
            opcode = fetch_data[0]
            operand = fetch_data[1]
            addressing_mode = fetch_data[2] if len(fetch_data) == 3 else "absolute"
            if len(pipeline['FETCH']) == 3:
                addressing_mode = pipeline['FETCH'][2]
            pipeline['DECODE'] = (opcode, operand, addressing_mode)
            pipeline['FETCH'] = None

        # Tahap Execute
        if pipeline['DECODE']:
            opcode, operand, addressing_mode = pipeline['DECODE']
            next_pc = execute_instruction(opcode, operand, addressing_mode)
            pipeline['DECODE'] = None

            # Jika program selesai
            if next_pc == -1:
                break
            elif next_pc is not None:
                register['PC'] = next_pc

        # Debugger untuk melacak langkah
        debugger()


# Program
program = [
    ("LOAD", 10),                   # LOAD nilai dari Memory[10]
    ("ADD", 11),                    # ADD nilai dari Memory[11]
    ("MOV", 'R1'),                  # MOV nilai ACC ke R1
    ("LOAD", 12, "relative"),       # LOAD nilai dari alamat relatif (PC + offset)
    ("STORE", 20),                  # STORE nilai ACC ke Memory[20]
    ("MOV", 'R2'),                  # MOV nilai ACC ke R2
    ("SUB", 13),                    # SUB nilai dari Memory[13]
    ("JZ", 30),                     # Lompat ke alamat 30 jika ACC == 0
    ("LOAD", 14),                   # LOAD nilai lain (tidak dieksekusi jika lompat)
    ("HLT", None),                  # Hentikan program
    ("LOAD", 15, "relative"),       # Program berlanjut dari sini jika lompat
    ("HLT", None),
]

# Mengisi memori dengan nilai
memory[10] = 5
memory[11] = 3
memory[12] = 2  # Alamat relatif
memory[13] = 8
memory[14] = 99
memory[15] = 42

# Jalankan program
pipeline_execution(program)
