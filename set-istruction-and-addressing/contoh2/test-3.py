import os
import time

# Memori dan register
memory = [0] * 256  # Memori utama
register = {'ACC': 0, 'PC': 0, 'R1': 0, 'R2': 0}  # Tambahan register R1 dan R2
pipeline = {'FETCH': None, 'DECODE': None, 'EXECUTE': None}  # Pipeline sederhana

# Fungsi untuk membersihkan layar
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Fungsi untuk menampilkan visualisasi
def visualize():
    clear_screen()
    print(f"{'='*50}")
    print(f"{'PROGRAM STATUS':^40}")
    print(f"{'='*50}")
    print("\nPipeline Status:")
    for stage, value in pipeline.items():
        print(f"{stage:10}: {value}")
    
    print("\nRegister Status:")
    for reg, value in register.items():
        print(f"{reg:10}: {value}")
    
    print("\nMemory (first 20 locations):")
    for i in range(0, 20, 5):
        print(" ".join(f"[{j:02d}]:{memory[j]:03}" for j in range(i, i+5)))

    print(f"{'='*50}\n")
    time.sleep(0.5)  # Menunggu sebentar agar perubahan terlihat

# Eksekusi instruksi
def execute_instruction(opcode, operand=None, addressing_mode="absolute"):
    effective_address = operand
    if addressing_mode == "relative":
        effective_address = register['PC'] + operand

    if opcode == "LOAD":
        register['ACC'] = memory[effective_address]
    elif opcode == "STORE":
        memory[effective_address] = register['ACC']
    elif opcode == "ADD":
        register['ACC'] += memory[effective_address]
    elif opcode == "SUB":
        register['ACC'] -= memory[effective_address]
    elif opcode == "MUL":
        register['ACC'] *= memory[effective_address]
    elif opcode == "DIV":
        if memory[effective_address] != 0:
            register['ACC'] //= memory[effective_address]
    elif opcode == "MOV":
        if operand == 'R1':
            register['R1'] = register['ACC']
        elif operand == 'R2':
            register['R2'] = register['ACC']
        elif operand == 'ACC':
            register['ACC'] = register['R1']
    elif opcode == "JUMP":
        return effective_address
    elif opcode == "JZ":
        if register['ACC'] == 0:
            return effective_address
    elif opcode == "JNZ":
        if register['ACC'] != 0:
            return effective_address
    elif opcode == "HLT":
        return -1
    return None

# Pipeline
def pipeline_execution(program):
    while True:
        # Visualisasi awal siklus
        visualize()

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
                visualize()
                print("Program Selesai.")
                break
            elif next_pc is not None:
                register['PC'] = next_pc

        # Visualisasi setelah eksekusi
        visualize()

# Program
program = [
    ("LOAD", 10),                   # LOAD nilai dari Memory[10]
    ("ADD", 11),                    # ADD nilai dari Memory[11]
    ("MOV", 'R1'),                  # MOV nilai ACC ke R1
    ("LOAD", 12, "relative"),       # LOAD nilai dari alamat relatif
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
