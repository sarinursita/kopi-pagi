#!/usr/bin/env bash
# Bangun ulang situs lalu salin ke folder yang disajikan pratinjau di VPS.
# Pratinjau: http://43.134.103.31:58296/  (container nginx "kopipagi-site")
#
# Pakai dari root repo:  ./scripts/deploy-preview.sh
set -euo pipefail

REPO=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
TUJUAN=${KOPIPAGI_PREVIEW_DIR:-/home/saristudio/sites/kopipagi}

python3 "$REPO/site/build.py"

# Jangan deploy kalau artikel terbaru tidak benar-benar ikut terbit.
if [ "${SKIP_CEK:-0}" != "1" ]; then
  python3 "$REPO/expert/kopi-pagi/skills/morning-study-blog/scripts/cek_post.py" || {
    echo "Pemeriksaan gagal. Deploy dibatalkan (pakai SKIP_CEK=1 kalau memang mau memaksa)."
    exit 1
  }
fi

rsync -a --delete "$REPO/site/dist/" "$TUJUAN/"

if docker ps --format '{{.Names}}' | grep -qx kopipagi-site; then
  docker restart kopipagi-site >/dev/null
  echo "Pratinjau diperbarui: http://43.134.103.31:58296/"
else
  echo "Folder sudah disalin ke $TUJUAN, tapi container kopipagi-site tidak jalan."
  echo "Jalankan: docker run -d --name kopipagi-site --restart unless-stopped -p 58296:80 -v $TUJUAN:/usr/share/nginx/html:ro nginx:alpine"
fi
