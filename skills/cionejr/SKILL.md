---
name: cionejr
description: >-
  Construct and critique drawings, illustrations, characters, and graphic compositions from basic shapes across scales. Use for sketching, drawing from references, geometric illustration, feather or material detail, visual storytelling, style translation, and contextual taste decisions. Enforce style-specific craft checks before comparing alternatives. Indonesian triggers include menggambar, bentuk dasar, sketsa, bulu, karakter, gaya ilustrasi, komunikasi visual, dan taste.
license: MIT
metadata:
  version: "0.1.0"
  status: "experimental"
---

# cionejr

Skill konstruksi ilustrasi, dari bentuk dasar ke adegan dan makna.

Bangun gambar yang sesuai tujuan. Gunakan lingkaran, persegi, dan segitiga sebagai alat memahami struktur, bukan bentuk akhir yang wajib dipertahankan. Setiap pilihan gaya harus dikerjakan dengan baik menurut tuntutan gayanya sebelum dibandingkan.

Skill ini memberi prosedur kerja. Ia tidak menjamin kemampuan menggambar, hasil sempurna, atau peningkatan kualitas model. Jangan menyatakan kelulusan hanya karena semua kotak checklist terisi.

## Mulai dari permintaan yang sebenarnya

- Jika diminta meneliti, mengkritik, atau menyusun skill, kerjakan itu. Jangan otomatis membuat gambar.
- Jika diminta menggambar atau memperbaiki gambar, gunakan alur di bawah.
- Jika diminta membandingkan gaya, periksa craft setiap kandidat lebih dulu.
- Jika diminta belajar, pakai latihan pada [panduan konstruksi](references/construction.md). Kritik satu kemampuan sebelum menambah kesulitan.
- Jika diminta plugin, pisahkan metodologi dari implementasi. Host dan cara mengedit hasil harus diketahui sebelum membuat integrasi.

Baca referensi relatif terhadap folder skill ini. Jangan menganggap akses internet, editor grafis, atau model gambar selalu tersedia.

## Dokumen pendamping

| Kebutuhan | Baca sebelum bekerja |
|---|---|
| Menggambar atau menjelaskan konstruksi | [construction.md](references/construction.md) |
| Memeriksa atau memperbaiki hasil | [craft-review.md](references/craft-review.md) |
| Gaya, karakter, komposisi, atau taste | [communication-and-style.md](references/communication-and-style.md) |
| Adegan penuh, banyak karakter, atau halaman buku cerita | [scene-staging.md](references/scene-staging.md) |
| Mengutip metode atau menambah riset | [sources-and-limits.md](references/sources-and-limits.md) |
| Menyimpan brief dan hasil kritik | [worksheet.md](templates/worksheet.md) |
| Menguji perilaku skill | [cases.md](evaluations/cases.md) |

Untuk pekerjaan visual lengkap, baca panduan konstruksi, craft, dan komunikasi. Untuk adegan penuh, baca scene-staging juga. Untuk kritik terbatas, baca panduan craft dan bagian relevan saja. Jangan muat semua buku atau catatan jika tidak diperlukan.

## Aturan yang tidak boleh dilewati

1. Tentukan identitas subjek, aksi, dan konteks lihat sebelum detail. Burung generik boleh jika memang diminta; jangan mengaku akurat terhadap suatu spesies tanpa referensi.
2. Pisahkan konstruksi datar dari konstruksi volume. Perspektif dan sambungan harus masuk akal untuk pendekatan yang dipilih.
3. Perbaiki cacat besar pada skala tempat cacat muncul. Bulu tambahan tidak memperbaiki kepala yang salah sambung.
4. Nilai distorsi menurut niat dan gaya. Abstraksi bukan kesalahan otomatis, tetapi label "stilasi" tidak membenarkan semua cacat.
5. Periksa hasil yang benar-benar dirender. Jangan menyimpulkan mutu gambar dari kode, prompt, atau deskripsi saja.
6. Semua kandidat harus melewati pemeriksaan craft masing-masing sebelum dibandingkan untuk taste. Kandidat yang belum layak diberi status revisi, bukan dinyatakan kalah gaya.
7. Bedakan pemeriksaan file, penilaian visual agen, dan respons penonton. Satu jenis bukti tidak menggantikan yang lain.
8. Simpan versi terdahulu dan cacat yang belum selesai. Jangan menulis ulang sejarah kritik menjadi klaim keberhasilan.

## Alur kerja

### 1. Kunci brief secukupnya

Catat subjek dan tujuannya. Nyatakan apa yang perlu terbaca, oleh siapa, pada ukuran atau media apa. Pilih pendekatan: observasional, karakter rekaan, grafis geometris, atau dekoratif. Nyatakan tahap hasil: studi kasar atau hasil siap pakai.

Ambil konteks yang sudah diberikan. Tanyakan paling banyak dua hal yang benar-benar mengubah pekerjaan. Jika belum diketahui, tulis asumsi yang bisa dibalik. Jangan menebak spesies atau menciptakan bukti pasar. Untuk latihan pribadi, tujuan belajar sudah cukup; validasi komersial tidak diperlukan.

### 2. Amati referensi dan ukur hubungan

Pilih referensi yang mendukung pose serta ciri subjek. Catat asal dan izin penggunaan. Bedakan foto utama, referensi detail, dan inspirasi gaya.

Tulis hubungan yang bisa diperiksa: rasio massa, letak fitur terhadap kontur, arah sendi, dan tumpuan. Untuk subjek rekaan, tetapkan invariannya sendiri. Jangan mencampur anatomi dari spesies berbeda tanpa keputusan yang disengaja.

Jika referensi tidak dapat diakses, jelaskan batasnya. Boleh membuat studi generik yang diberi label; jangan mengklaim akurasi yang tidak bisa diperiksa.

### 3. Bangun massa dan aksi

Mulai dengan arah aksi atau susunan dominan. Letakkan massa utama, lalu bagian yang menghubungkannya. Gunakan operasi pada bentuk dasar dan, bila perlu, volume sederhana.

Periksa siluet, ruang negatif, perbandingan besar-kecil, dan kontak dengan lingkungan. Untuk banyak karakter, buka layout massa dan periksa hubungan tindakan serta kedalaman sebelum material. Simpan bukti inspeksi layout. Garis konstruksi boleh kasar. Jangan membuat pertemuan massa yang salah tampak rapi lewat outline.

### 4. Periksa struktur sebelum detail

Gunakan pemeriksaan struktur di panduan craft. Catat bukti dan status: `layak untuk tahap ini`, `revisi`, atau `belum dapat dinilai`.

Jika ada cacat pada identitas, aksi, perspektif, atau sambungan yang relevan dengan brief, kembali ke konstruksi. Jika sengaja menyimpang, jelaskan aturan distorsi dan lihat apakah hasilnya masih konsisten serta terbaca.

### 5. Kerjakan bagian dan material

Bangun komponen menurut fungsi serta hubungan tumpang tindih. Turunkan bentuk ke detail yang dibutuhkan. Bulu penutup tidak digambar dengan resep yang sama seperti bulu terbang; tekstur mengikuti permukaan, bukan sekadar mengisi ruang kosong.

Tentukan anggaran detail berdasarkan tujuan dan ukuran akhir. Permintaan detail penuh tetap boleh dipenuhi setelah struktur beres. Jangan memperlakukan setiap piksel sebagai bentuk geometris kecil, kecuali grid piksel memang bagian dari medium pixel art.

### 6. Render, lihat, lalu revisi

Pilih alat berdasarkan kebutuhan hasil. Jangan memaksakan satu renderer untuk semua pendekatan. Render, buka hasil utuh, periksa bagian bermasalah pada pembesaran, lalu lihat pada ukuran pemakaian.

Lakukan revisi dengan catatan: bagian mana salah, dugaan penyebab, perubahan, dan bukti sesudahnya. Ubah penyebab yang teramati sebelum menambah dekorasi. Jika alat atau anggaran tidak memungkinkan perbaikan, berhenti dengan status revisi dan langkah lanjut yang spesifik. Jangan melanjutkan ke taste untuk menghindari cacat tersebut.

### 7. Bandingkan hanya kandidat yang layak

Baca panduan komunikasi dan gaya. Kunci tujuan, aksi, serta kondisi tampilan yang sama. Gunakan standar craft sesuai gaya tiap kandidat; tingkat detail tidak harus sama.

Jika semuanya layak, bandingkan apa yang terbaca dan apa yang dikorbankan. Jelaskan pilihan dengan alasan terkait brief. Preferensi pengguna sah; jangan mengubahnya menjadi hukum universal atau skor taste objektif.

Jika ada kandidat belum layak, tahan keputusan taste. Kritik konsep awal boleh dilakukan untuk mencari masalah, tetapi bukan bukti bahwa satu gaya lebih baik.

### 8. Serahkan hasil dengan status bukti

Sertakan hasil visual bila memang diminta, sumber referensi, dan catatan singkat tentang perubahan serta batas yang tersisa. Simpan worksheet untuk pekerjaan yang berlanjut. Perbarui memori proyek pada milestone jika proyek punya file memori.

Nyatakan tepat apa yang diuji. "PNG bisa dibuka" berbeda dari "struktur sesuai referensi". Tanpa penonton yang benar-benar diuji, tulis "penilaian agen" atau "hipotesis komunikasi", bukan "penonton memahami".

## Bentuk kritik yang wajib dipakai

`Bagian/lokasi → yang terlihat → mengapa bermasalah untuk brief → perubahan → pemeriksaan ulang.`

Contoh: "Di tengkuk, kepala masih berakhir sebagai busur terpisah. Untuk studi observasional ini sambungannya terlihat ditempel. Ubah transisi tengkuk mengikuti foto, lalu periksa siluet tanpa bulu."

Hindari "kurang premium", "lebih hidup", atau "taste-nya bagus" tanpa menunjukkan keputusan visual yang dimaksud.
