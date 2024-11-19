import time

def fetch_instruction():
    """
    Menerima input dari keyboard sebagai simulasi instruksi yang diterima prosesor.
    """
    instruction = input("Masukkan instruksi (misalnya, 'ADD 5 10' atau 'MUL 4 2'): ")
    return instruction

def decode_instruction(instruction):
    """
    Mendekode instruksi ke dalam bentuk operasi dan operand.
    """
    parts = instruction.split()
    if len(parts) < 3:
        raise ValueError("Instruksi tidak valid. Format: OPERASI OPERAND1 OPERAND2")
    operation, operand1, operand2 = parts[0], int(parts[1]), int(parts[2])
    return operation.upper(), operand1, operand2

def execute_instruction(operation, operand1, operand2):
    """
    Mengeksekusi instruksi berdasarkan operasi dan operand yang diberikan.
    """
    if operation == "ADD":
        return operand1 + operand2
    elif operation == "SUB":
        return operand1 - operand2
    elif operation == "MUL":
        return operand1 * operand2
    elif operation == "DIV":
        if operand2 == 0:
            raise ZeroDivisionError("Tidak bisa membagi dengan nol!")
        return operand1 / operand2
    else:
        raise ValueError(f"Operasi tidak dikenali: {operation}")

def simulate_processor():
    """
    Simulasi kerja prosesor dari menerima input hingga eksekusi.
    """
    print("Simulasi kerja prosesor dimulai...\n")
    time.sleep(1)
    print("Fetching instruction...")
    time.sleep(1)
    
    try:
        instruction = fetch_instruction()
        print(f"Instruksi diterima: {instruction}")
        time.sleep(1)
        
        print("Decoding instruction...")
        operation, operand1, operand2 = decode_instruction(instruction)
        print(f"Operasi: {operation}, Operand1: {operand1}, Operand2: {operand2}")
        time.sleep(1)
        
        print("Executing instruction...")
        result = execute_instruction(operation, operand1, operand2)
        print(f"Hasil eksekusi: {result}")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    while True:
        simulate_processor()
        continue_simulation = input("\nApakah ingin melanjutkan simulasi? (y/n): ").lower()
        if continue_simulation != 'y':
            print("Simulasi dihentikan.")
            break
