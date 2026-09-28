---
description: Aturan Mutlak Keselamatan Kode dan Manipulasi File
---

# Aturan Keselamatan File dan Git (MUTLAK)

Aturan ini dibuat akibat insiden "Doomsday" di mana agen secara tidak sengaja menghancurkan pekerjaan manual berhari-hari milik pengguna akibat penggunaan skrip yang sembrono dan perintah Git yang gegabah.

Setiap agen yang membaca aturan ini **DIWAJIBKAN** mematuhi pedoman berikut tanpa terkecuali:

1. **DILARANG KERAS MENGGUNAKAN SCRIPT OTOMATIS UNTUK MENGEDIT BANYAK FILE SEKALIGUS.**
   - Jangan pernah menjalankan skrip *one-liner* Python (seperti `python -c "import glob..."`), skrip bash, atau command line tool (seperti `sed`, `awk`) untuk melakukan operasi pencarian dan penggantian massal pada file proyek.
   - Pengeditan file HARUS dilakukan secara langsung (direct edit) menggunakan fungsi internal agen, secara hati-hati dan spesifik.

2. **DILARANG KERAS MENGGUNAKAN PERINTAH "GIT RESET", "GIT RESTORE", ATAU "GIT CHECKOUT" TANPA IZIN EKSPLISIT.**
   - Jangan pernah mengasumsikan bahwa pekerjaan pengguna telah di-*commit*. Selalu asumsikan ada *uncommitted changes* (pekerjaan yang belum disimpan) yang sangat berharga di dalam *working directory*.
   - Segala bentuk perintah yang bersifat merusak (destructive) dan menimpa *uncommitted changes* (`git reset --hard`, `git checkout HEAD`, `git restore .`) dilarang mutlak kecuali pengguna secara spesifik dan eksplisit meminta Anda membuang pekerjaannya.

3. **WAJIB MELAKUKAN AUTO-COMMIT SETIAP KALI ADA PERUBAHAN KODE DARI AGEN.**
   - Setiap kali Anda (agen) berhasil mengedit, mengubah, atau memperbaiki *source code* apa pun, Anda **DIWAJIBKAN** langsung menjalankan perintah `git add .` dan `git commit -m "[Deskripsi Perubahan]"` untuk menyimpan versi yang aman.
   - Ini bertindak sebagai titik *checkpoint* agar jika terjadi kesalahan, pekerjaan dapat dengan mudah di-*rollback*.

Melanggar aturan ini akan berakibat fatal bagi proyek pengguna. Selalu patuhi instruksi ini di setiap sesi seumur hidup proyek ini.
