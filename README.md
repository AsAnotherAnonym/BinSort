# BIN SORT

> A Retro Arcade Recycling Game Powered by Python

BinSort adalah game arcade berkecepatan tinggi yang menguji refleks dan kemampuan pemilahan sampah Anda. Dibangun sepenuhnya menggunakan **Python**, **Pygame**, dan **PyCairo**, game ini unik karena **tidak menggunakan aset gambar eksternal**. Semua visual; mulai dari karakter, sampah, latar belakang, hingga antarmuka pengguna, dihasilkan secara prosedural melalui kode (Math-based rendering).

## Daftar Isi

1. [Tentang Game](#tentang-game)
2. [Fitur Utama](#fitur-utama)
3. [Instalasi dan Cara Menjalankan](#instalasi-dan-cara-menjalankan)
4. [Panduan Bermain](#panduan-bermain)
5. [Arsitektur Teknis](#arsitektur-teknis)
6. [Kredit](#kredit)

---

## Tentang Game

Di dunia yang semakin tercemar, tugas Anda adalah memilah sampah yang jatuh dari langit. Anda mengendalikan sebuah tong sampah pintar yang bisa berubah mode antara **Organik (Hijau)** dan **Anorganik (Biru)**. 

Tujuan Anda sederhana: Tangkap sampah yang sesuai, hindari sampah yang salah, dan jangan biarkan sampah mencemari tanah.

## Fitur Utama

* **100% Procedural Assets:** Tidak ada file .png atau .jpg. Semua grafis (lemon, kaleng soda, awan, gunung, dst) digambar secara real-time menggunakan vector graphics library (PyCairo) yang kemudian dikonversi menjadi tekstur pixel-art 8-bit.
* **Procedural Audio:** Efek suara (SFX) untuk menangkap, melompat, dan game over dihasilkan melalui manipulasi gelombang sinus dan square wave secara matematis.
* **Sistem Level Progresif:** 10 level dengan tingkat kesulitan yang terus meningkat (kecepatan jatuh dan frekuensi sampah bertambah).
* **Save System:** Progres level yang terbuka disimpan secara otomatis dalam format JSON.
* **Retro UI:** Antarmuka pengguna bergaya tombol 3D klasik dengan dukungan navigasi mouse penuh.

---

## Instalasi dan Cara Menjalankan

### Prasyarat

Pastikan Anda telah menginstal Python (versi 3.8 atau lebih baru).

### Langkah Instalasi

1.  **Clone atau Unduh Repository ini.**
2.  **Instal Library yang Dibutuhkan:**
    Game ini membutuhkan `pygame` untuk game engine dan `pycairo` untuk pembuatan aset grafis.

    ```bash
    pip install pygame pycairo
    ```

3.  **Setup Font (Opsional tapi Disarankan):**
    Untuk pengalaman retro yang maksimal, unduh font **"Press Start 2P"** dari Google Fonts, ubah namanya menjadi `PressStart2P.ttf`, dan letakkan di folder yang sama dengan `main.py`. Jika tidak ada, game akan menggunakan font default sistem (Arial).

4.  **Jalankan Game:**
    
    ```bash
    python main.py
    ```

---

## Panduan Bermain

### Kontrol

| Aksi | Tombol Keyboard |
| :--- | :--- |
| Gerak Kiri | **A** atau **Panah Kiri** |
| Gerak Kanan | **D** atau **Panah Kanan** |
| Ganti Tipe Tong | **E** (Ada cooldown singkat) |
| Jeda (Pause) | **ESC** |
| Navigasi Menu | **Mouse (Klik Kiri)** |

### Mekanisme Permaianan

* **Tipe Sampah:**
    * **Organik (Wadah Hijau):** Lemon Bekas, Kertas Remuk, Apel Bekas.
    * **Anorganik (Wadah Biru):** Kantong Plastik, Botol Air, Kaleng Soda.
    * **Bonus (bintang):** Menambah nyawa (Health).

* **Aturan Kesehatan (HP):**
    * Menangkap sampah yang **benar**: Skor bertambah.
    * Menangkap sampah yang **salah**: Nyawa berkurang -1.
    * Sampah jatuh ke tanah (**miss**): Nyawa berkurang -1.
    * Game Over jika nyawa habis.

* **Deteksi Tutup:**
    Sampah hanya dianggap "tertangkap" jika mengenai bagian atas (tutup) tong sampah. Jika sampah mengenai sisi samping tong, itu dianggap gagal dan akan mengurangi nyawa.

---

## Arsitektur Teknis

Proyek ini menerapkan prinsip Object-Oriented Programming (OOP) untuk memastikan kode yang bersih dan mudah dikembangkan; dan prinsip Grafika Komputer agar file game bisa tetap berukuran kecil.

### Struktur Class Utama

* **GameManager:** Mengatur State Machine (Title, Playing, Paused, GameOver) dan loop utama game.
* **AssetFactory:** Jantung visual game ini. Class statis yang menggunakan PyCairo untuk menggambar bentuk vektor pada kanvas virtual, menerapkan tekstur noise, dan mengonversinya menjadi Pygame Surface yang kompatibel.
* **AudioFactory:** Menghasilkan objek Pygame Sound dari raw array data (PCM) menggunakan fungsi matematika gelombang.
* **UIManager:** Menangani rendering teks dengan outline hitam dan pembuatan tombol interaktif bergaya 3D.
* **LevelManager:** Mengatur logika skalabilitas tingkat kesulitan (kecepatan spawn dan jumlah sampah) menggunakan fungsi matematika linear/logaritmik.

---

## Kredit

Disusun oleh mahasiswa IF'24:

Muhammad Raihan Ramdhani (3059)
Mochammad Ryan Alviansyah (3005)
Arul Pramana Bahari (3035)

Dikembangkan sebagai proyek eksplorasi kemampuan Python dalam pembuatan game tanpa ketergantungan aset eksternal.

**Teknologi:**
* Python
* Pygame (Engine)
* PyCairo (Graphics Generation)