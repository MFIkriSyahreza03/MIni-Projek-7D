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
def ke_float(teks):
    """Terima desimal koma (0,33) maupun titik (0.33)."""
    return float(str(teks).strip().replace(",", "."))
def muat_data(path):
    """Baca CSV -> list of dict berisi nilai gizi per 100 g + hasil SNI."""
    if not os.path.exists(path):
        sys.exit(f"File '{path}' tidak ditemukan di folder program.")

    with open(path, encoding="utf-8-sig") as f:
        header = f.readline()
        pemisah = max(",;\t", key=header.count)     
        f.seek(0)
        pembaca = csv.DictReader(f, delimiter=pemisah)
        pembaca.fieldnames = [(k or "").strip().lower() for k in pembaca.fieldnames]
        hilang = [k for k in ["name", "weight", *KRITERIA] if k not in pembaca.fieldnames]
        if hilang:
            sys.exit("Kolom wajib tidak ada di CSV: " + ", ".join(hilang)
                     + "\nKolom yang terbaca: " + ", ".join(pembaca.fieldnames))

        data = []
        for baris in pembaca:
            try:
                gram = ke_float(baris["weight"]) * GRAM_PER_OZ
                gizi = {k: ke_float(baris[k]) for k in KRITERIA}
            except (ValueError, TypeError, AttributeError):
                continue                             # kosong / bukan angka
            if gram <= 0 or min(gizi.values()) < 0:  # -1 = data tidak tersedia
                continue
            produk = {"name": baris["name"].strip()}
            produk.update({k: round(v / gram * 100, 2) for k, v in gizi.items()})
            # Pemeriksaan acuan SNI -> daftar alasan gagal (kosong = lolos)
            produk["gagal"] = [f"{KRITERIA[k][0]} {produk[k]:g} g < min {m} g"
                               for k, m in SNI_MIN.items() if produk[k] < m]
            data.append(produk)
    if not data:
        sys.exit("Tidak ada baris data yang valid di cereal.csv.")
    return data


def pilih_produk(data, label):
    while True:
        kata = input(f"Nama {label} (sebagian nama juga boleh): ").strip().lower()
        hasil = [p for p in data if kata and kata in p["name"].lower()]
        if len(hasil) == 1:
            return hasil[0]
        if hasil:
            print("  Ditemukan beberapa produk:")
            return pilih(hasil, lambda p: p["name"])
        print("  ! Tidak ditemukan, coba kata lain.")
# ============================ MENU 1: DATA ============================
def menu_lihat_data(data):
    judul("DATA SEREAL (per 100 gram)")
    print(f"Jumlah produk valid: {len(data)}\n")
    ukuran = 15
    halaman = (len(data) - 1) // ukuran + 1
    for h in range(halaman):
        cetak_tabel(data[h * ukuran:(h + 1) * ukuran], TABEL, h * ukuran + 1)
        print(f"\nHalaman {h + 1}/{halaman}")
        if h + 1 < halaman and input(
                "ENTER = halaman berikutnya, Q = kembali: ").strip().lower() == "q":
            break
    tunggu()
# ======================== MENU 2: PEMERIKSAAN GIZI ========================
def menu_pemeriksaan(data):
    judul("PEMERIKSAAN KANDUNGAN GIZI")
    print("Batas acuan SNI 01-4270-1996 (per 100 g):")
    for k, m in SNI_MIN.items():
        print(f"  - {KRITERIA[k][0]:<12}: >= {m} g")
    print("\n1. Periksa satu produk\n2. Ringkasan semua produk")

    if minta_angka("Pilih (1/2): ", 1, 2) == 1:
        p = pilih_produk(data, "sereal")
        print(f"\nProduk: {p['name']}")
        for k, m in SNI_MIN.items():
            print(f"  {KRITERIA[k][0]:<12}: {p[k]:>8g} g    -> "
                  f"{'Memenuhi' if p[k] >= m else 'TIDAK memenuhi'}")
        print("\nStatus akhir:", "TIDAK LOLOS (tidak akan direkomendasikan)"
              if p["gagal"] else "LOLOS (masuk kandidat rekomendasi)")
    else:
        lolos = [p for p in data if not p["gagal"]]
        print(f"\nLolos       : {len(lolos)} produk"
              f"\nTidak lolos : {len(data) - len(lolos)} produk\n\nDaftar produk LOLOS:")
        for p in lolos:
            print("  +", p["name"])
        if input("\nTampilkan produk tidak lolos beserta alasannya? (y/n): "
                 ).strip().lower() == "y":
            for p in data:
                if p["gagal"]:
                    print(f"  - {p['name']}: {'; '.join(p['gagal'])}")
    tunggu()
