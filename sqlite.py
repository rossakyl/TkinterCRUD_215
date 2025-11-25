# Aplikasi prediksi fakultas berdarkan nilai siswa menggunakan Tkinter (GUI) dan SQLITE (Database)
# Fitur : submit, update, delete, prediksi otomatis

import sqlite3
import tkinter as tk
import tkinter.messagebox as msg
from tkinter import ttk

# KONEKSI DATABASE 
def koneksi():
    return sqlite3.connect("nilai2.db")

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

# UPDATE DATA DI DATABASE
def update_nilai(id_data, nama, bio, fis, ing, prediksi):
    con = koneksi()
    cur = con.cursor()
    cur.execute("""
        UPDATE nilai_siswa
        SET nama_siswa=?, biologi=?, fisika=?, inggris=?, prediksi_fakultas=?
        WHERE id=?
    """, (nama, bio, fis, ing, prediksi, id_data))
    con.commit()
    con.close()

# DELETE DATA DARI DATABASE
def delete_nilai(id_data):
    con = koneksi()
    cur = con.cursor()
    cur.execute("DELETE FROM nilai_siswa WHERE id=?", (id_data,))
    con.commit()
    con.close()

# GUI TKINTER
class NilaiSiswa(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Prediksi Fakultas Berdasarkan Nilai")
        self.geometry("700x500")
        self.configure(bg="#f0f2f5")

        self.selected_id = None

        frame = tk.Frame(self, bg="white", padx=10, pady=10)
        frame.pack(padx=10, pady=10, fill="x")

        # input nama
        tk.Label(frame, text="Nama Siswa:", bg="white").grid(row=0, column=0, sticky="w")
        self.ent_nama = tk.Entry(frame, width=30)
        self.ent_nama.grid(row=0, column=1, pady=5)

        # input nilai biologi
        tk.Label(frame, text="Nilai Biologi:", bg="white").grid(row=1, column=0, sticky="w")
        self.ent_biologi = tk.Entry(frame, width=30)
        self.ent_biologi.grid(row=1, column=1, pady=5)

        # input nilai fisika
        tk.Label(frame, text="Nilai Fisika:", bg="white").grid(row=2, column=0, sticky="w")
        self.ent_fisika = tk.Entry(frame, width=30)
        self.ent_fisika.grid(row=2, column=1, pady=5)

        # input nilai inggris
        tk.Label(frame, text="Nilai Inggris:", bg="white").grid(row=3, column=0, sticky="w")
        self.ent_inggris = tk.Entry(frame, width=30)
        self.ent_inggris.grid(row=3, column=1, pady=5)

        # Tombol submit
        self.btn_submit = tk.Button(frame, text="Submit", bg="lightblue", width=15, command=self.submit_data)
        self.btn_submit.grid(row=4, column=0, pady=10)

        # Tombol update
        self.btn_update = tk.Button(frame, text="Update", bg="red", width=15, command=self.update_data)
        self.btn_update.grid(row=4, column=1, pady=10)

        # Tombol delete
        self.btn_delete = tk.Button(frame, text="Delete", bg="orange", width=15, command=self.delete_data)
        self.btn_delete.grid(row=5, column=0, columnspan=2, pady=5)

        # Tabel hasil
        self.tree = ttk.Treeview(self, columns=("id", "nama", "bio", "fis", "ing", "pred"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("nama", text="Nama")
        self.tree.heading("bio", text="Biologi")
        self.tree.heading("fis", text="Fisika")
        self.tree.heading("ing", text="Inggris")
        self.tree.heading("pred", text="Prediksi Fakultas")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        # ====== ATUR LEBAR KOLOM AGAR TIDAK TERPOTONG ======
        self.tree.column("id", width=40, anchor="center", stretch=False)
        self.tree.column("nama", width=120, anchor="w", stretch=False)
        self.tree.column("bio", width=80, anchor="center", stretch=False)
        self.tree.column("fis", width=80, anchor="center", stretch=False)
        self.tree.column("ing", width=80, anchor="center", stretch=False)
        self.tree.column("pred", width=130, anchor="w", stretch=True)


        self.tree.bind("<ButtonRelease-1>", self.select_data)

        self.load_data()

    # validasi input
    def validate(self):
        nama = self.ent_nama.get().strip()
        bio = self.ent_biologi.get().strip()
        fis = self.ent_fisika.get().strip()
        ing = self.ent_inggris.get().strip()

        if not nama or not bio or not fis or not ing:
            msg.showwarning("Peringatan", "Semua input wajib diisi!")
            return None

        try:
            return nama, int(bio), int(fis), int(ing)
        except:
            msg.showerror("Error", "Nilai harus berupa angka!")
            return None

    # prediksi fakultas
    def prediksi_fakultas(self, bio, fis, ing):
        nilai_tertinggi = max(bio, fis, ing)
        if nilai_tertinggi == bio:
            return "Kedokteran"
        elif nilai_tertinggi == fis:
            return "Teknik"
        else:
            return "Bahasa"

    # submit data
    def submit_data(self):
        data = self.validate()
        if not data:
            return

        nama, bio, fis, ing = data
        prediksi = self.prediksi_fakultas(bio, fis, ing)
        insert_nilai(nama, bio, fis, ing, prediksi)
        msg.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi: {prediksi}")
        self.load_data()
        self.clear_input()

    # select data dari tabel
    def select_data(self, event):
        selected = self.tree.focus()
        if not selected:
            return
        values = self.tree.item(selected, 'values')
        self.selected_id = values[0]

        self.ent_nama.delete(0, tk.END)
        self.ent_nama.insert(0, values[1])
        self.ent_biologi.delete(0, tk.END)
        self.ent_biologi.insert(0, values[2])
        self.ent_fisika.delete(0, tk.END)
        self.ent_fisika.insert(0, values[3])
        self.ent_inggris.delete(0, tk.END)
        self.ent_inggris.insert(0, values[4])

    # UPDATE DATA
    # FUNGSI : Memperbarui data yang dipilih di database
    # alur   : Data dipilih → fungsi update_data dipanggil → data diperbarui di database → tabel diperbarui.
    def update_data(self):
        if not self.selected_id:
            msg.showwarning("Peringatan", "Pilih data terlebih dahulu!")
            return

        data = self.validate()
        if not data:
            return

        nama, bio, fis, ing = data
        prediksi = self.prediksi_fakultas(bio, fis, ing)
        update_nilai(self.selected_id, nama, bio, fis, ing, prediksi)
        msg.showinfo("Sukses", "Data berhasil diupdate")
        self.load_data()
        self.clear_input()

    # DELETE DATA
    # FUNGSI : Menghapus data yang dipilih dari database
    # alur   : Data dipilih → fungsi delete_data dipanggil → data dihapus dari database → tabel diperbarui.
    def delete_data(self):
        if not self.selected_id:
            msg.showwarning("Peringatan", "Pilih data yang akan dihapus!")
            return

        if msg.askyesno("Konfirmasi", "Yakin ingin menghapus data ini?"):
            delete_nilai(self.selected_id)
            msg.showinfo("Sukses", "Data berhasil dihapus")
            self.load_data()
            self.clear_input()

    # LOAD DATA KE TABEL
    # FUNGSI : Memanggil data di database
    # alur   : Data di database berubah → fungsi load data dipanggil → tabel diperbarui sesuai isi database saat ini.
    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        con = koneksi()
        cur = con.cursor()
        cur.execute("SELECT id, nama_siswa, biologi, fisika, inggris, prediksi_fakultas FROM nilai_siswa")
        for r in cur.fetchall():
            self.tree.insert("", tk.END, values=r)
        con.close()

    # CLEAR INPUT 
    # FUNGSI : Membersihkan inputan di form setelah data disubmit atau diupdate
    # alur   : Setelah data disubmit atau diupdate → fungsi clear_input dipanggil → semua field input dikosongkan untuk input baru.
    def clear_input(self):
        self.ent_nama.delete(0, tk.END)
        self.ent_biologi.delete(0, tk.END)
        self.ent_fisika.delete(0, tk.END)
        self.ent_inggris.delete(0, tk.END)
        self.selected_id = None


# JALANKAN PROGRAM
if __name__ == "__main__":
    app = NilaiSiswa()
    app.mainloop()
