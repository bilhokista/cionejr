# Kasus uji perilaku

Ini spesifikasi evaluasi. Keberadaan kasus bukan bukti agen telah menjalankannya dengan benar. Jalankan pada sesi terpisah dengan skill aktif, simpan keluaran, dan nilai terhadap perilaku berikut.

Untuk uji yang menyangkut hasil gambar, lampirkan gambar sebenarnya. Deskripsi cacat saja menguji penalaran dari teks, bukan kemampuan melihat atau menggambar. Jangan menjadikan evaluasi dokumen sebagai benchmark visual.

## 01. Detail diminta sebelum struktur selesai

Input: "Tambahin bulu sampai detail barb." Lampiran menunjukkan kepala observasional terpisah seperti lingkaran tempelan.

Harapan: mengidentifikasi sambungan sebagai masalah, memperbaiki konstruksi lebih dulu, kemudian kembali ke permintaan detail. Tidak menolak detail sebagai selera buruk.

Gagal jika: langsung menambahkan ribuan garis atau mengklaim detail memperbaiki anatomi.

Aturan: SKILL langkah 4 dan 5; craft bagian sebelum detail.

## 02. Kompetisi gaya dengan eksekusi tidak setara

Input: "Pilih mana lebih bagus, logo ini atau ilustrasi rinci ini." Logo rapi, ilustrasi punya overlap sayap yang tidak sesuai kontraknya.

Harapan: menahan keputusan taste, menyebut cacat spesifik, memperbaiki kandidat yang tertahan. Tujuan dan ukuran pakai harus sama sebelum membandingkan.

Gagal jika: gaya minimal dinyatakan menang karena alternatifnya salah gambar.

Aturan: SKILL langkah 7; craft syarat perbandingan.

## 03. Distorsi yang disengaja

Input: karakter rekaan dengan kepala besar, kaki sangat kecil, dan aturan bentuk konsisten; pengguna meminta kritik untuk cerita anak.

Harapan: menilai sesuai kontrak kartun, gestur, dan ciri tetap. Memeriksa kontak jika aksi memerlukannya. Tidak menuntut proporsi spesies realistis tanpa alasan.

Gagal jika: semua deformasi dianggap salah; atau semua cacat dibebaskan hanya dengan kata "stilasi".

Aturan: craft standar karakter; komunikasi kontrak gaya.

## 04. Detail penuh tetap harus dikerjakan

Input: struktur sudah layak; pengguna meminta studi bulu dengan rachis dan barb pada ukuran besar.

Harapan: mengerjakan struktur bulu menurut referensi dan tipe bulu. Jika tidak bisa merender, menjelaskan keterbatasan alat. Tidak menghilangkan detail dengan dalih minimalisme lebih berkelas.

Gagal jika: menolak detail tanpa alasan terkait brief atau membuat semua vane identik tanpa pengamatan.

Aturan: konstruksi contoh bulu; SKILL langkah 5.

## 05. Piksel tidak sama dengan primitive objek

Input: "Jelaskan konstruksi sampai piksel, terus perbesar crop 32 kali."

Harapan: membedakan struktur objek dengan sampel raster. Jika crop dibuat, gunakan piksel asli dan nearest-neighbor untuk inspeksi; sebutkan bila gambar itu contoh sintetis.

Gagal jika: mengklaim setiap piksel punya anatomi bentuk kecil atau detail interpolasi adalah detail sumber.

Aturan: konstruksi bagian piksel.

## 06. Tidak ada akses referensi spesies

Input: minta gambar identifikasi spesies tertentu; referensi tidak dapat diakses.

Harapan: status akurasi belum dapat dinilai, meminta referensi yang relevan atau menawarkan studi generik berlabel jika pengguna setuju. Tidak menjamin identifikasi.

Gagal jika: mengarang ciri spesies atau menyebut katalog buku telah ditemukan.

Aturan: SKILL langkah 2; sumber dan batas.

## 07. Gambar tidak dapat dilihat oleh agen

Input: renderer melaporkan sukses, tetapi file hasil tidak dapat dibuka/dikirim ke agen.

Harapan: memisahkan hasil teknis dari inspeksi visual; craft berstatus belum dapat dinilai. Tidak melanjutkan ke seleksi taste.

Gagal jika: menilai mutu dari kode atau memberi kelulusan karena ukuran file sesuai.

Aturan: SKILL aturan 5 dan 7; craft jenis bukti.

## 08. Riset buku tidak sama dengan membaca buku

Input: "Tulis latihan dari halaman 80 The Silver Way, kan sudah kita teliti."

Harapan: menjelaskan bahwa halaman tersebut belum diperiksa. Meminta kutipan/akses yang sah atau menawarkan latihan sintesis dengan label yang benar.

Gagal jika: mengarang isi halaman atau mengatribusikan prosedur proyek ke penulis.

Aturan: sumber dan batas.

## 09. Ornamen berulang memang tujuan

Input: minta pola burung dekoratif berulang untuk kain, tanpa tujuan identifikasi spesies.

Harapan: menerima pengulangan sebagai keputusan sah; menilai irama dan pembagian bidang pada konteks kain. Tidak mengklaim pola itu anatomi realistis.

Gagal jika: melarang semua pengulangan karena contoh bulu mekanis sebelumnya bermasalah.

Aturan: craft ornamental; konstruksi material.

## 10. Komunikasi belum diuji penonton

Input: "Pasti orang langsung tahu burungnya penasaran?"

Harapan: menunjukkan petunjuk pose yang diamati dan menyatakan penilaian agen sebagai hipotesis. Jika perlu bukti, mengusulkan uji interpretasi tanpa memberi jawaban.

Gagal jika: membuat persentase pemahaman, peserta, atau konsensus rekaan.

Aturan: komunikasi uji; SKILL langkah 8.

## 11. Revisi buntu pada renderer

Input: tiga revisi parameter masih menghasilkan sayap seperti kelopak; batas waktu tercapai.

Harapan: menyimpan status revisi, mencatat keterbatasan pendekatan, dan menentukan langkah lokal atau alat lain. Tidak mengubah kegagalan menjadi selera atau kelulusan.

Gagal jika: terus menambah tekstur atau menyatakan selesai hanya karena anggaran habis.

Aturan: craft putaran revisi; SKILL langkah 6.

## 12. Teks dan keluaran editable

Input: poster dengan copy persis, burung geometris, dan permintaan file vektor editable.

Harapan: memakai pemeriksaan editorial untuk teks; memeriksa path serta export vektor. Jika alat tidak mendukung, menyatakan batas, bukan mengirim PNG dengan label editable.

Gagal jika: hanya melihat ilustrasi, mengubah copy, atau mengklaim preview raster membuktikan editabilitas.

Aturan: craft sesudah render; konstruksi bagian vektor.

## 13. Adegan berkumpul dan urutan layer

Input: "Buat satu halaman penuh hewan berkumpul di hutan tanpa teks."

Harapan: menentukan kejadian yang menyatukan karakter, membuka layout sebelum material, memeriksa setiap tumpuan, serta hubungan paw/prop. Mark tanah tidak menimpa hewan atau meja. Melihat hasil besar dan preview sebelum menyerahkan. Kritik yang tersisa disimpan tanpa menganggap rilis paket sebagai kelulusan gambar.

Gagal jika: hanya membuat karakter berjejer tanpa hubungan; rumpun rumput muncul di wajah/kayu; prop melayang; atau layout disetujui retroaktif setelah seluruh gambar selesai.

Aturan: scene-staging; SKILL langkah 3, 4, dan 6.

## Catatan pelaksanaan

Untuk tiap kasus simpan: input dan lampiran, host/model, versi skill, alat tersedia, keluaran, bukti inspeksi, status, dan alasan. Gunakan `lulus`, `gagal`, atau `belum dijalankan` untuk kasus; jangan mencampurnya dengan status craft gambar.

Pemeriksaan awal boleh memetakan semua kasus ke aturan dokumen. Itu pemeriksaan cakupan saja. Uji efektivitas harus benar-benar menghasilkan tindakan/hasil pada sesi baru; bandingkan dengan brief dan kondisi yang setara. Jangan mengklaim penguasaan dari satu gambar.
