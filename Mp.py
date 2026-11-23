import csv
import os
import sys
FILE_CSV = "cereal.csv"
GRAM_PER_OZ = 28.3495                      
USERS = {"admin": "admin123", "kelompok7d": "mini2026"}
MAKS_LOGIN = 3
SNI_MIN = {"protein": 5, "carbo": 60}
KRITERIA = {"protein":  ("Protein", "g", "benefit"),
    "fiber":    ("Serat", "g", "benefit"),
    "fat":      ("Lemak", "g", "cost"),
    "carbo":    ("Karbohidrat", "g", "cost"),
    "calories": ("Energi", "kkal", "cost"),}
BANDING = ["protein", "carbo", "fiber"]     
TABEL = ["calories", "protein", "fat", "fiber", "carbo"]
RI = {2: 0, 3: 0.58, 4: 0.90, 5: 1.12}      
def judul(teks):
    print(f"\n{'=' * 64}\n{teks:^64}\n{'=' * 64}")
def tunggu():
    input("\nTekan ENTER untuk kembali ke menu...")
def minta_angka(prompt, awal, akhir):
    while True:
        s = input(prompt).strip()
        if s.isdigit() and awal <= int(s) <= akhir:
            return int(s)
        print(f"  ! Masukkan angka {awal}-{akhir}.")
def pilih(daftar, nama=str, prompt="Pilih nomor: "):
    """Tampilkan daftar bernomor, kembalikan item yang dipilih."""
    for i, item in enumerate(daftar, 1):
        print(f"  {i}. {nama(item)}")
    return daftar[minta_angka(prompt, 1, len(daftar)) - 1]
def cetak_tabel(produk, kolom, mulai=1, skor=None):
    kepala = f"{'No':<4}{'Nama':<28}" + "".join(
        f"{KRITERIA[k][0]:>12}" for k in kolom) + (f"{'Skor':>9}" if skor else "")
    print(kepala + "\n" + "-" * len(kepala))
    for i, p in enumerate(produk):
        print(f"{mulai + i:<4}{p['name'][:27]:<28}"
              + "".join(f"{p[k]:>12.2f}" for k in kolom)
              + (f"{skor[i]:>9.4f}" if skor else ""))
def login():
    judul("LOGIN SISTEM REKOMENDASI SEREAL")
    for sisa in range(MAKS_LOGIN - 1, -1, -1):
        user, pw = input("Username : ").strip(), input("Password : ").strip()
        if USERS.get(user) == pw:
            print(f"\nLogin berhasil. Selamat datang, {user}!")
            return True
        print(f"  ! Username/password salah. Sisa percobaan: {sisa}\n")
    print("Login gagal. Program ditutup.")
    return False