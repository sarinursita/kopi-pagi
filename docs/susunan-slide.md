# Susunan slide — versi 10 (hasil coretan Sari, 7 November)

| # | Slide | Isi |
|---|---|---|
| 1 | Kopi Pagi | Expert WorkBuddy yang merancang ulang materi kuliah untuk mahasiswa pekerja |
| 2 | Ritme keseharian | Kerja 8 jam, kelas 18.30, modul 30 halaman, batre otak 5% |
| 3 | Ini masalah desain | Bukan malas. Modul dirancang untuk orang yang punya dua jam dan kepala jernih |
| 4 | Yang sudah dicoba | NotebookLM dan ChatGPT memberi teks lebih pendek, bukan alasan untuk peduli |
| 5 | Solusi: satu paket | Rangkuman, mindmap, artikel, audio, soal. Satu bentuk tidak menutup masalah |
| 6 | Roadmap | Apa yang MVP, apa yang menyusul, dan **kenapa** urutannya begitu |
| 7 | Desain arsitektur MVP | Empat peran, satu skill, gerbang manusia, dan semua **kenapa** di baliknya |
| 8 | Pengujian | Yang diuji sekarang: expert-nya. Aturan yang dipakai, hasilnya, termasuk yang gagal |
| 9 | Implementasi | Dipasang dan dipakai: hasil nyata di blog dan di email |
| 10 | Kesimpulan | Batasan, manfaat, arah berikutnya |

## Kenapa pengujian (8) sebelum implementasi (9)

Bukan karena lupa urutan, tapi karena kata "implementasi" di sini berarti **dipasang dan dipakai**,
bukan "dibangun". Bangunannya sudah dibahas di slide 7 (desain) dan diuji di slide 8.

Urutannya jadi:

1. **Desain** apa yang dibangun dan kenapa begitu.
2. **Uji** expert-nya: aturan mana yang dipakai, apa yang lolos, apa yang ditolak.
3. **Implementasi**: setelah lolos uji, dipasang dan dipakai. Yang ditunjukkan hasilnya, bukan rencananya.
4. **Kesimpulan**.

Kalau dibalik, slide 9 akan memamerkan hasil yang belum pernah diuji di depan penonton, dan slide 8
jadi kehilangan gunanya.

## Pembagian "kenapa" — jangan diulang di dua slide

Semua pertanyaan "kenapa" dijawab di slide 6 dan 7, karena di situ tempatnya: menjelaskan MVP.

| Pertanyaan | Dijawab di |
|---|---|
| Kenapa beberapa peran, bukan satu agent | slide 7 |
| Kenapa harus ada Reviewer | slide 7 |
| Kenapa gerbang manusia | slide 7 |
| Kenapa blog, kenapa tidak semua materi di blog | slide 7 (keputusan arsitektur, sekaligus jawaban hak cipta) |
| Kenapa MVP-nya lewat email, bukan portal | slide 6 dan 10 |
| Kenapa urutan pembangunannya begitu | slide 6 |

Slide 8 dan 9 **tidak mengulang alasan**, hanya menunjukkan bukti.

## Isi minimum tiap slide

**Slide 6 · Roadmap.** Satu batang waktu sederhana: yang berjalan sekarang (rangkuman, artikel), lalu
tahap berikutnya (mindmap, unit audio, latihan soal, portal). Satu kalimat: "ini MVP, sengaja minimal
dan lewat email yang murah".

**Slide 7 · Arsitektur MVP.** Diagram empat peran + skill + gerbang. Di bawahnya tiga sampai empat
kalimat "kenapa", masing-masing satu baris, tidak boleh lebih.

**Slide 8 · Pengujian.** Aturan yang dipakai menguji (nomor dan bunyinya), hasil per aturan, dan satu
kegagalan yang diakui. Screenshot vonis Reviewer yang menyebut ID aturan.

**Slide 9 · Implementasi.** Dua artefak nyata: satu halaman blog yang bisa dibuka, dan satu tangkapan
layar email rangkuman yang masuk. Sebutkan di sesi mana, tanggal berapa.

**Slide 10 · Kesimpulan.** Batasan (agent hanya hidup saat mesin menyala; kebenaran isi bukan wilayah
mesin), manfaat (satu sesi selesai di pagi hari, materi nyantol), arah berikutnya (portal dengan login,
semua materi di satu tempat, aman soal hak cipta).

## Catatan

- Slide 9 baru bisa diisi setelah run hari ini selesai dan ada artikel tayang + email masuk.
- Slide 8 wajib memuat satu kegagalan. Pengujian yang semuanya hijau terbaca sebagai belum diuji.
- Slide 10 memuat tiga hal. Kalau waktu mepet, potong yang paling lemah, jangan potong "arah berikutnya".
