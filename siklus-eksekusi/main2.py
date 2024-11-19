import time
from rich.console import Console
from rich.progress import track
from rich.table import Table

console = Console()

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

def convert_to_binary(number):
    """
    Mengonversi angka ke dalam format biner 8-bit.
    """
    return format(number, '08b')

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

def visualize_instruction(process_name, process_details):
    """
    Menampilkan visualisasi dari proses tertentu.
    """
    console.print(f"[bold cyan]{process_name}[/bold cyan]")
    console.print(process_details)
    time.sleep(1)

def simulate_processor():
    """
    Simulasi kerja prosesor dari menerima input hingga eksekusi, termasuk konversi biner dan visualisasi.
    """
    console.print("\n[bold green]Simulasi kerja prosesor dimulai...[/bold green]\n", style="bold")
    time.sleep(1)
    
    # Fetching Instruction
    instruction = fetch_instruction()
    visualize_instruction("Fetching Instruction", f"Instruksi diterima: [yellow]{instruction}[/yellow]")

    # Decoding Instruction
    try:
        visualize_instruction("Decoding Instruction", "[blue]Memproses instruksi...[/blue]")
        operation, operand1, operand2 = decode_instruction(instruction)
        visualize_instruction("Decoded Instruction", f"Operasi: {operation}, Operand1: {operand1}, Operand2: {operand2}")

        # Converting to Binary
        visualize_instruction("Converting to Binary", "[magenta]Mengonversi ke bentuk biner...[/magenta]")
        binary_operand1 = convert_to_binary(operand1)
        binary_operand2 = convert_to_binary(operand2)
        visualize_instruction("Binary Conversion", f"Operand1: {operand1} -> {binary_operand1}\nOperand2: {operand2} -> {binary_operand2}")

        # Executing Instruction
        visualize_instruction("Executing Instruction", "[bold yellow]Mengeksekusi operasi...[/bold yellow]")
        result = execute_instruction(operation, operand1, operand2)
        binary_result = convert_to_binary(int(result)) if isinstance(result, int) else "N/A"
        visualize_instruction("Execution Result", f"Hasil: {result} ({binary_result} dalam biner)")

        # Finalizing
        table = Table(title="Proses Eksekusi")
        table.add_column("Tahapan", style="cyan", justify="left")
        table.add_column("Detail", style="green", justify="left")
        table.add_row("Instruksi", instruction)
        table.add_row("Operasi", operation)
        table.add_row("Operand1 (Biner)", f"{operand1} ({binary_operand1})")
        table.add_row("Operand2 (Biner)", f"{operand2} ({binary_operand2})")
        table.add_row("Hasil", f"{result} ({binary_result})")
        console.print(table)

    except Exception as e:
        console.print(f"[bold red]Terjadi kesalahan: {e}[/bold red]")

if __name__ == "__main__":
    while True:
        simulate_processor()
        continue_simulation = input("\nApakah ingin melanjutkan simulasi? (y/n): ").lower()
        if continue_simulation != 'y':
            console.print("\n[bold red]Simulasi dihentikan.[/bold red]")
            break
