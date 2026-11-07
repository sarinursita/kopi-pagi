#!/usr/bin/env bash
# Periksa artikel baru benar-benar ikut terbit di depan, kategori, dan pencarian.
# Satu sumber logika ada di paket expert supaya ikut terbawa saat zip:
#   expert/kopi-pagi/skills/morning-study-blog/scripts/cek_post.py
set -euo pipefail
REPO=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
exec python3 "$REPO/expert/kopi-pagi/skills/morning-study-blog/scripts/cek_post.py" "$@"
