import sqlite3
import tkinter as tk
import tkinter.messagebox as msg
from tkinter import ttk

# KONEKSI DATABASE
def koneksi():
    return sqlite3.connect("nilai.db")

def create_table():
    con = koneksi()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT NOT NULL,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    """)
    con.commit()
    con.close()

create_table()

# SIMPAN DATA KE DATABASE
def insert_nilai(nama, bio, fis, ing, prediksi):
    con = koneksi()
    cur = con.cursor()
    cur.execute("""
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, bio, fis, ing, prediksi))
    con.commit()
    con.close()

# GUI TKINTER
class NilaiSiswa(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Prediksi Fakultas Berdasarkan Nilai")
        self.geometry("500x420")
        self.configure(bg="#f0f2f5")

        frame = tk.Frame(self, bg="white", padx=10, pady=10)
        frame.pack(padx=10, pady=10, fill="x")

        # Input Nama
        tk.Label(frame, text="Nama Siswa:", bg="white").grid(row=0, column=0, sticky="w")
        self.ent_nama = tk.Entry(frame, width=30)
        self.ent_nama.grid(row=0, column=1, pady=5)

        # Input Nilai Biologi
        tk.Label(frame, text="Nilai Biologi:", bg="white").grid(row=1, column=0, sticky="w")
        self.ent_biologi = tk.Entry(frame, width=30)
        self.ent_biologi.grid(row=1, column=1, pady=5)

        # Input Nilai Fisika
        tk.Label(frame, text="Nilai Fisika:", bg="white").grid(row=2, column=0, sticky="w")
        self.ent_fisika = tk.Entry(frame, width=30)
        self.ent_fisika.grid(row=2, column=1, pady=5)

        # Input Nilai Inggris
        tk.Label(frame, text="Nilai Inggris:", bg="white").grid(row=3, column=0, sticky="w")
        self.ent_inggris = tk.Entry(frame, width=30)
        self.ent_inggris.grid(row=3, column=1, pady=5)

        # Tombol Submit
        self.btn_submit = tk.Button(frame, text="Submit", width=20, command=self.submit_data)
        self.btn_submit.grid(row=4, column=0, columnspan=2, pady=10)

        # Tabel Hasil
        self.tree = ttk.Treeview(self, columns=("nama", "bio", "fis", "ing", "pred"), show="headings")
        self.tree.heading("nama", text="Nama")
        self.tree.heading("bio", text="Biologi")
        self.tree.heading("fis", text="Fisika")
        self.tree.heading("ing", text="Inggris")
        self.tree.heading("pred", text="Prediksi Fakultas")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        self.load_data()

   
    # Validasi Input
    def validate(self):
        nama = self.ent_nama.get().strip()
        bio = self.ent_biologi.get().strip()
        fis = self.ent_fisika.get().strip()
        ing = self.ent_inggris.get().strip()

        if not nama or not bio or not fis or not ing:
            msg.showwarning("Peringatan", "Semua input wajib diisi!")
            return None

        try:
            bio = int(bio)
            fis = int(fis)
            ing = int(ing)
        except:
            msg.showerror("Error", "Nilai harus berupa angka!")
            return None

        return nama, bio, fis, ing

    # Prediksi Fakultas
    def prediksi_fakultas(self, bio, fis, ing):
        nilai_tertinggi = max(bio, fis, ing)

        if nilai_tertinggi == bio:
            return "Kedokteran"
        elif nilai_tertinggi == fis:
            return "Teknik"
        else:
            return "Bahasa"

    # Submit Data
    def submit_data(self):
        data = self.validate()
        if not data:
            return

        nama, bio, fis, ing = data
        prediksi = self.prediksi_fakultas(bio, fis, ing)

        insert_nilai(nama, bio, fis, ing, prediksi)

        msg.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")

        self.load_data()

        # Clear input
        self.ent_nama.delete(0, tk.END)
        self.ent_biologi.delete(0, tk.END)
        self.ent_fisika.delete(0, tk.END)
        self.ent_inggris.delete(0, tk.END)

    # Tampilkan Data ke Treeview
    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        con = koneksi()
        cur = con.cursor()
        cur.execute("SELECT nama_siswa, biologi, fisika, inggris, prediksi_fakultas FROM nilai_siswa")
        rows = cur.fetchall()
        con.close()

        for r in rows:
            self.tree.insert("", tk.END, values=r)


# JALANKAN PROGRAM
if __name__ == "__main__":
    app = NilaiSiswa()
    app.mainloop()