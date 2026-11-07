# Susunan slide — versi 10 (dicoret ulang Sari, 7 November)

Versi sebelumnya 13 bagian, dipadatkan jadi 10. Slide 1–5 narasi sudah ada di
`narasi-sari-v5.md`. Rencana awal slide 6–11 digabung, dan pemetaannya dicatat di bawah
supaya isi yang penting tidak hilang.

| # | Slide | Inti |
|---|---|---|
| 1 | Kopi Pagi | Expert WorkBuddy yang merancang ulang materi kuliah untuk mahasiswa pekerja |
| 2 | Ritme keseharian | Kerja 8 jam, kelas 18.30, modul 30 halaman, batre otak 5% |
| 3 | Ini masalah desain | Bukan malas. Modul dirancang untuk orang yang punya dua jam dan kepala jernih |
| 4 | Yang sudah dicoba | NotebookLM dan ChatGPT memberi teks lebih pendek, bukan alasan untuk peduli |
| 5 | Solusi: satu paket | Rangkuman, mindmap, artikel, audio, soal. Satu bentuk tidak menutup masalah |
| 6 | Roadmap | Status: yang jalan sekarang vs tahap teknis berikutnya |
| 7 | Desain arsitektur MVP | Empat peran, satu skill, gerbang manusia, dan kenapa dipisah begitu |
| 8 | Implementasi | Wujudnya di WorkBuddy: berkas, alur, dan apa yang benar-benar jalan |
| 9 | Pengujian | Aturan yang dipakai menguji, hasilnya, termasuk yang gagal |
| 10 | Kesimpulan | Batasan, manfaat, dan arah berikutnya |

## Jawaban untuk pertanyaan urutan: implementasi dulu, baru pengujian

Urutan yang dipakai: **desain → implementasi → pengujian → kesimpulan**, jadi implementasi di slide 8
dan pengujian di slide 9. Alasannya sederhana: pengujian menilai sesuatu yang sudah ditunjukkan.
Kalau pengujian ditaruh lebih dulu, penonton diminta percaya pada hasil uji dari benda yang belum
pernah mereka lihat.

Pengecualian: kalau yang dimaksud "implementasi" adalah **cara pakai sehari-hari di lapangan**
(setelah lulus uji, ini ritme paginya), maka pengujian dulu baru implementasi. Itu bukan salah,
cuma genre yang berbeda: laporan pengembangan vs studi kasus pemakaian.

## Pemetaan isi versi 13 ke versi 10

| Isi versi lama | Masuk ke |
|---|---|
| Isi expert, urutan satu sesi | slide 7 dan 8 |
| Kenapa beberapa peran, kenapa reviewer | slide 7, satu paragraf |
| Kenapa gerbang manusia | slide 7, satu kalimat |
| Kenapa blog, kenapa tidak semua di blog | **slide 7 atau 10**, jangan hilang. Ini jawaban untuk pertanyaan hak cipta |
| Gambaran besar kalau jadi sistem (portal login) | slide 10, bagian "arah berikutnya" |
| Bukti satu sesi (artefak, screenshot) | slide 9 |

## Catatan

- Slide 10 berisi tiga hal (batasan, manfaat, arah). Kalau waktunya mepet, potong yang paling lemah,
  jangan potong "arah berikutnya", karena di situ letak janji portal berlogin.
- Slide 9 wajib memuat satu kegagalan. Pengujian yang semuanya hijau terbaca sebagai tidak diuji.
- Slide 7 sebaiknya tetap menyebut kenapa materi privat tidak ikut tayang. Satu kalimat cukup, dan itu
  yang membedakan produk ini dari pembuat ringkasan biasa.
