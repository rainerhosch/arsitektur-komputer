import time
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Simulasi memori dengan 10 lokasi
memory = [0] * 10  # Memori dengan nilai awal 0

# Fungsi untuk membuat figure dan axis baru
def create_figure():
    fig, ax = plt.subplots()
    ax.set_ylim(0, 100)  # Nilai maksimal untuk visualisasi
    ax.set_xlabel("Alamat Memori")
    ax.set_ylabel("Nilai")
    return fig, ax

# Fungsi untuk menampilkan status prosesor di dalam visualisasi
def update_bars(ax, frame):
    ax.clear()  # Menghapus frame sebelumnya
    colors = ['red' if value > 80 else 'blue' if value > 50 else 'green' for value in memory]
    ax.bar(range(len(memory)), memory, color=colors)
    ax.set_ylim(0, 100)  # Nilai maksimal untuk visualisasi
    ax.set_title(f"Simulasi Prosesor - Status Memori")

# Fungsi untuk mengambil input dan menyusunnya menjadi instruksi
def get_input():
    return input("Masukkan data atau perintah (angka, ketik 'exit' untuk berhenti): ")

# Fungsi untuk instruksi eksekusi
def execute_instruction(instruction):
    global memory  # Memori yang diupdate harus bersifat global
    address = random.randint(0, len(memory) - 1)  # Menggunakan alamat acak dalam memori
    memory[address] = int(instruction)  # Menyimpan instruksi (angka) di memori
    return memory

# Fungsi utama untuk mensimulasikan proses prosesor
def processor_simulation_by_input():
    global memory  # Memori yang diupdate harus bersifat global
    memory = [0] * 10  # Reset memori

    print("Simulasi Prosesor Dimulai...")
    time.sleep(1)

    # Membuat ulang figure dan axis
    fig, ax = create_figure()

    # Animasi hanya aktif saat diperlukan
    ani = None

    def anim_func(frame):
        update_bars(ax, frame)

    plt.show(block=False)  # Membuka visualisasi tanpa menghalangi proses berikutnya

    while True:
        if ani:
            ani.event_source.stop()  # Hentikan animasi saat menunggu input

        user_input = get_input()
        if user_input.lower() == 'exit':
            print("Simulasi selesai.")
            plt.close(fig)  # Menutup grafik
            break
        try:
            # Cek apakah input adalah bilangan desimal
            float(user_input)  # Mengubah input menjadi float untuk validasi
            execute_instruction(user_input)  # Simulasikan set instruksi berdasarkan input

            # Animasi berjalan sekali untuk memperbarui grafik
            ani = FuncAnimation(fig, anim_func, frames=1, interval=500, blit=False)
            plt.pause(0.5)  # Pause untuk memberikan waktu pembaruan
        except ValueError:
            print("Input tidak valid. Silakan masukkan bilangan desimal/angka.")

# Fungsi utama untuk mensimulasikan proses prosesor
def processor_simulation_auto():
    global memory  # Memori yang diupdate harus bersifat global
    memory = [0] * 10  # Reset memori
    
    print("Simulasi Prosesor Dimulai...")
    time.sleep(1)

    # Membuat ulang figure dan axis
    fig, ax = create_figure()

    def anim_func(frame):
        random_number = random.randint(1, 100)  # Menghasilkan angka acak antara 1-100
        print(f"Instruksi yang dieksekusi: {random_number}")  # Menampilkan angka acak yang dieksekusi
        execute_instruction(random_number)  # Eksekusi instruksi dengan angka acak
        update_bars(ax, frame)

    ani = FuncAnimation(fig, anim_func, frames=150, interval=200, blit=False, repeat=False)

    plt.show()
    print("Simulasi selesai.")

if __name__ == "__main__":
    while True:
        print(f"{'='*40}")
        print("Silahkan pilih mode:")
        print(f"{'='*40}")
        print("1. mode auto")
        print("2. mode manual by input\n")
        print("'exit', untuk keluar.")
        print(f"{'='*40}\n")
        mode = input("masukan pilihan mode: ")
        if mode.lower() == 'exit':
            print("Simulasi selesai.")
            break
        elif mode == '1':
            processor_simulation_auto()
        elif mode == '2':
            processor_simulation_by_input()
        else:
            print("Pilihan tidak valid. Silakan masukkan 1 atau 2.")
