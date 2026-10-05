# cionejr

Skill ilustrasi eksperimental untuk agen coding. Mulai dari bentuk dasar, lihat hasilnya, lalu perbaiki pengerjaan sebelum memilih gaya.

[English](README.md) · [SKILL.md](skills/cionejr/SKILL.md)

![Studi ilustrasi hutan](examples/forest-gathering/preview.png)

## Cara pakai

Berikan `skills/cionejr/SKILL.md` kepada agen. Jika host mendukung penemuan skill, salin seluruh folder `skills/cionejr` ke lokasi skill yang dikonfigurasi host. Jangan memisahkan referensi dan template dari entry file.

Clone repo tidak otomatis mengaktifkan skill. Proyek ini tidak mengubah pengaturan global.

Contoh permintaan:

> Gunakan cionejr. Buat burung dari referensi ini, periksa sambungan kepala dan badan sebelum bulu.

> Buat satu halaman penuh hewan berkumpul di hutan tanpa teks. Buka layout sebelum detail dan periksa kontak setiap karakter.

> Buat beberapa pendekatan gaya. Perbaiki craft masing-masing dulu, jangan bandingkan hasil rapi dengan alternatif yang belum benar.

## Isi

Panduan mencakup konstruksi lintas skala, karakter dan komunikasi, serta staging adegan penuh. Ada worksheet kritik dan spesifikasi kasus evaluasi. Contoh Python dapat dijalankan ulang dengan Pillow dan NumPy; bukan mesin yang otomatis menggambar semua subjek.

## Menjalankan contoh

Python 3.10+:

```bash
python -m pip install -r requirements.txt
python tools/validate_skill.py
python -m unittest discover -s tests -v
python examples/bird-styles/render.py
python examples/bird-styles/test_outputs.py
python examples/forest-gathering/render.py --layout
python examples/forest-gathering/render.py
python examples/forest-gathering/test_outputs.py
```

Renderer menimpa PNG contoh di foldernya sendiri. Salin versi sebelumnya jika ingin menyimpan revisi. Perbedaan font label dapat mengubah piksel teks antar mesin.

## Status

Versi 0.1.0 masih eksperimental. Halaman hutan dinilai cukup sebagai contoh awal, tetapi masih perlu dirapikan. [Roadmap](docs/roadmap.md) mencatat pekerjaan lanjut; penerbitan repo tidak berarti gambarnya sudah sempurna.

Test file dan validasi dokumen bukan sertifikasi anatomi atau pemahaman penonton. Kasus evaluasi perilaku belum menjadi benchmark yang lulus. Tidak ada plugin editor atau model gambar di paket ini.

Kode, instruksi, dokumentasi, dan PNG original memakai [lisensi MIT](LICENSE). Sumber pihak lain yang hanya dirujuk tetap punya hak masing-masing. Baca [catatan contoh](docs/examples.md) dan [atribusi](docs/attribution.md).
