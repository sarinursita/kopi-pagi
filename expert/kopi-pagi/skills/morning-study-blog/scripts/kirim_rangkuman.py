#!/usr/bin/env python3
"""Kirim rangkuman sesi ke email pribadi pengguna.

Dipakai oleh tim Kopi Pagi setelah rangkuman lolos R12. Rangkuman tidak
ditayangkan ke publik, jadi jalur ini sengaja bukan kanal dan bukan situs.

Konfigurasi lewat variabel lingkungan (jangan taruh password di berkas ini):

    KOPIPAGI_SMTP_HOST   contoh: smtp.gmail.com
    KOPIPAGI_SMTP_PORT   465 (SSL) atau 587 (STARTTLS). Default 465.
    KOPIPAGI_SMTP_USER   alamat email pengirim
    KOPIPAGI_SMTP_PASS   kata sandi aplikasi, bukan kata sandi akun
    KOPIPAGI_SMTP_FROM   opsional, kalau berbeda dari SMTP_USER

Pemakaian:

    python kirim_rangkuman.py --to aku@contoh.com \
        --subject "Rangkuman Psikologi Anak sesi 1 · 2026-11-07" \
        --file study-blog/rangkuman/2026-11-07-pcps-101-sesi-01.md

Aturan penting: kalau konfigurasi belum ada, skrip ini keluar dengan kode 2
dan pesan jelas. Jangan pernah mengaku email sudah terkirim kalau belum.
"""

from __future__ import annotations

import argparse
import os
import smtplib
import ssl
import sys
from email.message import EmailMessage
from pathlib import Path


def ambil_konfigurasi() -> dict[str, str]:
    wajib = ["KOPIPAGI_SMTP_HOST", "KOPIPAGI_SMTP_USER", "KOPIPAGI_SMTP_PASS"]
    hilang = [k for k in wajib if not os.environ.get(k)]
    if hilang:
        print(
            "Email belum dikonfigurasi. Variabel yang belum ada: "
            + ", ".join(hilang)
            + "\nSet dulu di lingkungan tempat expert berjalan, lalu ulangi. "
            "Rangkuman tetap tersimpan sebagai berkas dan bisa dikirim manual."
        )
        sys.exit(2)

    user = os.environ["KOPIPAGI_SMTP_USER"]
    return {
        "host": os.environ["KOPIPAGI_SMTP_HOST"],
        "port": os.environ.get("KOPIPAGI_SMTP_PORT", "465"),
        "user": user,
        "password": os.environ["KOPIPAGI_SMTP_PASS"],
        "sender": os.environ.get("KOPIPAGI_SMTP_FROM", user),
    }


def baca_berkas(path: Path) -> str:
    if not path.exists():
        print(f"Berkas rangkuman tidak ditemukan: {path}")
        sys.exit(3)
    teks = path.read_text(encoding="utf-8")
    if not teks.strip():
        print(f"Berkas rangkuman kosong: {path}")
        sys.exit(3)
    return teks


def buang_frontmatter(teks: str) -> str:
    if teks.startswith("---"):
        bagian = teks.split("---", 2)
        if len(bagian) == 3:
            return bagian[2].lstrip("\n")
    return teks


def kirim(konfig: dict[str, str], ke: str, subjek: str, isi: str) -> None:
    pesan = EmailMessage()
    pesan["From"] = konfig["sender"]
    pesan["To"] = ke
    pesan["Subject"] = subjek
    pesan.set_content(isi)

    port = int(konfig["port"])
    konteks = ssl.create_default_context()
    if port == 465:
        with smtplib.SMTP_SSL(konfig["host"], port, context=konteks, timeout=30) as server:
            server.login(konfig["user"], konfig["password"])
            server.send_message(pesan)
    else:
        with smtplib.SMTP(konfig["host"], port, timeout=30) as server:
            server.starttls(context=konteks)
            server.login(konfig["user"], konfig["password"])
            server.send_message(pesan)


def main() -> int:
    ap = argparse.ArgumentParser(description="Kirim rangkuman sesi ke email pribadi.")
    ap.add_argument("--to", required=True, help="alamat email penerima")
    ap.add_argument("--subject", required=True, help="subjek email, format baku per sesi")
    ap.add_argument("--file", required=True, help="berkas markdown rangkuman")
    args = ap.parse_args()

    konfig = ambil_konfigurasi()
    isi = buang_frontmatter(baca_berkas(Path(args.file)))
    kirim(konfig, args.to, args.subject, isi)
    print(f"Rangkuman terkirim ke {args.to} dengan subjek: {args.subject}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
