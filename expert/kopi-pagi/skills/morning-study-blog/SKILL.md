---
name: morning-study-blog
description: Fetch a lecture session PDF from psy.cerivitas.com, convert it to readable text, then write the session rangkuman (sent to the reader's own email) before writing the morning article. Use whenever producing or regenerating a Kopi Pagi session.
---

# Morning Study Blog

Prosedur teknis untuk mengambil materi kuliah dan menulis blog pagi. Aturan suara & karakter ada di `references/character-sheet.md`; struktur artikel ada di `references/article-template.md`.

## 1. Lokasi kerja

Semua data pengguna disimpan di folder `study-blog/` pada direktori kerja (workspace), bukan di dalam paket expert:

```
study-blog/
├── profil.md            # siapa pembacanya, termasuk email_penerima
├── character-sheet.md   # salinan yang boleh diedit Sari
├── progress.md          # sesi mana yang sudah ditulis
├── log.md               # kontinuitas cerita (2-3 fakta per artikel)
├── rulebook.md          # salinan rulebook dari paket expert
├── cache/               # PDF + hasil konversi
├── rangkuman/           # rangkuman per sesi, dasar artikel dan isi email
├── draft/               # artikel menunggu persetujuan
├── blog/                # artikel jadi, .md
└── audit/               # log audit per sesi, .json
```

Kalau folder/file belum ada, salin dari `references/` (khusus `character-sheet.md`) lalu buat `progress.md` dan `log.md` kosong dengan header sederhana.

## 2. Peta kurikulum

`references/kurikulum-semester-1.md` memuat daftar 6 mata kuliah semester 1 beserta judul tiap sesi. Gunakan untuk:
- menentukan slug mata kuliah dari nama yang disebut Sari,
- mengecek apakah nomor sesi memang ada,
- menulis konteks "sesi ini bagian dari alur apa" di artikel.

Kalau Sari menyebut mata kuliah yang tidak ada di peta, tanyakan slug-nya atau cek `https://psy.cerivitas.com/content/semester-1/` (direktori terbuka, listing HTML).

## 3. Ambil materi

```bash
python skills/morning-study-blog/scripts/fetch_materi.py \
  --course pcps-101-psikologi-anak --sesi 4
```

Script akan:
1. mengunduh `materi.pdf` (wajib) dan `handout.pdf` (kalau ada) ke `study-blog/cache/<slug>/`,
2. mengonversinya jadi `.md` memakai `workbuddy-pdf`,
3. mencetak path hasil konversi.

Lalu **baca seluruh isi .md** sebelum menulis. Jangan hanya baca 1-2 paragraf pertama — bagian akhir transkrip biasanya berisi kesimpulan dosen, dan itu bahan terbaik untuk penutup artikel.

Kalau script gagal (404 / offline / konverter tidak ketemu), laporkan apa adanya. Jangan mengarang materi.

## 4. Pilih sudut cerita

Setelah baca materi, jawab 3 pertanyaan ini untuk dirimu sendiri:

1. **Satu ide inti sesi ini apa?** (kalau nggak bisa dijawab dalam satu kalimat, materinya belum cukup dipahami — baca ulang.)
2. **Ide ini muncul di kehidupan Raka yang mana?** Pilih dari character sheet: konflik kantor, keponakan, keluarga, atau kebiasaan harian.
3. **Apa yang bikin Sari "ohhh"?** Biasanya bukan definisi, tapi contoh yang dia alami sendiri.

Baru mulai menulis setelah tiga jawaban itu ada.

## 5. Tulis & simpan

- Path: `study-blog/blog/YYYY-MM-DD-<slug>-sesi-NN.md`
- Frontmatter ringan di atas artikel:

```markdown
---
mata_kuliah: Psikologi Anak (PCPS 101)
sesi: 4
tanggal: 2026-11-09
judul_materi: Metode-metode ilmu sosial dalam penelitian psikologi anak
kata: 1234
---
```

- Setelah menyimpan, perbarui:
  - `progress.md` — tandai sesi ini selesai + tanggal
  - `log.md` — tambahkan 2-3 fakta baru tentang Raka (proyek baru di kantor, umur keponakan, janji yang belum ditepati, dsb.)

## 6. Setelah menulis

Sampaikan ke Sari: judul, jumlah kata, sesi berikutnya, dan satu kalimat "besok gue mau cerita soal ...". Jangan minta maaf berlebihan kalau artikelnya panjang.

## 7. Daftar berkas yang wajib ikut berubah saat ada post baru

Satu sesi baru bukan cuma satu berkas. Kalau salah satu terlewat, situs jadi bohong: artikelnya ada tapi nggak muncul di daftar, atau kategori dan pencariannya ketinggalan.

| Berkas | Kenapa wajib |
|---|---|
| `study-blog/blog/YYYY-MM-DD-<slug>-sesi-NN.md` | artikelnya. Frontmatter **wajib** memuat `mata_kuliah` dan `sesi`; dari dua kolom itu halaman kategori `/kuliah/<slug>.html` dibentuk |
| `study-blog/rangkuman/YYYY-MM-DD-<slug>-sesi-NN.md` | rangkuman yang sudah dikirim ke email |
| `study-blog/audit/YYYY-MM-DD-sesi-NN.json` | bukti audit: putaran, `konsep_dipakai`, `konsep_dibuang`, siapa menyetujui |
| `study-blog/progress.md` | sesi berikutnya, supaya tidak dobel |
| `study-blog/log.md` | kontinuitas cerita untuk sesi berikutnya |
| `blog-site/dist/` | hasil build. Menjalankan `python blog-site/build.py` otomatis memperbarui **index, halaman kategori, dan `search.json`** |

Nama `mata_kuliah` harus **persis sama** dengan sesi sebelumnya (contoh: `Psikologi Anak`). Kalau beda satu kata, halaman kategorinya pecah jadi dua.

Setelah build, sebutkan di laporan satu baris: "situs dibangun ulang, indeks dan kategori ikut diperbarui". Kalau build gagal atau folder `blog-site/` tidak ada, jangan bilang sudah tayang.

## Referensi

- `references/character-sheet.md` — siapa Raka, cara ngomongnya, siapa saja orang di sekitarnya
- `references/kurikulum-semester-1.md` — peta 6 mata kuliah + judul sesi
- `references/article-template.md` — struktur, panjang tiap bagian, contoh suara
