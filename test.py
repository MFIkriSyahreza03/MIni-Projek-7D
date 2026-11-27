print("=" * 65)
print("MINI PROJECT PROGRAMA KOMPUTER".center(70))
print("=" * 65)

print("" \
"ANALISIS DAN REKOMENDASI PEMILIHAN SEREAL SARAPAN".center(70))
print("BERDASARKAN KANDUNGAN GIZI MENGGUNAKAN METODE AHP-SAW.".center(70))

print("\n" + "=" * 65)
print("KELOMPOK 7D".center(70))
print("=" * 65)

print("Anggota Kelompok:".center(70))
print("1. Aprilia Putri Rawi          2610931020".center(70))
print("2. Raffi Raditia               2610933021".center(70))
print("3. Muhammad Fikri Syahreza    2610933041".center(70))
print("4. Azka Zalila Raisa           2610937003".center(70))
print()
print("Asisten Pembimbing:".center(70))
print("Anisha Nur Aprilia".center(70))
print()
print("Dosen Pengampu:".center(70))
print("Ikhwan Arief, S.T., M.Sc.".center(70))

print("\n" + "=" * 65)
print("LABORATORIUM SISTEM INFORMASI DAN KEPUTUSAN".center(70))
print("DEPARTEMEN TEKNIK INDUSTRI".center(70))
print("FAKULTAS TEKNIK".center(70))
print("UNIVERSITAS ANDALAS".center(70))

import csv
import os
import sys

FILE_CSV = "cereal.csv"
GRAM_PER_OZ = 28.3495                      
USERS = {"admin": "admin123", "kelompok7d": "mini2026"}
SNI_MIN = {"protein": 5, "carbo": 60}
KRITERIA = {"protein":  ("Protein", "g", "benefit"),
    "fiber":    ("Serat", "g", "benefit"),
    "fat":      ("Lemak", "g", "cost"),
    "carbo":    ("Karbohidrat", "g", "cost"),
    "calories": ("Energi", "kkal", "cost"),}
BANDING = ["protein", "carbo", "fiber"]     
TABEL = ["calories", "protein", "fat", "fiber", "carbo"]
RI = {2: 0, 3: 0.58, 4: 0.90, 5: 1.12}


class Tabel:
    """Cetak tabel ber-border. rata: '<' kiri / '>' kanan, satu huruf per kolom."""
    def __init__(self, kolom, rata=None):
        self.kolom, self.baris = kolom, []
        self.rata = rata or "<" * len(kolom)

    def tambah(self, *sel):
        self.baris.append([str(x) for x in sel])

    def cetak(self):
        w = [max(len(r[i]) for r in [self.kolom] + self.baris) for i in range(len(self.kolom))]
        gr = "+" + "+".join("-" * (x + 2) for x in w) + "+"
        f = lambda r, a: "|" + "|".join(f" {x:{a[i]}{w[i]}} " for i, x in enumerate(r)) + "|"
        print(gr, f(self.kolom, "^" * len(w)), gr, *[f(r, self.rata) for r in self.baris], gr, sep="\n")


class Tampilan:
    """Fungsi bantu input/output terminal."""

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
        return daftar[Tampilan.minta_angka(prompt, 1, len(daftar)) - 1]

    def cetak_tabel(produk, kolom, mulai=1, skor=None):
        t = Tabel(["No", "Nama"] + (["Peringkat"] if skor else [])
                  + [KRITERIA[k][0] for k in kolom] + (["Skor"] if skor else []),
                  "<<" + ("^" if skor else "") + ">" * (len(kolom) + bool(skor)))
        for i, p in enumerate(produk):
            # produk sudah terurut dari skor tertinggi -> peringkat berurutan 1, 2, 3, ...
            t.tambah(mulai + i, p["name"][:27], *([i + 1] if skor else []),
                     *[f"{p[k]:.2f}" for k in kolom],
                     *([f"{skor[i]:.4f}"] if skor else []))
        t.cetak()


class Autentikasi:
    """Login tanpa batas percobaan (diulang sampai berhasil atau dibatalkan)."""

    @staticmethod
    def login():
        Tampilan.judul("LOGIN SISTEM REKOMENDASI SEREAL")
        while True:
            try:
                user = input("Username : ").strip()
                pw = input("Password : ").strip()
                if USERS[user] != pw:        # KeyError otomatis bila username tidak ada
                    raise ValueError("password salah")
                print(f"\nLogin berhasil. Selamat datang, {user}!")
                return True
            except KeyError:
                print("  ! Username tidak terdaftar. Silakan coba lagi.\n")
            except ValueError:
                print("  ! Password salah. Silakan coba lagi.\n")
            except (KeyboardInterrupt, EOFError):
                print("\nLogin dibatalkan. Program ditutup.")
                return False


class RepositoriSereal:
    """Membaca CSV dan memilih produk sereal."""
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
                    gram = RepositoriSereal.ke_float(baris["weight"]) * GRAM_PER_OZ
                    gizi = {k: RepositoriSereal.ke_float(baris[k]) for k in KRITERIA}
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
                return Tampilan.pilih(hasil, lambda p: p["name"])
            print("  ! Tidak ditemukan, coba kata lain.")


class AHP:
    """Pembobotan kriteria (Analytic Hierarchy Process)."""
    def hitung(urutan):
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


class SAW:
    """Perangkingan alternatif (Simple Additive Weighting)."""
    def hitung(data, bobot):
        """Normalisasi SAW + skor terbobot. Return [(skor, produk)] terurut."""
        ekstrem = {k: (min(p[k] for p in data), max(p[k] for p in data)) for k in bobot}
        def normal(k, x):
            lo, hi = ekstrem[k]
            if KRITERIA[k][2] == "benefit":
                return x / hi if hi > 0 else 0
            return lo / x if lo > 0 else (lo + 1) / (x + 1)   # +1 bila ada nilai 0
        hasil = [(sum(w * normal(k, p[k]) for k, w in bobot.items()), p) for p in data]
        return sorted(hasil, key=lambda h: round(h[0], 4), reverse=True)


class PemeriksaanGizi:
    """Menu pemeriksaan gizi terhadap SNI."""
    def menu_pemeriksaan(data):
        Tampilan.judul("PEMERIKSAAN KANDUNGAN GIZI")
        print("Batas acuan SNI 01-4270-1996 (per 100 g):")
        for k, m in SNI_MIN.items():
            print(f"  - {KRITERIA[k][0]:<12}: >= {m} g")
        print("\n1. Periksa satu produk\n2. Ringkasan semua produk")
        if Tampilan.minta_angka("Pilih (1/2): ", 1, 2) == 1:
            p = RepositoriSereal.pilih_produk(data, "sereal")
            print(f"\nProduk: {p['name']}")
            t = Tabel(["Parameter", "Nilai (g)", "Min (g)", "Status"], "<>><")
            for k, m in SNI_MIN.items():
                t.tambah(KRITERIA[k][0], f"{p[k]:g}", m, "Memenuhi" if p[k] >= m else "TIDAK memenuhi")
            t.cetak()
            print("\nStatus akhir:", "TIDAK LOLOS (tidak akan direkomendasikan)"
                  if p["gagal"] else "LOLOS (masuk kandidat rekomendasi)")
        else:
            lolos = [p for p in data if not p["gagal"]]
            print(f"\nLolos       : {len(lolos)} produk"
                  f"\nTidak lolos : {len(data) - len(lolos)} produk\n\nDaftar produk LOLOS:")
            t = Tabel(["No", "Nama", "Protein", "Karbohidrat"], "<<>>")
            for i, p in enumerate(lolos, 1):
                t.tambah(i, p["name"][:35], f"{p['protein']:.2f}", f"{p['carbo']:.2f}")
            t.cetak()
            if input("\nTampilkan produk tidak lolos beserta alasannya? (y/n): "
                     ).strip().lower() == "y":
                t = Tabel(["Nama", "Alasan"])
                for p in data:
                    if p["gagal"]:
                        t.tambah(p["name"][:30], "; ".join(p["gagal"]))
                t.cetak()
        Tampilan.tunggu()


class Rekomendasi:
    """Menu rekomendasi Top 5 (AHP-SAW)."""
    def menu_rekomendasi(data):
        Tampilan.judul("REKOMENDASI SEREAL (AHP - SAW)")
        cand = []
        for p in data:
            if not p["gagal"]:
                cand.append(p)
        if len(cand) < 5:
            print("Kandidat yang lolos kurang dari 5 produk.")
            Tampilan.tunggu()
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
            nomor_pilih = Tampilan.minta_angka("Pilih nomor: ", 1, len(sisa))
            urutan.append(sisa[nomor_pilih - 1])
            sisa.pop(nomor_pilih - 1)
        bobot, cr = AHP.hitung(urutan)
        print("\n--- Bobot Kriteria (AHP) ---")
        t = Tabel(["Kriteria", "Bobot"], "<>")
        for k in bobot:
            t.tambah(KRITERIA[k][0], f"{bobot[k]:.4f}")
        t.cetak()
        print("CR =", round(cr, 4))
        if cr < 0.1:
            print("Penilaian KONSISTEN")
        else:
            print("Penilaian TIDAK KONSISTEN")
        hasil = SAW.hitung(cand, bobot)
        produk_top = []
        skor_top = []
        for i in range(5):
            produk_top.append(hasil[i][1])
            skor_top.append(hasil[i][0])
        print("\n--- TOP 5 REKOMENDASI SEREAL (SAW) ---")
        Tampilan.cetak_tabel(produk_top, list(bobot), skor=skor_top)
        print("\nProduk terbaik:", hasil[0][1]["name"])
        print("Skor:", round(hasil[0][0], 4))
        Tampilan.tunggu()


class Perbandingan:
    """Menu perbandingan dua produk."""
    @staticmethod
    def menu_perbandingan(data):
        Tampilan.judul("PERBANDINGAN DUA PRODUK SEREAL")
        print("Pilih parameter pembanding:")
        for i in range(len(BANDING)):
            k = BANDING[i]
            print(i + 1, ".", KRITERIA[k][0])
        print(len(BANDING) + 1, ". Ketiganya")
        pilihan = Tampilan.minta_angka("Pilih parameter: ", 1, len(BANDING) + 1)
        param = []
        if pilihan == len(BANDING) + 1:
            for k in BANDING:
                param.append(k)
        else:
            param.append(BANDING[pilihan - 1])
        print("\nMasukkan produk yang ingin dibandingkan.")
        a = RepositoriSereal.pilih_produk(data, "sereal pertama")
        b = RepositoriSereal.pilih_produk(data, "sereal kedua")
        while a["name"] == b["name"]:
            print("! Produk kedua harus berbeda dari produk pertama.")
            b = RepositoriSereal.pilih_produk(data, "sereal kedua")
        print("\nPerbandingan kandungan gizi per 100 gram:")
        t = Tabel(["Parameter", a["name"][:20], "Peringkat", b["name"][:20], "Peringkat"],
                  "<>^>^")
        for k in param:
            if a[k] == b[k]:
                rank_a = rank_b = 1                          # seri -> sama-sama peringkat 1
            else:
                a_unggul = (a[k] > b[k]) if KRITERIA[k][2] == "benefit" else (a[k] < b[k])
                rank_a, rank_b = (1, 2) if a_unggul else (2, 1)
            t.tambah(f"{KRITERIA[k][0]} ({KRITERIA[k][1]})", a[k], rank_a, b[k], rank_b)
        t.cetak()
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
        Tampilan.tunggu()


class Aplikasi:
    """Alur utama program."""
    
    def menu_lihat_data(data):
        Tampilan.judul("DATA SEREAL (per 100 gram)")
        print(f"Jumlah produk valid: {len(data)}\n")
        ukuran = 15
        halaman = (len(data) - 1) // ukuran + 1
        for h in range(halaman):
            Tampilan.cetak_tabel(data[h * ukuran:(h + 1) * ukuran], TABEL, h * ukuran + 1)
            print(f"\nHalaman {h + 1}/{halaman}")
            if h + 1 < halaman and input(
                    "ENTER = halaman berikutnya, Q = kembali: ").strip().lower() == "q":
                break
        Tampilan.tunggu()

    
    def main():
        if not Autentikasi.login():
            return
        data = RepositoriSereal.muat_data(FILE_CSV)
        while True:
            Tampilan.judul("MENU UTAMA")
            for no, (nama, _) in MENU.items():
                print(f"  {no}. {nama}")
            print("  5. Keluar")
            pilihan = Tampilan.minta_angka("\nPilih menu (1-5): ", 1, 5)
            if pilihan == 5:
                return print("\nTerima kasih. Program selesai.")
            MENU[pilihan][1](data)


MENU = {
    1: ("Lihat Data Sereal", Aplikasi.menu_lihat_data),
    2: ("Pemeriksaan Kandungan Gizi", PemeriksaanGizi.menu_pemeriksaan),
    3: ("Rekomendasi Sereal (Top 5 AHP-SAW)", Rekomendasi.menu_rekomendasi),
    4: ("Perbandingan Dua Produk", Perbandingan.menu_perbandingan),
}


if __name__ == "__main__":
    Aplikasi.main()