#!/usr/bin/env python3
"""Bangun situs statis dari study-blog/blog/*.md.

Jalankan dari mana saja:
    python blog-site/build.py

Hasil: blog-site/dist/ (index.html + posts/*.html)
"""

from __future__ import annotations

import html
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT.parent / "study-blog" / "blog"
DIST = ROOT / "dist"

SITE_TITLE = "Kopi Pagi"
SITE_TAGLINE = "Ngopi dulu, baru kuliah. Catatan pagi seorang mahasiswa yang kuliah sambil kerja: satu sesi, satu cerita, satu kopi."
SITE_DESC = "Blog belajar psikologi anak, ditulis jam 5 pagi sebelum berangkat kerja."

MONTHS = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni",
    7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember",
}


# ---------------------------------------------------------------- frontmatter

def parse_front(text: str) -> tuple[dict, str]:
    meta: dict[str, str] = {}
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].strip().splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip()
            body = parts[2]
    return meta, body.strip()


def fmt_date(iso: str) -> str:
    try:
        d = datetime.strptime(iso, "%Y-%m-%d")
        return f"{d.day} {MONTHS[d.month]} {d.year}"
    except ValueError:
        return iso


# ---------------------------------------------------------------- markdown

def inline(s: str) -> str:
    s = html.escape(s, quote=False)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


def md_to_html(md: str) -> str:
    out: list[str] = []
    buf: list[str] = []
    in_list = False

    def flush_para() -> None:
        if buf:
            out.append("<p>" + inline(" ".join(buf).strip()) + "</p>")
            buf.clear()

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    for raw in md.splitlines():
        line = raw.rstrip()
        if not line.strip():
            flush_para()
            close_list()
            continue
        if line.startswith("# "):
            flush_para(); close_list()
            continue  # judul sudah dipakai di header halaman
        if line.startswith("### "):
            flush_para(); close_list()
            out.append("<h3>" + inline(line[4:]) + "</h3>")
        elif line.startswith("## "):
            flush_para(); close_list()
            out.append("<h2>" + inline(line[3:]) + "</h2>")
        elif line.startswith("> "):
            flush_para(); close_list()
            out.append("<blockquote>" + inline(line[2:]) + "</blockquote>")
        elif re.match(r"^[-*] ", line):
            flush_para()
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append("<li>" + inline(line[2:]) + "</li>")
        elif line.strip() in ("---", "***"):
            flush_para(); close_list()
            out.append("<hr>")
        else:
            close_list()
            buf.append(line)
    flush_para()
    close_list()
    return "\n".join(out)


def plain(md: str, limit: int = 190) -> str:
    t = re.sub(r"[#>*`_]", "", md)
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t[:limit].rsplit(" ", 1)[0] + "..." if len(t) > limit else t


# ---------------------------------------------------------------- template

CSS = """
:root{
  --ink:#1d1a16; --muted:#6f665c; --paper:#fbf8f3; --card:#ffffff;
  --line:#e7e0d5; --accent:#a8462a; --accent-soft:#f3e4dd;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; background:var(--paper); color:var(--ink);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  font-size:18px; line-height:1.75;
}
a{color:var(--accent); text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:720px; margin:0 auto; padding:0 24px}

header.site{padding:56px 0 40px; border-bottom:1px solid var(--line)}
header.site .kicker{font-size:13px; letter-spacing:.14em; text-transform:uppercase; color:var(--accent); font-weight:600; margin-bottom:14px}
header.site h1{
  font-family:Georgia,"Times New Roman",serif; font-size:clamp(30px,5vw,44px);
  line-height:1.15; margin:0 0 12px; letter-spacing:-.02em;
}
header.site p{margin:0; color:var(--muted); font-size:17px; max-width:52ch}

.list{padding:16px 0 8px}
.post-card{
  display:block; padding:26px 0; border-bottom:1px solid var(--line);
  color:inherit;
}
.post-card:hover{text-decoration:none}
.post-card:hover h2{color:var(--accent)}
.post-meta{font-size:13px; color:var(--muted); letter-spacing:.02em; margin-bottom:8px}
.post-meta .dot{margin:0 8px; opacity:.5}
.post-card h2{
  font-family:Georgia,"Times New Roman",serif; font-size:24px; line-height:1.3;
  margin:0 0 8px; letter-spacing:-.01em; transition:color .15s;
}
.post-card p{margin:0; color:var(--muted); font-size:16px}

article{padding:48px 0 24px}
article .post-meta{margin-bottom:18px}
article h1{
  font-family:Georgia,"Times New Roman",serif; font-size:clamp(28px,4.6vw,40px);
  line-height:1.2; letter-spacing:-.02em; margin:0 0 18px;
}
article .lede{border-left:3px solid var(--accent-soft); padding-left:16px; color:var(--muted); font-style:italic}
article h2{
  font-family:Georgia,"Times New Roman",serif; font-size:23px; line-height:1.35;
  margin:44px 0 12px; letter-spacing:-.01em;
}
article h3{font-size:19px; margin:32px 0 10px}
article p{margin:0 0 20px}
article ul{margin:0 0 20px; padding-left:22px}
article li{margin-bottom:8px}
article blockquote{
  margin:26px 0; padding:16px 20px; background:var(--card);
  border-left:3px solid var(--accent); border-radius:0 6px 6px 0;
  color:var(--muted); font-style:italic;
}
article hr{border:0; border-top:1px solid var(--line); margin:36px 0}
article code{background:var(--accent-soft); padding:1px 5px; border-radius:4px; font-size:.9em}
article strong{font-weight:650}

.pager{display:flex; justify-content:space-between; gap:16px; margin:44px 0 0; padding-top:24px; border-top:1px solid var(--line); font-size:15px}
.pager a{max-width:48%}
.pager .lbl{display:block; font-size:12px; color:var(--muted); letter-spacing:.08em; text-transform:uppercase; margin-bottom:4px}

.about{margin:52px 0 0; padding:28px; background:var(--card); border:1px solid var(--line); border-radius:10px}
.about h2{font-family:Georgia,serif; font-size:19px; margin:0 0 10px}
.about p{margin:0 0 10px; color:var(--muted); font-size:16px}
.about p:last-child{margin-bottom:0}
.about ul.cast{list-style:none; margin:0 0 26px; padding:0; font-size:16px; color:var(--muted)}
.about ul.cast li{padding:7px 0; border-bottom:1px dashed var(--line)}
.about ul.cast li:last-child{border-bottom:0}
.about ul.cast strong{color:var(--ink); font-weight:650}

footer.site{margin-top:64px; padding:28px 0 56px; border-top:1px solid var(--line); color:var(--muted); font-size:14px}
.back{display:inline-block; margin-bottom:26px; font-size:15px}
@media (max-width:560px){
  body{font-size:17px}
  header.site{padding:40px 0 30px}
  article{padding:32px 0 16px}
}
"""


def page(title: str, desc: str, body: str, root: str = "") -> str:
    return f"""<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="article">
<link rel="stylesheet" href="{root}style.css">
</head>
<body>
<div class="wrap">
{body}
</div>
</body>
</html>
"""


# ---------------------------------------------------------------- build

def main() -> int:
    files = sorted(SRC.glob("*.md"))
    posts = []
    for f in files:
        meta, body = parse_front(f.read_text(encoding="utf-8"))
        m = re.search(r"^#\s+(.+)$", body, re.M)
        title = m.group(1).strip() if m else f.stem
        posts.append({
            "slug": f.stem,
            "title": title,
            "date": meta.get("tanggal", f.stem[:10]),
            "course": meta.get("mata_kuliah", ""),
            "session": meta.get("sesi", ""),
            "topic": meta.get("judul_materi", ""),
            "body": body,
            "excerpt": plain(re.sub(r"^#.*$", "", body, count=1, flags=re.M)),
        })

    posts.sort(key=lambda p: (p["date"], p["session"]), reverse=True)

    DIST.mkdir(parents=True, exist_ok=True)
    (DIST / "posts").mkdir(exist_ok=True)
    (DIST / "style.css").write_text(CSS, encoding="utf-8")

    # ---- index
    cards = []
    for p in posts:
        meta_bits = [fmt_date(p["date"])]
        if p["course"]:
            meta_bits.append(f'{p["course"]}, sesi {p["session"]}')
        meta_html = '<span class="dot">·</span>'.join(html.escape(b) for b in meta_bits)
        cards.append(
            f'<a class="post-card" href="posts/{p["slug"]}.html">'
            f'<div class="post-meta">{meta_html}</div>'
            f'<h2>{html.escape(p["title"])}</h2>'
            f'<p>{html.escape(p["excerpt"])}</p></a>'
        )

    about = """<div class="about">
<h2>Siapa yang nulis ini</h2>
<p>Gue Raka, 24. Kuliah Psikologi Islam semester satu sambil kerja di distributor kecil di Bandung. Belajar malem udah nggak masuk, jadi gue pindah ke pagi: baca materi hari itu, terus gue tulis ulang jadi cerita yang gue sendiri ngerti.</p>

<h2>Orang-orang yang bakal sering muncul</h2>
<ul class="cast">
<li><strong>Sinta</strong> &middot; rekan kerja, mejanya sebelah gue</li>
<li><strong>Pak Yanto</strong> &middot; bos gue</li>
<li><strong>Mba Ratna</strong> &middot; kakak gue</li>
<li><strong>Nadia, Bima, Aya</strong> &middot; tiga keponakan gue, umur 7, 4, dan belum 2</li>
<li><strong>Bu Alina</strong> &middot; dosen kelas ini</li>
</ul>

<h2>Cara baca blog ini</h2>
<p>Episodik. Lo bisa mulai dari tulisan mana pun, nggak harus urut dari yang paling awal. Tiap tulisan berdiri sendiri.</p>

<h2>Soal nama</h2>
<p>Semua nama orang, kampus, dan dosen di sini gue samarkan. Isi materinya tetap sesuai modul, cuma cara nyampeinnya yang gue bikin kayak ngobrol.</p>
</div>"""

    body = f"""<header class="site">
<div class="kicker">Study in public</div>
<h1>{html.escape(SITE_TITLE)}</h1>
<p>{html.escape(SITE_TAGLINE)}</p>
</header>
<main class="list">
{''.join(cards) if cards else '<p style="color:#6f665c">Belum ada artikel.</p>'}
</main>
{about}
<footer class="site">Ditulis tiap pagi sebelum berangkat kerja.</footer>"""

    (DIST / "index.html").write_text(page(SITE_TITLE, SITE_DESC, body), encoding="utf-8")

    # ---- posts
    for i, p in enumerate(posts):
        newer = posts[i - 1] if i > 0 else None
        older = posts[i + 1] if i + 1 < len(posts) else None
        pager = '<div class="pager">'
        pager += (
            f'<a href="{newer["slug"]}.html"><span class="lbl">Lebih baru</span>{html.escape(newer["title"])}</a>'
            if newer else "<span></span>"
        )
        pager += (
            f'<a href="{older["slug"]}.html" style="text-align:right"><span class="lbl">Sebelumnya</span>{html.escape(older["title"])}</a>'
            if older else "<span></span>"
        )
        pager += "</div>"

        meta_bits = [fmt_date(p["date"])]
        if p["course"]:
            meta_bits.append(f'{p["course"]}, sesi {p["session"]}')
        meta_html = '<span class="dot">·</span>'.join(html.escape(b) for b in meta_bits)

        topic = f'<p class="lede">{html.escape(p["topic"])}</p>' if p["topic"] else ""

        content = f"""<a class="back" href="../index.html">&larr; Semua tulisan</a>
<article>
<div class="post-meta">{meta_html}</div>
<h1>{html.escape(p["title"])}</h1>
{topic}
{md_to_html(p["body"])}
{pager}
</article>
<footer class="site">Nama orang dan lembaga di tulisan ini sudah disamarkan.</footer>"""

        (DIST / "posts" / f'{p["slug"]}.html').write_text(
            page(p["title"], p["excerpt"], content, root="../"), encoding="utf-8"
        )

    # ---- single-file version (semua artikel dalam satu .html, CSS inline)
    toc = "".join(
        f'<li><a href="#{p["slug"]}">{html.escape(p["title"])}</a>'
        f'<span class="toc-date">{fmt_date(p["date"])}</span></li>'
        for p in posts
    )
    sections = []
    for p in posts:
        meta_bits = [fmt_date(p["date"])]
        if p["course"]:
            meta_bits.append(f'{p["course"]}, sesi {p["session"]}')
        meta_html = '<span class="dot">·</span>'.join(html.escape(b) for b in meta_bits)
        topic = f'<p class="lede">{html.escape(p["topic"])}</p>' if p["topic"] else ""
        sections.append(
            f'<section id="{p["slug"]}"><article><div class="post-meta">{meta_html}</div>'
            f'<h1>{html.escape(p["title"])}</h1>{topic}{md_to_html(p["body"])}</article></section>'
        )

    single_css = CSS + """
.toc{margin:28px 0 8px; padding:0; list-style:none}
.toc li{display:flex; justify-content:space-between; gap:16px; padding:12px 0; border-bottom:1px solid var(--line)}
.toc a{font-family:Georgia,serif; font-size:18px}
.toc-date{color:var(--muted); font-size:14px; white-space:nowrap}
section{scroll-margin-top:24px}
section + section{margin-top:56px; padding-top:40px; border-top:1px solid var(--line)}
"""

    single = f"""<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(SITE_TITLE)}</title>
<meta name="description" content="{html.escape(SITE_DESC)}">
<style>{single_css}</style>
</head>
<body>
<div class="wrap">
<header class="site">
<div class="kicker">Study in public</div>
<h1>{html.escape(SITE_TITLE)}</h1>
<p>{html.escape(SITE_TAGLINE)}</p>
</header>
<ul class="toc">{toc}</ul>
{''.join(sections)}
<footer class="site">Nama orang dan lembaga di tulisan ini sudah disamarkan.</footer>
</div>
</body>
</html>
"""
    (DIST / "standalone.html").write_text(single, encoding="utf-8")

    print(f"OK: {len(posts)} artikel -> {DIST}")
    print(f"    index.html, posts/*.html, standalone.html (satu file, bisa dikirim langsung)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
