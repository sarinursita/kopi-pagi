# Roadmap produk Kopi Pagi: v1 sampai v4

**Status:** draft, menunggu persetujuan Sari · **Ditulis:** 7 November 2026
**Sumber keputusan:** percakapan 7 Nov (artikel = salah satu jalan masuk; rangkuman dulu baru artikel; latihan soal dijadwalkan, bukan ditumpuk)

## Prinsip

1. **Artikel bukan hasil akhir, tapi dosis pertama.** Tugasnya menanam kail: satu istilah, satu adegan, satu rasa penasaran, supaya waktu materi aslinya datang pembaca sudah pernah ketemu versi lemahnya.
2. **Rangkuman sendirian tidak menyelesaikan masalah.** Yang salah bukan rangkuman, tapi menjadikan rangkuman satu-satunya bentuk.
3. **Bentuk mengikuti energi dan waktu, bukan mengikuti format.** Pagi untuk masuk (baca), sepanjang hari untuk menyelip (dengar dan menjawab), malam tidak dijadwalkan.
4. **Cakupan modul harus bisa diperiksa, bukan dijanjikan.** Tulangnya `konsep_dipakai` dan `konsep_dibuang` yang sudah keluar di log audit.

## Hierarki artefak

```
modul PDF
   └─ rangkuman        semua konsep sesi, bentuk padat, jadi tulang cakupan
        └─ artikel     dosis pertama, dramatisasi dari rangkuman (bukan dari PDF)
        └─ mindmap     peta konsep, sekali lihat
        └─ unit audio  satu unit per konsep, ada transkripnya
             └─ latihan soal  penguat, dijadwalkan, 1 pertanyaan per notifikasi
```

Urutan kerja **rangkuman dulu, artikel kemudian** mengikuti cara Sari bekerja sehari-hari: materi diringkas bersama Max, lalu artikelnya ditulis Wiz dari rangkuman itu. Konsekuensi teknis: Writer tidak membaca PDF lagi setelah rangkuman jadi. Artikel tidak bisa membawa konsep yang tidak ada di rangkuman, jadi cakupan otomatis warisan.

## Halaman hub (bentuk situs)

Blog bukan deretan post. Blog adalah **daftar isi satu semester**.

- `/materi` indeks semua sesi. Satu semester 30 sesi = 30 tautan, urut sesi, dengan status per artefak.
- `/materi/sesi-01` hub sesi. Lima pilihan: artikel, rangkuman, mindmap, audio, latihan soal.
- Artefak yang belum ada tetap ditampilkan, dengan label versinya (`v2`, `v3`, `v4`). Kosong yang jelas lebih jujur daripada menu yang disembunyikan.
- Setiap artefak punya tautan balik ke hub sesinya dan ke sesi sebelum/berikutnya.

## Latihan soal (v4)

Dua tipe, aturan sama untuk keduanya: **satu pertanyaan per kiriman.**

| Tipe | Isi | Kapan |
|---|---|---|
| Objektif | satu pertanyaan pendek, kunci tunggal | siang, sela kerja |
| Esai | satu pertanyaan, jawaban 1 sampai 2 kalimat, kunci muncul setelah dijawab | pagi di KRL, sore |

- **Bukan soal analisis.** Tujuannya mengulang, bukan menguji kecerdasan. Contoh: sebutkan tahapan software design, sebutkan salah satu agile manifesto, apa itu regresi, spam filter itu machine learning jenis apa.
- **Dijadwalkan, jangan ditumpuk.** Tiga kiriman per hari di waktu berbeda, bukan lima sekaligus. Lima terasa seperti kewajiban ibadah, tiga terasa seperti teman yang mencolek. Slot yang dipakai: 07:00 (KRL), 12:30 (makan siang), 16:45 (menjelang pulang).
- **Tidak lewat gerbang persetujuan.** Gerbang manusia hanya untuk artefak yang terbit. Latihan soal tidak terbit, jadi tidak butuh approval, cukup aturan mutu.
- Kalau satu hari kelewat, pertanyaannya tidak diakumulasi ke hari berikutnya. Kelewat ya kelewat.

## Status tayang per artefak (usul R13)

Hak cipta melindungi ekspresi, bukan ide. Definisi ego dan superego bukan milik dosen siapa pun. Karena itu kelayakan tayang dinilai **per artefak**, bukan per sumber:

| Artefak | Sifat transformasi | Status tayang |
|---|---|---|
| Artikel | ekspresi baru: adegan sendiri, urutan sendiri, istilah dan konsep umum | publik |
| Rangkuman | menuruti urutan dan pilihan konsep modul, parafrase dekat | privat |
| Mindmap | struktur modul dipetakan apa adanya | privat |
| Unit audio | isi sama, dipecah jadi struktur baru dan dikembangkan | publik setelah naskahnya diperiksa sebagai teks, bukan sebagai audio |
| Latihan soal | cuma meminjam istilah umum, tanpa ekspresi dosen | publik, dengan syarat kunci jawaban ditulis sendiri |

Usul aturan:

- **R13.1** Status tayang ditentukan per artefak, bukan per sumber.
- **R13.2** Artefak berstatus privat tidak punya URL publik dan tidak muncul di indeks `/materi`.
- **R13.3** Naskah audio dinilai sebagai teks. Parafrase dekat tetap parafrase dekat walau dibacakan.
- **R13.4** Kunci jawaban dilarang mengutip kalimat modul.
- **R13.5** Daftar `konsep_dipakai` tetap internal di log audit, tidak pernah terbit sebagai kerangka modul.

Efeknya ke hub: lima kotak per sesi tetap ada, tapi dua di antaranya berlambang kunci. Di v1 kunci itu artinya "tidak dipublikasikan", bukan "login" (auth masuk v5).

## Ruang privat: Slack sebagai portal (bukan login sendiri)

Menerbitkan artinya menaruh konten di suatu tempat. Menaruh di channel Slack privat adalah menerbitkan juga, tapi batas aksesnya sudah ada: keanggotaan workspace. Jadi portal privat tidak perlu dibangun dari nol.

- **Blog publik = etalase.** Artikel, soal, dan tautan. Tidak ada yang sensitif.
- **Slack privat = ruang belajar.** Rangkuman, mindmap, unit audio, arsip. Satu channel per kebutuhan, anggota hanya user dan agent.
- Kotak yang terkunci di hub tidak menautkan berkas, tapi boleh menautkan pesan Slack. Yang melihat tautan tanpa akses akan mendarat di halaman minta masuk, bukan di materi.
- Aturan yang menyertainya: artefak privat hanya boleh berada di channel yang anggotanya user dan agent. Begitu ada anggota manusia lain, status privat gugur dan artefak harus ditinjau ulang.

Konsekuensi yang diakui: Slack bukan pengaman keras. Anggota bisa menyalin, dan admin workspace bisa mengekspor. Untuk catatan belajar pribadi itu cukup, dan lebih jujur daripada mengaku aman.

## Tutor: peran kelima (v2, bukan v1)

Interaksi di Slack adalah tempat produk ini bisa naik kelas atau justru kehilangan disiplin. Dua pilihan:

| Pilihan | Kekuatan | Masalah |
|---|---|---|
| Asisten WorkBuddy tanpa batas | bebas, apa pun bisa ditanya | tidak bisa dipertanggungjawabkan, bisa membocorkan isi modul, tidak ada aturan yang bisa dikutip |
| **Agent Tutor dengan batas** | jawaban bisa ditelusuri, penolakan beralasan | perlu aturan baru dan artefak bukti |

Yang dipakai: Tutor dengan batas. Batasnya sederhana karena bahan bakunya sudah ada, yaitu **rangkuman sesi**.

- Tutor menjawab dari rangkuman sesi itu, bukan dari PDF.
- Setiap jawaban menyebut konsep mana yang dipakai.
- Pertanyaan di luar sesi ditolak dengan alasan, bukan dijawab setengah.
- Tutor dilarang menulis artikel baru atau mengubah rangkuman. Tugasnya menjelaskan, bukan memproduksi.
- Format jawaban: maksimal 120 kata, satu contoh konkret.

Ini sekaligus menjawab satu pertanyaan desain yang belum pernah dijawab: rangkuman bukan cuma artefak yang disimpan, tapi **basis pengetahuan Tutor**. Karena rangkuman dijaga R12, jawaban Tutor otomatis terikat cakupan yang sama.

Tidak masuk v1 karena menambah satu peran berarti menambah aturan, bukti, dan waktu demo di hari yang sama dengan deadline.

## Versi

| Versi | Isi | Selesai kalau |
|---|---|---|
| **v1** | rangkuman + artikel + hub indeks sesi | setiap `konsep_dipakai` muncul di rangkuman; artikel 1.000 sampai 1.500 kata lolos Reviewer; `/materi` dan hub sesi bisa dibuka |
| **v2** | mindmap | satu sesi punya mindmap yang bisa dirender dari teks (Mermaid atau SVG), dan tiap cabang cocok dengan `konsep_dipakai` |
| **v3** | unit audio microlearning + transkrip | jumlah unit = jumlah `konsep_dipakai`; setiap unit maksimal 90 detik; setiap unit punya transkrip; tidak ada konsep yang hanya muncul di artikel |
| **v4** | latihan soal terjadwal | bank soal menutup semua `konsep_dipakai`; tiga slot per hari jalan tanpa approval; kunci tidak pernah terkirim sebelum jawaban |

## Yang sengaja belum masuk

- **Mindmap sebagai gambar.** v2 cukup teks yang bisa dirender. Renderer gambar butuh skill kelima, dan itu bukan pekerjaan satu hari.
- **Personal adaptive schedule.** Menjadwalkan ulang berdasarkan jawaban salah itu produk lain. v4 cukup waktu tetap.
- **Notifikasi lintas app.** WhatsApp dan Instagram tetap distribusi manual. Penjadwalan latihan cukup di Slack, yang sudah tersambung.

## Risiko

| Risiko | Catatan |
|---|---|
| Hub 30 sesi dengan 5 artefak = 150 halaman | v1 baru 3 artefak per sesi. Halaman kosong wajib punya label versi, jangan halaman rusak |
| Bank soal 3 per hari x 30 sesi | 90 soal. v1 cukup satu sesi sebagai bukti, sisanya menyusul |
| Rangkuman jadi batas mutu | kalau rangkuman salah, artikel dan soal mewarisi salahnya. Reviewer wajib memeriksa rangkuman sebelum artikel ditulis |
