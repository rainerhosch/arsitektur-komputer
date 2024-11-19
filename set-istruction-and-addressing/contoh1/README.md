# Penjelasan Program
### 1. Memori dan Register:

#### - Memori diwakili sebagai array dengan 256 lokasi.
#### - Register ACC adalah akumulator untuk menyimpan hasil sementara.

### 2. Set Instruksi:

#### - LOAD: Memuat nilai dari memori ke register ACC.
#### - ADD: Menambahkan nilai dari memori ke register ACC.
#### - STORE: Menyimpan nilai dari ACC ke memori.
#### - HALT: Menghentikan program.

### 3. Program:

#### - Program terdiri dari daftar tuple (opcode, operand) yang mewakili instruksi.

### 4. Eksekusi:

#### - Program dijalankan secara berurutan menggunakan counter program (pc).