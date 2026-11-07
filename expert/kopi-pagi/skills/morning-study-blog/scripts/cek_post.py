#!/usr/bin/env python3
"""Periksa satu artikel benar-benar ikut terbit di semua permukaan situs.

Jalankan setelah build. Memeriksa:

  1. frontmatter punya `mata_kuliah` dan `sesi`
  2. halaman artikelnya ada di dist/posts/
  3. muncul di halaman depan (index.html)
  4. muncul di halaman kategori mata kuliahnya (kuliah/<slug>.html)
  5. ada di indeks pencarian (search.json)
  6. kategori tidak pecah (nama mata kuliah sama tapi ditulis beda)

Pemakaian, dari folder kerja mana pun:

    python skills/morning-study-blog/scripts/cek_post.py
    python skills/morning-study-blog/scripts/cek_post.py sesi-03

Keluar dengan kode 1 kalau ada pemeriksaan yang gagal.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def calon_akar() -> list[Path]:
    akar = [Path.cwd()]
    akar += list(Path(__file__).resolve().parents)
    return akar


def cari_situs() -> Path | None:
    # Urutan rel di luar, akar di dalam: situs baru menang di akar mana pun
    # sebelum situs lama (blog-site) dipertimbangkan.
    for rel in ("site/dist", "kopi-pagi-repo/site/dist", "blog-site/dist", "dist"):
        for akar in calon_akar():
            kandidat = akar / rel
            if (kandidat / "index.html").exists():
                return kandidat
    return None


def cari_blog() -> Path | None:
    # study-blog/ (data pengguna) selalu menang atas samples/ (contoh repo),
    # walau cwd-nya ada di dalam repo.
    for rel in ("study-blog/blog", "samples/blog"):
        for akar in calon_akar():
            kandidat = akar / rel
            if kandidat.exists() and any(kandidat.glob("*.md")):
                return kandidat
    return None


def slugify(teks: str) -> str:
    teks = re.sub(r"[^a-z0-9\s-]", "", teks.lower().strip())
    return re.sub(r"\s+", "-", teks)


def baca_frontmatter(path: Path) -> dict[str, str]:
    teks = path.read_text(encoding="utf-8")
    if not teks.startswith("---"):
        return {}
    potong = teks.split("---", 2)
    if len(potong) < 3:
        return {}
    data: dict[str, str] = {}
    for baris in potong[1].strip().splitlines():
        if ":" in baris:
            kunci, nilai = baris.split(":", 1)
            data[kunci.strip()] = nilai.strip()
    return data


def pilih_berkas(folder: Path, potongan: str | None) -> Path:
    berkas = sorted(folder.glob("*.md"))
    if not berkas:
        sys.exit(f"Tidak ada .md di {folder}.")
    if potongan:
        cocok = [f for f in berkas if potongan in f.name]
        if not cocok:
            sys.exit(f"Tidak ada berkas yang cocok dengan '{potongan}' di {folder}.")
        return cocok[0]
    return max(berkas, key=lambda f: (f.stat().st_mtime, f.name))


def cek_kategori_pecah(folder: Path) -> list[str]:
    peta: dict[str, set[str]] = {}
    for f in folder.glob("*.md"):
        nama = baca_frontmatter(f).get("mata_kuliah", "").strip()
        if nama:
            peta.setdefault(slugify(nama), set()).add(nama)
    return [f"{s}: {', '.join(sorted(n))}" for s, n in peta.items() if len(n) > 1]


def main() -> int:
    potongan = sys.argv[1] if len(sys.argv) > 1 else None

    blog = cari_blog()
    if not blog:
        sys.exit("Tidak ada folder artikel (study-blog/blog atau samples/blog).")
    situs = cari_situs()
    if not situs:
        sys.exit("Situs belum dibangun (index.html tidak ditemukan). Jalankan build dulu.")

    berkas = pilih_berkas(blog, potongan)
    meta = baca_frontmatter(berkas)
    hasil: list[tuple[str, bool, str]] = []

    meta_ok = bool(meta.get("mata_kuliah")) and bool(meta.get("sesi"))
    hasil.append(
        (
            "frontmatter mata_kuliah + sesi",
            meta_ok,
            f"mata_kuliah={meta.get('mata_kuliah', '-')!r}, sesi={meta.get('sesi', '-')!r}",
        )
    )

    halaman = situs / "posts" / f"{berkas.stem}.html"
    hasil.append(("halaman artikel", halaman.exists(), str(halaman)))

    index = (situs / "index.html").read_text(encoding="utf-8")
    hasil.append(("muncul di halaman depan", berkas.stem in index, str(situs / "index.html")))

    kat_slug = slugify(meta.get("mata_kuliah", "")) if meta.get("mata_kuliah") else ""
    kat_file = situs / "kuliah" / f"{kat_slug}.html" if kat_slug else None
    kat_ok = bool(kat_file and kat_file.exists() and berkas.stem in kat_file.read_text(encoding="utf-8"))
    hasil.append(
        (
            "muncul di kategori mata kuliah",
            kat_ok,
            str(kat_file) if kat_file else "mata_kuliah kosong di frontmatter",
        )
    )

    try:
        indeks = json.loads((situs / "search.json").read_text(encoding="utf-8"))
        ada_cari = any(item.get("u") == f"posts/{berkas.stem}.html" for item in indeks)
        hasil.append(("terdaftar di pencarian", ada_cari, f"search.json ({len(indeks)} entri)"))
    except FileNotFoundError:
        hasil.append(("terdaftar di pencarian", False, "search.json tidak ada"))

    pecah = cek_kategori_pecah(blog)
    hasil.append(
        ("kategori tidak pecah", not pecah, "; ".join(pecah) if pecah else "nama mata kuliah konsisten")
    )

    print(f"Artikel : {berkas.name}")
    print(f"Judul   : {meta.get('judul_materi', '-')}")
    print("")
    gagal = 0
    for nama, lolos, catatan in hasil:
        print(f"[{'LULUS' if lolos else 'GAGAL'}] {nama} · {catatan}")
        if not lolos:
            gagal += 1

    print("")
    if gagal:
        print(f"{gagal} pemeriksaan gagal. Jangan bilang sudah tayang sebelum beres.")
        return 1
    print("Semua pemeriksaan lolos. Artikel ikut terbit di depan, kategori, dan pencarian.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
