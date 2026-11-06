# Roadmap produk Kopi Pagi: v1 sampai v5

**Status:** draft, menunggu persetujuan Sari · **Ditulis:** 7 November 2026, diperbarui setelah keputusan kanal
**Sumber keputusan:** percakapan 7 Nov (artikel = salah satu jalan masuk; rangkuman dulu baru artikel; soal dijadwalkan; kanal sebagai portal; Tutor = v5)

## Prinsip

1. **Artikel bukan hasil akhir, tapi dosis pertama.** Tugasnya menanam kail: satu istilah, satu adegan, satu rasa penasaran, supaya waktu materi aslinya datang pembaca sudah pernah ketemu versi lemahnya.
2. **Rangkuman sendirian tidak menyelesaikan masalah.** Yang salah bukan rangkuman, tapi menjadikan rangkuman satu-satunya bentuk.
3. **Bentuk mengikuti energi dan waktu, bukan mengikuti format.** Pagi untuk masuk (baca), sepanjang hari untuk menyelip (dengar dan menjawab), malam tidak dijadwalkan.
4. **Cakupan modul harus bisa diperiksa, bukan dijanjikan.** Tulangnya `konsep_dipakai` dan `konsep_dibuang` yang sudah keluar di log audit.
5. **Terbit itu soal tempat, bukan soal situs.** Menaruh konten di kanal privat sudah terbit, dan batas aksesnya sudah ada tanpa perlu membangun login.

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

## Tempat terbit: kanal sebagai portal, blog sebagai etalase

Ada dua permukaan terbit, dan pembagiannya bukan selera tapi soal hak dan akses.

| Permukaan | Isi | Kenapa di situ |
|---|---|---|
| **Kanal (Discord)**, primer | semua artefak: rangkuman, artikel, mindmap, audio, soal | aksesnya sudah ada (keanggotaan server), riwayatnya awet, tidak perlu membangun login |
| **Blog publik**, sekunder | artikel saja | artikel satu-satunya artefak yang ekspresinya baru, jadi aman tayang |

Bentuk kanalnya: satu **post forum per sesi** di `#materi`, dan di dalamnya lima pesan atau thread: rangkuman, artikel, mindmap, audio, soal. Post forum berperan sebagai hub sesi, dan daftar post berperan sebagai daftar isi satu semester. Nol kode.

Keputusan yang mengikutinya:

- **Blog tidak perlu daftar isi dan tidak perlu tautan ke rangkuman.** Daftar isi hidup di kanal. Blog cukup artikel plus satu tautan ke server bagi yang punya akses, atau tanpa tautan sama sekali.
- **Slack ditinggalkan sebagai portal** karena sambungan Slack ke WorkBuddy belum nyambung. Discord dipakai karena koneksinya jalan, riwayatnya tidak dibatasi di free plan, dan forum channel sudah memberi struktur hub.
- **Keanggotaan server = satu manusia.** Begitu ada anggota manusia kedua, status privat gugur dan artefak harus ditinjau ulang.

Konsekuensi yang diakui: kanal bukan pengaman keras. Anggota bisa menyalin, admin server bisa mengekspor. Untuk catatan belajar pribadi itu cukup, dan lebih jujur daripada mengaku aman.

## Satu bot, empat mandat (bukan empat bot)

Yang masuk ke Discord adalah **asisten WorkBuddy**, bukan Kiki, Susi, Wena, dan Yani sebagai empat akun terpisah. Ini perlu ditulis supaya tidak jadi janji palsu di depan juri.

- Yang terlihat di kanal: satu bot, wajahnya Kiki sebagai pemimpin redaksi.
- Yang terjadi di belakang: empat mandat berjalan berurutan, dan **namanya muncul di teks**, bukan di akun. Contoh: "Brief selesai. Wena menulis. Yani menolak R4.3 karena penutup punya dua pertanyaan."
- Formulir submission minta 3 agent terpisah dengan mandat berbeda. Empat skill dengan mandat terpisah tetap memenuhi itu, walau antarmukanya satu bot.
- Yang **tidak** boleh: menjanjikan empat bot di kanal, atau menjanjikan asisten tanpa batas yang bisa apa saja. Yang kedua tidak bisa dipertanggungjawabkan karena tidak ada aturan yang bisa dikutip saat dia salah.

## Batas runtime: agent hanya hidup saat mesin user menyala

WorkBuddy berjalan di mesin user. Artinya:

- Cron 05:00 hanya jalan kalau mesin menyala jam 05:00. Kalau laptop tutup, tidak ada artikel.
- Konsekuensi untuk demo: kalimat "pagi berikutnya saya dapat artikel" harus diberi syarat "mesin menyala", atau demo dijalankan manual saat sesi direkam.
- Agent 24/7 butuh runtime di server, bukan di laptop. Itu di luar lingkup hackathon dan ditulis sebagai batas, bukan disembunyikan.
- Efek samping ke v4: soal terjadwal juga hanya terkirim saat mesin menyala. Jadwal yang bolong bukan bug, itu batas runtime.

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
- **R13.2** Artefak berstatus privat hanya boleh berada di kanal yang anggotanya user dan agent, tidak pernah di blog publik.
- **R13.3** Naskah audio dinilai sebagai teks. Parafrase dekat tetap parafrase dekat walau dibacakan.
- **R13.4** Kunci jawaban dilarang mengutip kalimat modul.
- **R13.5** Daftar `konsep_dipakai` tetap internal di log audit, tidak pernah terbit sebagai kerangka modul.

## Tutor: mode kedua bot (v5)

Tutor bukan peran kelima dan bukan bot baru. Karena yang tersambung ke kanal cuma satu asisten, Tutor paling masuk akal sebagai **mode** dari bot yang sama, dipicu perintah atau kanal khusus, dengan aturan sendiri.

Alasannya bukan kerapian, tapi pertanggungjawaban: asisten tanpa batas tidak bisa disalahkan dengan aturan apa pun kalau jawabannya salah, dan bisa membocorkan kalimat modul ke dalam chat.

Batas Tutor, dan bahannya sudah ada:

- Menjawab dari **rangkuman sesi**, bukan dari PDF.
- Setiap jawaban menyebut konsep mana yang dipakai.
- Pertanyaan di luar sesi ditolak dengan alasan, bukan dijawab setengah.
- Dilarang menulis artikel baru atau mengubah rangkuman. Tugasnya menjelaskan, bukan memproduksi.
- Maksimal 120 kata, satu contoh konkret.

Efek sampingnya bagus: rangkuman jadi **basis pengetahuan Tutor**. Karena rangkuman dijaga R12, jawaban Tutor otomatis terikat cakupan yang sama. Satu aturan menjaga dua hal.

## Portal dengan login sendiri (v5, kalau memang perlu)

Kalau kanal terasa kurang, portal sendiri bisa dibangun tanpa kerangka berat:

- Blog tetap statis (Hugo, Astro, atau Eleventy), karena host WorkBuddy menerima Node tapi tidak menerima PHP. Hasil build statis paling aman.
- Login jangan ditaruh di aplikasi. Taruh di depan, pakai Cloudflare Access atau Worker dengan basic auth. Nol basis data, nol framework tambahan.
- Portal baru layak kalau artefak privat perlu dicari, disaring, dan ditautkan dari luar kanal. Selama kebutuhannya cuma "jangan tayang publik", kanal sudah cukup.

## Versi

| Versi | Isi | Selesai kalau |
|---|---|---|
| **v1** | rangkuman + artikel, portal di kanal, blog artikel saja | setiap `konsep_dipakai` muncul di rangkuman; artikel 1.000 sampai 1.500 kata lolos Reviewer; satu post forum per sesi berisi keduanya |
| **v2** | mindmap | satu sesi punya mindmap yang bisa dirender dari teks (Mermaid atau SVG), dan tiap cabang cocok dengan `konsep_dipakai` |
| **v3** | unit audio microlearning + transkrip | jumlah unit = jumlah `konsep_dipakai`; maksimal 90 detik per unit; setiap unit punya transkrip; tidak ada konsep yang hanya muncul di artikel |
| **v4** | latihan soal terjadwal | bank soal menutup semua `konsep_dipakai`; tiga slot per hari jalan tanpa approval; kunci tidak pernah terkirim sebelum jawaban |
| **v5** | portal login sendiri, mode Tutor | portal hanya bisa dibuka pemilik; Tutor menolak pertanyaan di luar sesi dengan menyebut alasannya |

## Yang sengaja belum masuk

- **Mindmap sebagai gambar.** v2 cukup teks yang bisa dirender. Renderer gambar butuh skill kelima.
- **Personal adaptive schedule.** Menjadwalkan ulang berdasarkan jawaban salah itu produk lain. v4 cukup waktu tetap.
- **Notifikasi lintas app.** WhatsApp dan Instagram tetap distribusi manual.
- **Agent 24/7.** Butuh runtime di server. Ditulis sebagai batas.

## Risiko

| Risiko | Catatan |
|---|---|
| Runtime di mesin user | cron mati kalau mesin mati. Semua janji "otomatis pagi" bergantung pada ini |
| Kanal jadi satu-satunya arsip | kalau server dihapus atau akun kena limit, arsip hilang. Perlu ekspor berkala ke repo |
| Bank soal 3 per hari x 30 sesi | 90 soal. v1 cukup satu sesi sebagai bukti |
| Rangkuman jadi batas mutu | kalau rangkuman salah, artikel, audio, dan soal mewarisi salahnya. Reviewer wajib memeriksa rangkuman sebelum artikel ditulis |
| Satu bot, empat mandat | kalau dijual sebagai empat bot, juri yang masuk kanal akan melihat satu akun dan menganggap klaimnya berlebihan |
