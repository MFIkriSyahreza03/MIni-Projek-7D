MINI PROJECT PROGRAM KOMPUTER

Analisis dan Rekomendasi Pemilihan Sereal Sarapan Berdasarkan Kandungan Gizi Menggunakan Metode AHP dan SAW

1. Latar Belakang

Sereal merupakan salah satu pilihan makanan yang sering dikonsumsi sebagai menu sarapan. Setiap produk sereal memiliki kandungan gizi yang berbeda, seperti protein, serat, lemak, karbohidrat, dan kalori. Perbedaan kandungan tersebut membuat konsumen perlu mempertimbangkan nilai gizi sebelum memilih produk sereal.

Berdasarkan permasalahan tersebut, dibuat sebuah program yang dapat membantu menganalisis dan memberikan rekomendasi pemilihan sereal berdasarkan kandungan gizinya. Program ini menerapkan metode Analytical Hierarchy Process (AHP) dan Simple Additive Weighting (SAW) untuk menentukan bobot kriteria serta menghitung peringkat produk sereal.

2. Tujuan Program

Program ini bertujuan untuk:

- Membantu pengguna mengetahui kandungan gizi pada produk sereal.
- Memeriksa kandungan gizi produk berdasarkan standar yang ditentukan dalam program.
- Membandingkan kandungan gizi dari dua produk sereal.
- Memberikan rekomendasi produk sereal berdasarkan perhitungan metode AHP dan SAW.

3. Deskripsi Program

Program ini dibuat menggunakan bahasa pemrograman Python dengan memanfaatkan dataset dalam format CSV. Pengguna dapat melihat data sereal, melakukan pemeriksaan kandungan gizi, membandingkan dua produk, serta memperoleh rekomendasi berdasarkan kriteria yang dipilih.

4. Fitur Program

Program memiliki empat menu utama:

1. Lihat Data Sereal

Menampilkan daftar produk sereal beserta informasi kandungan gizinya.

2. Pemeriksaan Kandungan Gizi

Melakukan pemeriksaan kandungan protein dan karbohidrat berdasarkan batas minimum yang telah ditentukan dalam program.

3. Rekomendasi Sereal (AHP–SAW)

Menghasilkan rekomendasi produk berdasarkan bobot prioritas kriteria menggunakan metode AHP dan perhitungan nilai akhir menggunakan metode SAW.

4. Perbandingan Dua Produk

Membandingkan dua produk sereal berdasarkan kandungan protein, karbohidrat, dan serat.

5. Metode yang Digunakan

  A. Analytical Hierarchy Process (AHP)
     AHP digunakan untuk menentukan bobot atau tingkat kepentingan setiap kriteria. Pengguna memilih dan mengurutkan kriteria berdasarkan prioritasnya. Program
     kemudian membentuk matriks perbandingan dan menghitung bobot masing-masing kriteria serta nilai Consistency Ratio (CR).

  B. Simple Additive Weighting (SAW)
     SAW digunakan untuk menghitung nilai akhir setiap produk berdasarkan bobot kriteria yang diperoleh dari AHP. Perhitungan dilakukan melalui proses
     normalisasi, perkalian nilai normalisasi dengan bobot, dan penjumlahan untuk mendapatkan skor akhir produk.

6. Kriteria Penilaian
  Kriteria yang digunakan dalam proses rekomendasi meliputi: 
  No.| Kriteria| Jenis
  1| Protein| Benefit
  2| Serat| Benefit
  3| Lemak| Cost
  4| Karbohidrat| Cost
  5| Kalori| Cost

  Keterangan:
  - Benefit: semakin tinggi nilai kriteria, semakin baik.
  - Cost: semakin rendah nilai kriteria, semakin baik.

7. Dataset
   Dataset yang digunakan bernama "cereal.csv". Dataset berisi informasi produk sereal beserta kandungan gizinya yang digunakan sebagai sumber data dalam proses
   pemeriksaan, perbandingan, dan rekomendasi.

9. Teknologi yang Digunakan
   - Bahasa Pemrograman: Python
   - Format Dataset: CSV
   - Code Editor: Visual Studio Code
   - Version Control: Git dan GitHub

10. Cara Menjalankan Program
    
   1. Pastikan Python sudah terpasang pada perangkat.
   2. Clone atau download repository ini.
   3. Buka folder proyek menggunakan Visual Studio Code.
   4. Pastikan file program Python dan "cereal.csv" berada pada folder yang sesuai.
   5. Buka terminal pada folder proyek.
   6. Jalankan program menggunakan perintah berikut:
      python nama_file_program.py
      Ganti "nama_file_program.py" dengan nama file program utama.


11. Penutup
    Melalui mini project ini, diharapkan program dapat membantu pengguna dalam memahami kandungan gizi dan menentukan pilihan produk sereal berdasarkan kriteria
    yang digunakan. Selain itu, proyek ini menjadi penerapan konsep pemrograman komputer dalam pengolahan data dan sistem pendukung keputusan sederhana.Ini Projek
    7D

