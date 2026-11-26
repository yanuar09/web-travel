# NusaShuttle - Konsol Pemesanan Tiket & Kursi Travel

Aplikasi sistem pemesanan tiket travel antarkota (Bandung - Jakarta) dengan 3 tahapan (wizard):
1. **Rute & Jadwal**: Filter koridor, tanggal, kelas armada, serta daftar jadwal keberangkatan (`JAD-01`, `JAD-02`, `JAD-03`).
2. **Pilih Kursi & Kuota**: Denah interaktif armada shuttle (HiAce Premio 14 kursi), validasi batas kuota transaksi (maksimal 4 kursi), dan estimasi tarif.
3. **Penumpang & Tarif**: Input data penumpang, pilihan kategori tiket (Dewasa, Pelajar diskon 15%, Lansia diskon 20%), kalkulasi rincian tarif, biaya layanan loket (Rp 5.000), total pembayaran (Rp 282.500), serta fitur **Cetak Tiket**.

---

## Pilihan Menjalankan Aplikasi

Tersedia **2 opsi implementasi Python**:

### Opsi 1: Versi Web (Flask + HTML/CSS/JS) - *Rekomendasi (Tampilan Persis Screenshot)*
1. Pastikan dependensi terpasang:
   ```bash
   pip install flask
   ```
2. Jalankan server:
   ```bash
   python app.py
   ```
3. Buka browser di alamat:
   [http://localhost:5000](http://localhost:5000)

### Opsi 2: Versi Desktop GUI (Python Tkinter)
Dapat langsung dijalankan di sistem operasi Windows tanpa server:
```bash
python app_gui.py
```

---

## Struktur File Proyek

```
web_travel/
├── app.py                # Backend Web Flask & API perhitungan tarif
├── app_gui.py            # Aplikasi GUI Desktop berbasis Tkinter
├── templates/
│   └── index.html        # Antarmuka web 3 tahap (Rute, Kursi, Penumpang)
├── static/
│   ├── css/
│   │   └── style.css     # Styling palet warna warm beige & dark brown
│   └── js/
│       └── main.js       # Logika interaktif denah kursi, kuota, & kalkulasi
└── README.md
```

