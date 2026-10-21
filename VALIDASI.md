# Pemeriksaan pembaruan peta — 21 Oktober 2026

Basis: repositori `https://github.com/R34gen/dashboard-datmin`, commit `fb0456f50ff3a76d86dd745ad153ca1a4587f1d6`. Peta diintegrasikan ke versi HTML dan Streamlit pada proyek ini.

## Hasil pembaruan

- CSV GitHub identik byte demi byte dengan CSV unggahan. CSV, empat database, sumber Excel, notebook, dan fungsi analisis utama tidak diubah.
- 38 wilayah indikator cocok satu-ke-satu dengan 38 fitur GeoJSON unggahan; tidak ada nama yang hilang.
- Total tetap 25.521 sekolah, 294.886 guru, dan 4.282.023 murid.
- `node scripts/verify_web.cjs` lulus: perhitungan awal, filter, data kosong, perbandingan, reset, presentasi lima bagian, unduhan, serta peta menurut indikator/jenjang/jenis wilayah/IPM.
- `python scripts/verify_streamlit.py` lulus: data DuckDB lokal, KPI, 38 penanda, sembilan kota, pilihan murid SMA, popup Kota Surabaya, pewarnaan IPM, dan filter kosong. Surabaya memuat 57.135 murid SMA, 3.359 guru SMA, dan 139 sekolah SMA.
- Browser Chromium 134 berhasil membuka `index.html` dalam mode offline: peta, popup, zoom, filter, dan mode presentasi berfungsi tanpa error JavaScript pada skenario uji.
- Tampilan desktop 1440 piksel dan ponsel 390 piksel diperiksa. Peta ponsel menampilkan 38 penanda yang digabung sesuai zoom dan tidak menyebabkan luapan horizontal halaman.
- Server Streamlit dijalankan dan diperiksa melalui browser nyata: iframe peta, 38 penanda, dan kontrol zoom berhasil tampil.
- Sintaks Python diperiksa memakai grammar Python 3.10. Runtime pengujian: Python 3.12, Streamlit 1.55.0, DuckDB 1.5.6, Plotly 6.9.0. Eksekusi langsung Python 3.10/Windows belum diuji.
- Builder web memakai UTF-8 secara eksplisit untuk menjaga teks saat dijalankan di Windows.

## Batas verifikasi pembaruan

Koneksi MotherDuck, publikasi ulang ke GitHub/hosting, dan ketersediaan layanan peta dasar OpenStreetMap belum diuji. Batas dan penanda offline sudah diuji. Atribusi geometri mengikuti dokumentasi unggahan; tidak dilakukan verifikasi ulang batas administratif atau publikasi angka BPS. Perubahan belum didorong ke repositori jarak jauh.

---

## Catatan validasi versi dasar

### Pemeriksaan hasil

Tanggal: 14 Oktober 2026.

## Lulus

- CSV terintegrasi direkonsiliasi ulang terhadap seluruh nilai dalam tiga Excel. Hasil cocok persis setelah tahun integrasi 2025 ditambahkan sesuai notebook. Join one-to-one berhasil.
- 38 wilayah unik, 29 kabupaten dan 9 kota, tanpa nilai kosong atau baris duplikat.
- Total sekolah 25.521, guru 294.886, dan murid 4.282.023. Total per jenjang juga diperiksa.
- Rata-rata IPM 76,06447368421051, RLS 8,941315789473686, dan korelasi Pearson 0,97963430749045 cocok dengan perhitungan Python dan output notebook.
- Penghitungan JavaScript diuji terhadap total dan statistik referensi. Rasio gabungan memakai total murid dibagi total guru.
- Model DOM memeriksa perubahan filter, hasil kosong, reset, batas rentang IPM, perbandingan independen dari filter, pilihan daerah yang sama, navigasi tab dan presentasi, serta jalur unduh CSV.
- JavaScript lolos pemeriksaan syntax Node. app.py dan builder lolos pemeriksaan syntax Python.
- Dataset di index.html disematkan dan sama dengan CSV. Tidak ada dependensi aset eksternal untuk membuka versi web.

## Batas verifikasi

Layout, rendering SVG/CSS, dan interaksi pada browser nyata belum diuji di lingkungan ini. Tes model DOM memeriksa logika UI, bukan tampilan aktual atau perilaku browser secara menyeluruh.

UI Streamlit belum dijalankan karena paket Streamlit tidak tersedia di lingkungan pemeriksaan. Koneksi MotherDuck, ekstensi DuckLake, serta eksekusi ulang seluruh notebook tidak diuji. Publikasi GitHub/Pages belum dilakukan. URL tabel sumber dan tahun asli data pendidikan belum diverifikasi.

## Pembaruan database fisik

DuckDB 1.4.1 tersedia dalam lingkungan pemeriksaan terpisah. Tiga database sumber dan satu warehouse gabungan berhasil dibuat dari Excel. Semua file ditutup, dibuka ulang read-only, dan tabel serta jumlah barisnya diperiksa. View warehouse cocok dengan CSV pada seluruh 13 kolom dan 38 baris. SHA-256 dan daftar tabel tersimpan dalam database/manifest.json. Database fisik disertakan, bukan file kosong atau hasil mengganti ekstensi.

Fungsi pembacaan data aktual pada app.py diuji dengan DuckDB lokal, tanpa menjalankan UI Streamlit. Hasilnya 38 wilayah dengan total yang sesuai.

Untuk pengecekan akhir di perangkat demonstrasi: buka index.html, pilih Kota, pilih SD, cari Surabaya, klik Mode presentasi, pindah bagian, bandingkan dua daerah, dan unduh CSV. Coba juga pada layar proyektor atau monitor fakultas.
