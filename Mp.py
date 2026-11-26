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
    while True:
        try:
            user = input("Username : ").strip()
            pw = input("Password : ").strip()
            if USERS[user] == pw:          # KeyError jika username tidak ada
                print(f"\nLogin berhasil. Selamat datang, {user}!")
                return True
            print("  ! Password salah. Silakan coba lagi.\n")
        except KeyError:
            print("  ! Username tidak terdaftar. Silakan coba lagi.\n")
        except (KeyboardInterrupt, EOFError):
            print("\nLogin dibatalkan. Program ditutup.")
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
def bobot_ahp(urutan):
    """Matriks Saaty dari urutan prioritas (selisih peringkat -> skala 1-9).
    Return: (bobot per kriteria, CR)."""
    n = len(urutan)
    mat = [[1 if i == j else min(9, 1 + j - i) if i < j else 1 / min(9, 1 + i - j)
            for j in range(n)] for i in range(n)]
    jml = [sum(baris[j] for baris in mat) for j in range(n)]
    w = [sum(mat[i][j] / jml[j] for j in range(n)) / n for i in range(n)]
    lam = sum(sum(mat[i][j] * w[j] for j in range(n)) / w[i] for i in range(n)) / n
    cr = (lam - n) / (n - 1) / RI[n] if RI[n] else 0
    return dict(zip(urutan, w)), cr


def hitung_saw(data, bobot):
    """Normalisasi SAW + skor terbobot. Return [(skor, produk)] terurut."""
    ekstrem = {k: (min(p[k] for p in data), max(p[k] for p in data)) for k in bobot}

    def normal(k, x):
        lo, hi = ekstrem[k]
        if KRITERIA[k][2] == "benefit":
            return x / hi if hi > 0 else 0
        return lo / x if lo > 0 else (lo + 1) / (x + 1)   # +1 bila ada nilai 0

    hasil = [(sum(w * normal(k, p[k]) for k, w in bobot.items()), p) for p in data]
    return sorted(hasil, key=lambda h: round(h[0], 4), reverse=True)


def menu_rekomendasi(data):
    judul("REKOMENDASI SEREAL (AHP - SAW)")

    cand = []
    for p in data:
        if not p["gagal"]:
            cand.append(p)

    if len(cand) < 5:
        print("Kandidat yang lolos kurang dari 5 produk.")
        tunggu()
        return

    print("Kandidat yang lolos:", len(cand), "produk")

    daftar = []
    for k in KRITERIA:
        daftar.append(k)

    print("\nPilih kriteria yang ingin diprioritaskan:")
    for i in range(len(daftar)):
        k = daftar[i]
        print(i + 1, ".", KRITERIA[k][0])


    while True:
        pilihan = input("\nMasukkan nomor kriteria dipisah koma (contoh 1,2,4): ")
        nomor = pilihan.split(",")
        idx = []
        valid = True

        for x in nomor:
            try:
                angka = int(x.strip())
                if angka < 1 or angka > len(daftar):
                    valid = False
                elif angka in idx:
                    valid = False
                else:
                    idx.append(angka)
            except ValueError:
                valid = False

        if valid and len(idx) >= 2:
            break
        print("! Pilih minimal 2 nomor berbeda yang valid.")

    sisa = []
    for i in idx:
        sisa.append(daftar[i - 1])
   
    urutan = []
    print("\nUrutkan kriteria dari yang paling penting.")

    while len(sisa) > 0:
        print("\nPilih prioritas:")
        for i in range(len(sisa)):
            print(i + 1, ".", KRITERIA[sisa[i]][0])

        nomor_pilih = minta_angka("Pilih nomor: ", 1, len(sisa))
        urutan.append(sisa[nomor_pilih - 1])
        sisa.pop(nomor_pilih - 1)

    bobot, cr = bobot_ahp(urutan)

    print("\n--- Bobot Kriteria (AHP) ---")
    for k in bobot:
        print(KRITERIA[k][0], ":", round(bobot[k], 4))

    print("CR =", round(cr, 4))
    if cr < 0.1:
        print("Penilaian KONSISTEN")
    else:
        print("Penilaian TIDAK KONSISTEN")

    hasil = hitung_saw(cand, bobot)
    produk_top = []
    skor_top = []

    for i in range(5):
        produk_top.append(hasil[i][1])
        skor_top.append(hasil[i][0])

    print("\n--- TOP 5 REKOMENDASI SEREAL (SAW) ---")
    cetak_tabel(produk_top, list(bobot), skor=skor_top)
    print("\nProduk terbaik:", hasil[0][1]["name"])
    print("Skor:", round(hasil[0][0], 4))
    tunggu()


def menu_perbandingan(data):
    judul("PERBANDINGAN DUA PRODUK SEREAL")

    print("Pilih parameter pembanding:")
    for i in range(len(BANDING)):
        k = BANDING[i]
        print(i + 1, ".", KRITERIA[k][0])
    print(len(BANDING) + 1, ". Ketiganya")

    pilihan = minta_angka("Pilih parameter: ", 1, len(BANDING) + 1)

    param = []
    if pilihan == len(BANDING) + 1:
        for k in BANDING:
            param.append(k)
    else:
        param.append(BANDING[pilihan - 1])

    print("\nMasukkan produk yang ingin dibandingkan.")
    a = pilih_produk(data, "sereal pertama")
    b = pilih_produk(data, "sereal kedua")

    while a["name"] == b["name"]:
        print("! Produk kedua harus berbeda dari produk pertama.")
        b = pilih_produk(data, "sereal kedua")

    print("\nPerbandingan kandungan gizi per 100 gram:")
    print("Parameter                 ", a["name"][:18], "   ", b["name"][:18])
    print("-" * 65)

    for k in param:
        label = KRITERIA[k][0]
        satuan = KRITERIA[k][1]
        print(label, "(", satuan, "):", a[k], " | ", b[k])


    skor_a = 0
    skor_b = 0

    print("\nAnalisis keunggulan:")
    for k in param:
        label = KRITERIA[k][0]
        satuan = KRITERIA[k][1]
        jenis = KRITERIA[k][2]

        if a[k] == b[k]:
            print("-", label, ": seri (", a[k], satuan, ")")
        elif jenis == "benefit":
            if a[k] > b[k]:
                print("-", label, ":", a["name"], "lebih unggul")
                skor_a = skor_a + 1
            else:
                print("-", label, ":", b["name"], "lebih unggul")
                skor_b = skor_b + 1
        else:
            if a[k] < b[k]:
                print("-", label, ":", a["name"], "lebih unggul")
                skor_a = skor_a + 1
            else:
                print("-", label, ":", b["name"], "lebih unggul")
                skor_b = skor_b + 1

    print("\nSkor keunggulan:")
    print(a["name"], ":", skor_a)
    print(b["name"], ":", skor_b)

    if skor_a > skor_b:
        print("PEMENANG:", a["name"])
    elif skor_b > skor_a:
        print("PEMENANG:", b["name"])
    else:
        print("HASIL: seri.")

    print("\nCatatan: protein dan serat semakin tinggi semakin baik.")
    print("Karbohidrat semakin rendah semakin baik.")
    tunggu()


MENU = {
    1: ("Lihat Data Sereal", menu_lihat_data),
    2: ("Pemeriksaan Kandungan Gizi", menu_pemeriksaan),
    3: ("Rekomendasi Sereal (Top 5 AHP-SAW)", menu_rekomendasi),
    4: ("Perbandingan Dua Produk", menu_perbandingan),
}


def main():
    if not login():
        return
    data = muat_data(FILE_CSV)
    while True:
        judul("MENU UTAMA")
        for no, (nama, _) in MENU.items():
            print(f"  {no}. {nama}")
        print("  5. Keluar")
        pilihan = minta_angka("\nPilih menu (1-5): ", 1, 5)
        if pilihan == 5:
            return print("\nTerima kasih. Program selesai.")
        MENU[pilihan][1](data)
if __name__ == "__main__":
    main()