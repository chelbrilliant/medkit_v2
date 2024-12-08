import csv
import os
import pyfiglet
from tabulate import tabulate

# Fungsi untuk signup
def signup():
    role = input("\nMasukkan peran (admin/user): ").strip().lower()

    if role == "admin":
        kode_admin = input("Masukkan kode admin: ").strip()
        if kode_admin != "AdminXMedTan":
            print("Kode admin salah. Anda tidak dapat mendaftar sebagai admin.")
            return

    username = input("Masukkan username baru: ").strip()
    password = input("Masukkan password baru: ").strip()

    if role not in ["admin", "user"]:
        print("Peran tidak valid. Masukkan 'admin' atau 'user'.")
        return

    if username == () or password == ():
        print("Masukkan username atau password baru anda terlebih dahulu")
        return

    try:
        with open("users.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Username"] == username:
                    print("Username sudah ada. Coba lagi.")
                    return
    except FileNotFoundError:
        pass

    with open("users.csv", "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["Username", "Password", "Role"])
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow({"Username": username, "Password": password, "Role": role})
        print("Signup berhasil! Silakan login.")

# Fungsi untuk login
def login():
    username = input("\nMasukkan username: ").strip()
    password = input("Masukkan password: ").strip()

    try:
        with open("users.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Username"] == username and row["Password"] == password:
                    print(f"Login berhasil sebagai {row['Role']}!")
                    if row["Role"] == "admin":
                        menu_admin()
                    elif row["Role"] == "user":
                        menu_user(username)
                    return
        print("Username atau password salah.")
    except FileNotFoundError:
        print("Belum ada pengguna terdaftar. Silakan signup terlebih dahulu.")

# Fungsi untuk melihat produk
def lihat_produk():
    try:
        with open("produk.csv", "r") as file:
            reader = csv.DictReader(file)
            produk = list(reader)

        if not produk:
            print("Belum ada produk yang tersedia.")
            return

        # Header tabel
        header = ["Kode", "Nama", "Harga (Rp)", "Stok", "Manfaat"]

        # Data untuk tabel
        data = [[row["Kode"], row["Nama"], row["Harga"], row["Stok"], row["Manfaat"]] for row in produk]

        # Menampilkan tabel
        print("\n=== Daftar Produk ===")
        print(tabulate(data, headers=header, tablefmt="fancy_grid"))  # Menggunakan format 'fancy_grid'
    except FileNotFoundError:
        print("Belum ada produk yang tersedia.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

# Fungsi untuk menambah obat (admin)
def tambah_obat():
    kode = input("Masukkan kode obat: ").strip()

    # Cek apakah kode obat sudah ada
    try:
        with open("produk.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Kode"] == kode:
                    print("Kode obat sudah ada. Gunakan kode lain.")
                    return
    except FileNotFoundError:
        pass

    nama = input("Masukkan nama obat: ").strip()
    harga = input("Masukkan harga obat: ").strip()
    stok = input("Masukkan stok obat: ").strip()
    manfaat = input("Masukkan manfaat obat: ").strip()

    try:
        with open("produk.csv", "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Kode", "Nama", "Harga", "Stok", "Manfaat"])
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow({"Kode": kode, "Nama": nama, "Harga": harga, "Stok": stok, "Manfaat": manfaat})
            print("Obat berhasil ditambahkan!")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")


# Fungsi untuk menghapus obat (admin)
def hapus_obat():
    try:
        with open("produk.csv", "r") as file:
            reader = csv.DictReader(file)
            produk = list(reader)

        kode = input("Masukkan kode obat yang ingin dihapus: ").strip()
        produk_baru = [p for p in produk if p["Kode"] != kode]

        if len(produk_baru) < len(produk):
            with open("produk.csv", "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["Kode", "Nama", "Harga", "Stok", "Manfaat"])
                writer.writeheader()
                writer.writerows(produk_baru)
            print(f"Obat dengan kode '{kode}' berhasil dihapus.")
        else:
            print(f"Obat dengan kode '{kode}' tidak ditemukan.")
    except FileNotFoundError:
        print("Database obat belum tersedia.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

# Fungsi untuk transaksi pembelian obat (user)

def transaksi(username):
    keranjang = []  # Untuk menampung item belanja sementara
    lihat_produk()

    while True:
        print("\n1. Tambah ke keranjang")
        print("2. Lihat keranjang")
        print("3. Hapus dari keranjang")
        print("4. Lanjut ke pembayaran")
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            # Tambahkan ke keranjang
            kode = input("Masukkan kode obat yang dibeli: ").strip()

            while True:
                try:
                    jumlah = int(input("Masukkan jumlah yang dibeli: ").strip())
                    if jumlah <= 0:
                        print("Perlu memesan minimal 1 item produk untuk melanjutkan pembelian.")
                        continue
                    break
                except ValueError:
                    print("Perlu memesan minimal 1 item produk untuk melanjutkan pembelian.")
                    print("Mohon masukkan jumlah pemesanan yang sesuai.")

            try:
                with open("produk.csv", "r") as file:
                    reader = csv.DictReader(file)
                    produk = list(reader)

                for item in produk:
                    if item["Kode"] == kode:
                        if int(item["Stok"]) >= jumlah:
                            keranjang.append({
                                "Kode": kode,
                                "Nama": item["Nama"],
                                "Harga": int(item["Harga"]),
                                "Jumlah": jumlah,
                                "Subtotal": int(item["Harga"]) * jumlah
                            })
                            print(f"{item['Nama']} sebanyak {jumlah} berhasil ditambahkan ke keranjang.")
                        else:
                            print("Stok tidak mencukupi.")
                        break
                else:
                    print("Kode obat tidak ditemukan.")
            except FileNotFoundError:
                print("Database obat belum tersedia.")
            except Exception as e:
                print(f"Terjadi kesalahan: {e}")

        elif pilihan == "2":
            # Lihat keranjang
            print("\n=== Keranjang Belanja ===")
            if keranjang:
                
                # Header tabel
                header = ["No", "Nama", "Harga (Rp)", "Jumlah", "Subtotal (Rp)"]

                # Data tabel dengan nomor urut
                data = [
                    [i + 1, item["Nama"], item["Harga"], item["Jumlah"], item["Subtotal"]]
                    for i, item in enumerate(keranjang)
                ]

                # Menampilkan tabel keranjang belanja
                print(tabulate(data, headers=header, tablefmt="fancy_grid"))
            else:
                print("Keranjang masih kosong.")

        elif pilihan == "3":
            # Hapus item dari keranjang
            print("\n=== Keranjang Belanja ===")
            if keranjang:
                # Header tabel
                header = ["No", "Nama", "Harga (Rp)", "Jumlah", "Subtotal (Rp)"]

                # Data tabel dengan nomor urut
                data = [
                    [i + 1, item["Nama"], item["Harga"], item["Jumlah"], item["Subtotal"]]
                    for i, item in enumerate(keranjang)
                ]

                # Menampilkan tabel keranjang belanja
                print(tabulate(data, headers=header, tablefmt="fancy_grid"))
                
                try:
                    # Meminta input nomor item yang ingin dihapus
                    hapus_keranjang = int(input("Masukkan nomor item yang ingin dihapus: ").strip()) - 1
                    
                    # Validasi apakah nomor yang dimasukkan sesuai dengan indeks daftar keranjang
                    if 0 <= hapus_keranjang < len(keranjang):
                        item_dihapus = keranjang.pop(hapus_keranjang)
                        print(f"{item_dihapus['Nama']} berhasil dihapus dari keranjang.")
                    else:
                        print("Nomor item tidak valid. Pilih nomor dari daftar.")
                except ValueError:
                    print("Masukkan nomor yang valid.")
            else:
                print("Keranjang masih kosong.")

        elif pilihan == "4":
            # Lanjut ke pembayaran
            if not keranjang:
                print("Keranjang masih kosong. Tambahkan produk terlebih dahulu.")
                continue

            print("\n=== Konfirmasi Pembayaran ===")
            total_belanja = sum(item["Subtotal"] for item in keranjang)
            print(f"Total yang harus dibayar: Rp{total_belanja}")

            while True:
                try:
                    uang_dibayar = int(input("Masukkan jumlah uang yang dibayarkan: Rp").strip())
                    if uang_dibayar < total_belanja:
                        print("Uang yang dibayarkan tidak cukup.")
                        continue
                    break
                except ValueError:
                    print("Masukkan jumlah uang dalam angka.")

            kembalian = uang_dibayar - total_belanja
            print(f"Pembayaran berhasil. Kembalian: Rp{kembalian}")

            # Update stok di produk.csv
            try:
                with open("produk.csv", "r") as file:
                    reader = csv.DictReader(file)
                    produk = list(reader)

                for item in keranjang:
                    for p in produk:
                        if p["Kode"] == item["Kode"]:
                            p["Stok"] = str(int(p["Stok"]) - item["Jumlah"])

                with open("produk.csv", "w", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=["Kode", "Nama", "Harga", "Stok", "Manfaat"])
                    writer.writeheader()
                    writer.writerows(produk)

                # Catat transaksi ke transaksi.csv
                with open("transaksi.csv", "a", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=["Username", "Kode", "Nama", "Jumlah", "Total", "Pembayaran", "Kembalian"])
                    if file.tell() == 0:
                        writer.writeheader()
                    for item in keranjang:
                        writer.writerow({
                            "Username": username,
                            "Kode": item["Kode"],
                            "Nama": item["Nama"],
                            "Jumlah": item["Jumlah"],
                            "Total": item["Subtotal"],
                            "Pembayaran": uang_dibayar,
                            "Kembalian": kembalian
                        })

                print("Transaksi berhasil disimpan.")
            except FileNotFoundError:
                print("Database obat belum tersedia.")
            except Exception as e:
                print(f"Terjadi kesalahan: {e}")
            return

        else:
            print("Pilihan tidak valid. Coba lagi.")


# Fungsi untuk melihat history transaksi (admin)
def lihat_history():
    try:
        with open("transaksi.csv", "r") as file:
            reader = csv.DictReader(file)
            print("\n=== History Transaksi ===")
            for row in reader:
                print(f"Username: {row['Username']}, Obat: {row['Nama']}, Jumlah: {row['Jumlah']}, Total: Rp{row['Total']}")
    except FileNotFoundError:
        print("Belum ada transaksi yang tercatat.")

# Menu untuk admin
def menu_admin():
    while True:
        print("\n=== Menu Admin ===")
        print("1. Lihat Produk")
        print("2. Tambah Obat")
        print("3. Hapus Obat")
        print("4. Lihat History Transaksi")
        print("5. Logout")
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            lihat_produk()
        elif pilihan == "2":
            tambah_obat()
        elif pilihan == "3":
            hapus_obat()
        elif pilihan == "4":
            lihat_history()
        elif pilihan == "5":
            print("Logout berhasil!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

# Menu untuk user
def menu_user(username):
    while True:
        print("\n=== Menu User ===")
        print("1. Lihat Produk")
        print("2. Transaksi")
        print("3. Logout")
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            lihat_produk()
        elif pilihan == "2":
            transaksi(username)
        elif pilihan == "3":
            print("Logout berhasil!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

# Menu utama
def menu_utama():
    while True:
        judul = pyfiglet.figlet_format("   MEDKIT", font="blocky")
        judul2 = pyfiglet.figlet_format("TANAMAN", font="blocky")
        print( )
        print(judul)
        print(judul2)
        print("====================================================================")
        print("               -Solusi Kesehatan untuk Tanaman Anda-")
        print("====================================================================\n")
        print("+++++++++++++++++++++++++++ MENU UTAMA +++++++++++++++++++++++++++++\n")
        print("                             1. Login")
        print("                             2. Signup")
        print("                             3. Keluar\n")
        pilihan = input("                            Pilih menu: ").strip()\

        if pilihan == "1":
            login()
        elif pilihan == "2":
            signup()
        elif pilihan == "3":
            print("\nTerima kasih telah mengunjungi MEDKIT TANAMAN!")
            break
        else:
            print("\nPilihan tidak valid. Silakan coba lagi.")

# Membuat file CSV jika belum ada
def buat_file_csv():
    # Cek dan buat file users.csv
    if not os.path.exists("users.csv"):
        with open("users.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Username", "Password", "Role"])
            writer.writeheader()
        print("File users.csv berhasil dibuat.")

    # Cek dan buat file produk.csv
    if not os.path.exists("produk.csv"):
        with open("produk.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Kode", "Nama", "Harga", "Stok", "Manfaat"])
            writer.writeheader()
        print("File produk.csv berhasil dibuat.")

    # Cek dan buat file transaksi.csv
    if not os.path.exists("transaksi.csv"):
        with open("transaksi.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Username", "Kode", "Nama", "Jumlah", "Total"])
            writer.writeheader()
        print("File transaksi.csv berhasil dibuat.")


# Menjalankan aplikasi
buat_file_csv() # Memastikan file CSV tersedia
menu_utama()