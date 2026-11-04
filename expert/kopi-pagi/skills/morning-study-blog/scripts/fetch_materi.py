#!/usr/bin/env python3
"""Ambil materi kuliah dari psy.cerivitas.com dan konversi ke teks.

Contoh:
    python fetch_materi.py --course pcps-101-psikologi-anak --sesi 4
    python fetch_materi.py --course pcps-101-psikologi-anak --sesi 6 --out study-blog/cache

Hasil:
    <out>/<slug>/sesi-04/materi.pdf
    <out>/<slug>/sesi-04/materi.md
    <out>/<slug>/sesi-04/handout.md   (kalau ada)

Kalau file .md sudah ada dan --force tidak dipakai, unduhan dilewati.
"""

from __future__ import annotations

import argparse
import glob
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

BASE = "https://psy.cerivitas.com/content/semester-1/{course}/sesi-{sesi:02d}/{name}.pdf"
UA = "Mozilla/5.0 (compatible; morning-study-blog/1.0)"


def find_converter() -> list[str] | None:
    """Cari binary konverter PDF -> markdown."""
    env = os.environ.get("WORKBUDDY_PDF_BIN")
    if env and Path(env).exists():
        return [env]
    for name in ("workbuddy-pdf", "workbuddy-pdf.exe"):
        hit = shutil.which(name)
        if hit:
            return [hit]
    home = Path.home()
    patterns = [
        home / ".workbuddy-ai" / "external-packages" / "pdf-cli" / "workbuddy-pdf.exe",
        home / ".workbuddy-ai" / "external-packages" / "pdf-cli" / "workbuddy-pdf",
    ]
    for p in patterns:
        if p.exists():
            return [str(p)]
    for p in glob.glob(str(home / ".workbuddy-ai" / "external-packages" / "**" / "workbuddy-pdf*"), recursive=True):
        if Path(p).is_file():
            return [p]
    if shutil.which("pdftotext"):
        return None  # pakai fallback
    return []


def download(url: str, dest: Path) -> bool:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False
        raise
    if not data.startswith(b"%PDF"):
        print(f"  ! bukan PDF: {url}", file=sys.stderr)
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return True


def convert(pdf: Path, md: Path, conv: list[str] | None) -> bool:
    if conv is None:
        r = subprocess.run(["pdftotext", str(pdf), str(md)], capture_output=True)
        return r.returncode == 0
    r = subprocess.run(conv + [str(pdf), str(md), "--format", "md-plain"], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  ! konversi gagal: {r.stderr.strip()[:400]}", file=sys.stderr)
        return False
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--course", required=True, help="slug mata kuliah, mis. pcps-101-psikologi-anak")
    ap.add_argument("--sesi", required=True, type=int, help="nomor sesi (1-30)")
    ap.add_argument("--out", default="study-blog/cache", help="folder cache (default: study-blog/cache)")
    ap.add_argument("--force", action="store_true", help="unduh ulang walau sudah ada")
    args = ap.parse_args()

    conv = find_converter()
    if conv == []:
        print("ERROR: konverter PDF tidak ketemu. Set env WORKBUDDY_PDF_BIN atau install pdftotext.", file=sys.stderr)
        return 2

    outdir = Path(args.out) / args.course / f"sesi-{args.sesi:02d}"
    outdir.mkdir(parents=True, exist_ok=True)

    produced: list[Path] = []
    for name in ("materi", "handout"):
        url = BASE.format(course=args.course, sesi=args.sesi, name=name)
        pdf = outdir / f"{name}.pdf"
        md = outdir / f"{name}.md"

        if md.exists() and not args.force:
            print(f"[skip] {md} (sudah ada)")
            produced.append(md)
            continue

        if not (pdf.exists() and not args.force):
            print(f"[get ] {url}")
            try:
                ok = download(url, pdf)
            except Exception as e:  # noqa: BLE001
                print(f"  ! gagal unduh: {e}", file=sys.stderr)
                ok = False
            if not ok:
                if name == "materi":
                    print("ERROR: materi.pdf tidak tersedia untuk sesi ini.", file=sys.stderr)
                    return 1
                print("  (handout tidak ada, dilewati)")
                continue
        else:
            print(f"[cached] {pdf}")

        print(f"[conv] {pdf.name} -> {md.name}")
        if not convert(pdf, md, conv):
            if name == "materi":
                return 1
            # handout sering berupa slide hasil ekspor gambar (tanpa layer teks),
            # jadi gagal konversi bukan alasan untuk membatalkan artikel.
            print("  (handout tanpa layer teks / gagal dikonversi, dilewati)")
            continue
        produced.append(md)

    print("\nSELESAI. Baca file berikut sebelum menulis:")
    for p in produced:
        print(f"  {p}  ({p.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
