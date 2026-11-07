#!/usr/bin/env bash
# Tarik teks halaman landing dari repo kerja di Gitea, pasang ke situs, bangun ulang.
#
# Yang diedit Sari:  SariApps/tencent-hackathon  ->  docs/landing-page.md
# Yang dibaca build: site/pages/hackathon.md (salinan, jangan diedit langsung)
#
# Pakai dari root repo:  ./scripts/tarik-landing.sh
set -euo pipefail

REPO=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
KERJA=${KOPIPAGI_REPO_KERJA:-$REPO/../tencent-hackathon}
SUMBER="$KERJA/docs/landing-page.md"

[ -f "$SUMBER" ] || {
  echo "Tidak ketemu: $SUMBER"
  echo "Clone dulu: git clone http://43.134.103.31:58235/SariApps/tencent-hackathon.git $KERJA"
  exit 2
}

git -C "$KERJA" pull --ff-only --quiet
cp "$SUMBER" "$REPO/site/pages/hackathon.md"
echo "Teks landing ditarik dari Gitea: $(git -C "$KERJA" log -1 --format='%h, %ad' --date=format:'%d %b %H:%M' -- docs/landing-page.md)"

exec "$REPO/scripts/deploy-preview.sh"
