# Narasi video Kopi Pagi — naskah rekaman

Slide 1–5: verbatim tulisan Sari (dari `narasi-sari-v5.md`), tidak diubah.
Slide 6–11: lanjutan yang ditulis Wiz, mengikuti keputusan Sari 7 November
(solusi utuh dulu, roadmap dan status teknis belakangan, kenapa-kenapa di slide roadmap dan arsitektur).

Total 1.065 kata. Tempo santai 140 kata/menit = sekitar 8 menit; kalau bicara 150 kata/menit = sekitar 7 menit.
Kalau harus di bawah 7 menit, yang dipotong lebih dulu: daftar panjang di slide 5 (hemat 20 detik) dan
satu paragraf di slide 7 (hemat 20 detik). Jangan potong slide 9, itu satu-satunya tempat kamu mengaku salah.

---

## Slide 1 · Kopi Pagi · 24 kata, ±10 detik

Halo, nama saya sari. Siang saya kerja, malam saya kuliah. Dengan WorkBuddy, saya merancang ulang
materi belajar dari kampus, supaya bisa dipakai mahasiswa pekerja.

## Slide 2 · Ritme keseharian · 95 kata, ±41 detik

Ini ritme keseharian mahasiswa pekerja. Komuter pagi yang padat. Kerja delapan jam. Jam lima sore
keluar kantor kena macet. Yang WFH? Sama aja, sore buru-buru masak dan beresin rumah kayak takut
ketinggalan KRL. Sampai kelas jam setengah tujuh malam, kena hantam presentasi atau video materi dari
dosen, modul 30 halaman, pretest, kuis, tugas, forum, dan posttest. Butuh dua sampai tiga jam full
konsentrasi kalau mau selesai malam itu juga. And guess what? Batre otak saya udah 5% sejak jam tujuh.
Materi kuliah cuma numpang lewat kayak orang gajian. Hari ini masuk, besok udah nggak ada.

## Slide 3 · Ini masalah desain · 34 kata, ±15 detik

Ini masalah desain pembelajaran. Modul kuliah umumnya dirancang buat orang yang datang dengan badan
segar, kepala jernih, dan dua jam waktu luang. Bukan untuk mahasiswa pekerja seperti saya. Saya nggak
malas. Saya cuma capek.

## Slide 4 · Yang sudah dicoba · 111 kata, ±48 detik

Jadi saya pindahin jam belajar ke pagi hari. Antara jam lima sampai jam enam, sebelum siap-siap
ngantor. Saya butuh materi belajar yang bisa dibaca dan dimengerti dengan cepat. Saya masukin pdf
materinya ke notebooklm dan chatgpt. Dapet sih teks yang lebih pendek. Tapi ringkasan materi itu masih
bikin kening saya berkerut. Isinya kering dan penuh istilah asing, nggak peduli saya masih blank dan
bayangin super ego itu mungkin temannya superman. Nggak ada drama penerapan teori di dunia nyata yang
bikin saya relate dan peduli. Nggak ada kasus menarik yang bikin saya penasaran dan buka modul 30
halaman di tengah gencetan KRL buat nyari solusinya. Jadi saya membangun sistem ini di WorkBuddy.

## Slide 5 · Solusi: satu paket · 173 kata, ±74 detik

Ini bukan sekadar ringkasan. Saya mendesain ulang seluruh materi belajar agar bisa dikonsumsi
mahasiswa pekerja seperti saya. Saya kasih PDF materi ke expert Kopi Pagi di WorkBuddy. Dia akan
proses materi itu jadi beberapa bentuk.

Rangkuman dan mindmap materi dikirim lewat email. Artikel berupa cerita ditampilkan di WorkBuddy
untuk saya baca dan review. Kalau layak tayang, saya approve untuk dipublish ke blog. Audio materi
kuliah yang dipecah jadi beberapa unit kecil berdurasi 60 detik lengkap dengan transkripnya, yang
disave ke hp dan bisa saya dengar atau baca di KRL. Satu sesi materi bisa jadi beberapa audio yang
bisa saya dengar saat ngantri, saat makan siang, saat nunggu printer kantor selesai kerja, saat
tergencet di KRL. Kapan saja saya punya waktu satu menit di sela-sela kesibukan.

Latihan soal satu esai saat makan siang, dan lima pilihan ganda di penghujung hari, untuk memastikan
saya mengerti dan tetap ingat materi kuliahnya.

Semua bentuk ini satu paket, karena satu bentuk saja tidak menyelesaikan masalah tadi. Yang sudah
berjalan di WorkBuddy sekarang rangkuman dan artikel. Sisanya tahap berikutnya.

## Slide 6 · Roadmap · 90 kata, ±39 detik

Sekarang saya jujur soal urutan pengerjaannya.

Yang jalan hari ini dua. Rangkuman dikirim ke email saya tiap pagi. Artikelnya tayang di blog setelah
saya setujui. Itu v1, dan dua-duanya saya sorot kuning di gambar ini. Mindmap menyusul di v2, karena
dia butuh renderer sendiri. Audio microlearning di v3, satu sesi dipecah jadi beberapa unit satu
menit. Latihan soal di v4, dijadwalkan beberapa kali sehari, bukan ditumpuk di satu waktu.

Kenapa saya sebut yang belum ada? Supaya jelas, bukan supaya kelihatan lengkap. Saya lebih suka
bilang dua daripada pura-pura semuanya beres.

## Slide 7 · Desain arsitektur MVP · 142 kata, ±61 detik

Di dalam expert ini ada empat peran.

Susi menyusun rencana. Materi sesi ini dibahas apa saja, konsep mana yang dipakai, konsep mana yang
dibuang. Wena menulis. Pertama rangkuman, maksimal lima ratus kata. Baru setelah rangkuman lolos, dia
menulis artikel seribu sampai seribu lima ratus kata dari rangkuman itu, bukan dari PDF lagi. Yani
yang menolak. Dia tidak boleh bilang "kurang enak". Setiap penolakan harus menyebut nomor aturan. Kiki
yang mengatur urutan dan memegang gerbang.

Kenapa harus empat? Karena satu agent yang menulis dan menilai tulisannya sendiri tidak akan pernah
menolak. Kalau saya jadi penulis sekaligus penguji, semua tulisan saya lulus.

Dan yang paling penting: keputusan terakhir bukan di mesin. Rangkuman boleh langsung masuk email,
karena penerimanya saya sendiri, dan saya memang belum tahu materinya. Artikel tidak boleh tayang
sebelum saya baca utuh dan klik setuju. Gerbangnya di tangan manusia, bukan di reviewer.

## Slide 8 · Pembangunan · 82 kata, ±35 detik

Semuanya dibangun di WorkBuddy, dan caranya tidak lewat coding.

Saya ceritakan masalah saya: saya mahasiswa pekerja, materi kuliah menumpuk, saya butuh rangkuman dan
artikel cerita yang bisa dibaca jam lima pagi. WorkBuddy membuatkan expert-nya. Lalu saya pakai, dan
setiap kali hasilnya tidak sesuai, saya koreksi, dan koreksinya saya jadikan aturan.

Contohnya: penutup artikelnya punya dua pertanyaan. Saya bilang satu saja. Itu jadi aturan, dan
seterusnya jadi banyak aturan. Yang membuat hasilnya konsisten bukan prompt ajaib, tapi aturan yang
tertulis dan bisa ditegur.

## Slide 9 · Pengetesan · 96 kata, ±41 detik

Setiap kali expert-nya diubah, saya tes pakai Test Now di WorkBuddy. Saya jalankan satu sesi penuh,
dari PDF sampai tayang.

Di sini saya harus jujur: versi pertama salah. Expert-nya menulis artikel lalu langsung tayang. Tidak
ada yang menyerahkan artikel ke saya untuk dibaca, padahal itu justru inti produknya. Dari temuan itu
saya tambah pengecekan: artikel wajib dilampirkan, dan wajib menunggu persetujuan.

Satu lagi yang masih lolos dan saya catat: parafrase identitas. Kalau kata "dosen" saya ganti jadi
"pengajar asal Eropa yang mualaf", reviewernya belum tentu menangkap. Untuk sekarang itu saya akui
sebagai batas, bukan saya sembunyikan.

## Slide 10 · Implementasi · 75 kata, ±32 detik

Setelah lolos, expert-nya saya pakai. WorkBuddy membuatkan blog untuk tempat artikelnya tayang.
Jadwalnya Senin dan Kamis jam lima pagi, atau kapan pun saya minta. Artikel yang tayang sekarang
empat, semuanya Psikologi Anak, mulai sesi satu. Ada pencarian, ada daftar per mata kuliah.

Yang juga perlu saya sebut: jadwal jam lima itu jalan kalau laptop saya menyala. WorkBuddy hidup di
mesin saya, bukan di server. Saya tahu itu, dan saya tidak mau janji lebih dari itu.

## Slide 11 · Kesimpulan · 134 kata, ±57 detik

Jadi apa yang berubah buat saya? Dulu malam saya cuma bisa mengeluh, materi lewat begitu saja.
Sekarang jam lima pagi saya punya dua hal yang bisa dibaca dalam sepuluh menit. Rangkuman untuk
kerangkanya, artikel untuk alasan peduli.

Batasannya tiga. Pertama, agent hanya hidup saat mesin saya menyala. Kedua, yang diperiksa mesin
adalah cakupan konsep dan aturan gaya, bukan kebenaran isi. Manusia tetap membaca, tapi manusia itu
sedang belajar. Ketiga, tidak semua materi kuliah boleh tayang publik, jadi rangkuman lewat email dan
hanya artikel yang tampil di blog.

Kalau ini diteruskan, bentuk berikutnya bukan blog, tapi portal belajar dengan login. Semua ada di
satu tempat: rangkuman, artikel, audio, soal. Aman untuk materi kampus, dan tetap enak dibaca di KRL.

Ini MVP, jadi sengaja kecil. Tapi kecilnya bukan karena saya tidak tahu mau dibawa ke mana.

## Slide 12 · Penutup · 9 kata, ±4 detik

Terima kasih. Saya Sari Nursita, dan ini Kopi Pagi.
