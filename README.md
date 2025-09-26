# omr-3kolom-30soal
Bismillah.
Program mengoreksi pilihan ganda (ABCDE) 30 nomor dengan kode soal berbeda-beda tiap siswa.

## yang perlu disiapkan
1. Python dengan library:
   - numpy
   - tkinter (untuk memunculkan dialog memasukkan kode kunci)
   - cv2 (opencv)
2. ada webcam
3. ljk.

## cara:
1. Siapkan file `kunci_kode.txt` yang berisi kunci jawabannya. Formatnya seperti ini:
```
330:[3, 1, 0, 0, 2, 4, 3, 1, 4, 3, 3, 0, 4, 0, 0, 4, 0, 1, 2, 1, 0, 0, 4, 2, 4, 1, 4, 4, 1, 3, ]
511:[2, 0, 2, 0, 2, 1, 1, 4, 0, 1, 2, 2, 2, 0, 4, 3, 0, 3, 1, 3, 3, 1, 3, 3, 2, 3, 4, 4, 3, 3, ]
512:[4, 2, 4, 3, 1, 1, 1, 4, 0, 3, 2, 1, 1, 2, 4, 1, 1, 4, 0, 2, 1, 3, 0, 2, 4, 1, 4, 2, 4, 2, ]
543:[0, 3, 2, 1, 4, 4, 1, 2, 0, 2, 2, 2, 0, 0, 4, 4, 1, 0, 0, 3, 1, 2, 4, 2, 0, 1, 3, 4, 2, 4, ]
...
```
330 itu kode soalnya, 3, 1, 0, 0, ... itu kuncinya yang berarti D, B, A, A, ...
2. Shortcut (pada saat jendela cv2 nya terbuka, kameranya terdeteksi):
   - `k` untuk memasukkan kunci kode, sekaligus mengetahui skor.
   - `s` untuk menyimpan
   - `q` atau `Esc` untuk keluar
3. Jika webcam tidak terdeteksi, ganti pada baris `port = 0` menjadi bilangan lain seperti 2, 3, 4, dsb.
