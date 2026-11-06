# Kopi Pagi

Satu sesi kuliah masuk sebagai PDF, keluar sebagai dua hal: **rangkuman untuk kamu sendiri** (dikirim ke email) dan **satu artikel pagi yang layak tayang** (setelah kamu setujui). Dibangun untuk orang yang kuliah sambil kerja dan belajar di sela-sela, bukan untuk orang yang punya waktu luang.

## Isi paket

| Berkas | Isi |
|---|---|
| `agents/kopi-pagi-team-lead.md` | Kiki, pemimpin redaksi. Mengatur urutan, memegang gerbang persetujuan |
| `agents/planner.md` | Susi, curriculum planner. Brief, daftar konsep dipakai dan dibuang |
| `agents/writer.md` | Wena, penulis. Rangkuman dulu, artikel kemudian |
| `agents/reviewer.md` | Yani, pemeriksa rulebook. Menolak dengan ID aturan, bukan selera |
| `rulebook.md` | 68 aturan bernomor dengan severity dan cara cek. Satu-satunya dasar penolakan |
| `skills/morning-study-blog/` | Prosedur teknis: ambil materi, konversi, tulis, simpan, kirim rangkuman ke email |

## Alur satu sesi

```
PDF materi sesi
   └─ Planner        brief: satu ide inti, satu sudut cerita, konsep dipakai & dibuang
        └─ Writer     rangkuman (maks 500 kata)
             └─ Reviewer  cek R12: semua konsep dipakai masuk, konsep buangan tidak
                  └─ email    rangkuman dikirim ke alamat pembaca sendiri
        └─ Writer     artikel (1000-1500 kata) ditulis DARI rangkuman, bukan dari PDF
             └─ Reviewer  cek R2, R3, R4, R9, R10, R11, R12.4
                  └─ manusia  membaca artikel utuh, lalu acc atau minta revisi
                       └─ terbit  artikel masuk blog, log audit ditulis
```

Dua hal yang tidak bisa dibalik:

1. **Rangkuman sebelum artikel.** Artikel tidak boleh ditulis sebelum rangkuman lolos R12.
2. **Tidak ada yang tayang tanpa persetujuan manusia.** Reviewer boleh PASS, tapi publikasi tetap menunggu manusia.

## Kenapa rangkuman tidak lewat gerbang manusia

Gerbang manusia itu gerbang **publikasi**, bukan gerbang kebenaran isi. Rangkuman penerimanya pembaca sendiri, dan dia belum mempelajari materinya, jadi tidak ada yang bisa dia nilai. Artikel akan dilihat orang lain, dan dia memang membacanya utuh sebelum menyetujui. Pembacaan itu sekaligus sesi belajarnya, bukan pemeriksaan terpisah.

## Folder kerja

Semua data pengguna ada di `study-blog/` pada direktori kerja, bukan di dalam paket:

```
study-blog/
├── profil.md      # termasuk email_penerima
├── character-sheet.md
├── tokoh.md
├── progress.md
├── log.md
├── rulebook.md
├── cache/         # PDF + hasil konversi
├── rangkuman/     # rangkuman per sesi
├── draft/         # artikel menunggu persetujuan
├── blog/          # artikel terbit
└── audit/         # log audit per sesi
```

## Konfigurasi email

Rangkuman dikirim lewat SMTP. Isi variabel lingkungan di tempat expert berjalan:

```
KOPIPAGI_SMTP_HOST=smtp.gmail.com
KOPIPAGI_SMTP_PORT=465
KOPIPAGI_SMTP_USER=alamat@gmail.com
KOPIPAGI_SMTP_PASS=kata-sandi-aplikasi
```

Kalau belum diisi, skrip keluar dengan pesan jelas dan rangkuman tetap tersimpan sebagai berkas. Agent dilarang mengaku email terkirim kalau belum.

## Pemasangan

1. Buka WorkBuddy, pilih **Import Expert**, arahkan ke folder `kopi-pagi/` atau ke `kopi-pagi.zip`.
2. Isi `profil.md` di folder kerja, termasuk alamat email.
3. Salin `rulebook.md` ke `study-blog/rulebook.md`.
4. Jalankan sesi pertama. Kalau `study-blog/profil.md` belum ada, Kiki akan bertanya enam hal dulu, dan tidak menulis artikel sebelum dijawab.

## Yang belum ada (jujur)

- **Jalan hanya saat mesin menyala.** WorkBuddy berjalan di mesin pengguna, jadi jadwal 05:00 tidak jalan kalau laptop mati.
- **Mindmap, unit audio microlearning, dan latihan soal terjadwal** belum ada. Peta versinya di `docs/roadmap-v1-v5.md` pada repo.
- **Tidak memeriksa kebenaran isi terhadap modul.** Reviewer memeriksa cakupan konsep dan aturan gaya. Manusia membaca penuh, tapi sedang belajar, jadi yang ditangkap adalah "ini nyambung atau tidak", bukan audit.
- **Tidak memutuskan hak tayang.** Artikel dipilih karena ekspresinya baru, bukan karena materinya bebas hak cipta. Keputusan tayang tetap milik manusia.

## Avatar

Sudah ada di `avatars/`. Kalau diganti: PNG, 512x512, maksimal 500KB per berkas.
