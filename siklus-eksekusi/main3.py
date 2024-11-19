import time
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Simulasi memori dengan 10 lokasi
memory = [0] * 10  # Memori dengan nilai awal 0
register = None  # Register untuk menyimpan hasil sementara

# Untuk visualisasi
fig, ax = plt.subplots()
bars = ax.bar(range(len(memory)), memory, color='blue')

# Fungsi untuk memperbarui visualisasi
def update_bars(frame):
    ax.clear()  # Menghapus frame sebelumnya
    ax.bar(range(len(memory)), memory, color='blue')
    ax.set_ylim(0, 100)  # Nilai maksimal untuk visualisasi
    ax.set_title(f"Simulasi Prosesor - Iterasi {frame + 1}")
    ax.set_xlabel("Alamat Memori")
    ax.set_ylabel("Nilai")
    return bars

# Fungsi untuk instruksi eksekusi
def execute_instruction(instruction):
    global memory  # Memori yang diupdate harus bersifat global
    address = random.randint(0, len(memory) - 1)  # Menggunakan alamat acak dalam memori
    memory[address] = instruction  # Menyimpan instruksi (angka) di memori
    return memory

# Fungsi utama untuk mensimulasikan proses prosesor
def processor_simulation():
    print("Simulasi Prosesor Dimulai...")
    time.sleep(1)

    # Setup untuk animasi
    def anim_func(frame):
        random_number = random.randint(1, 100)  # Menghasilkan angka acak antara 1-100
        execute_instruction(random_number)  # Eksekusi instruksi dengan angka acak
        return update_bars(frame)

    ani = FuncAnimation(fig, anim_func, frames=150, interval=200, blit=False, repeat=False)

    plt.show()

    print("Simulasi selesai.")

if __name__ == "__main__":
    processor_simulation()
