#!/usr/bin/env python3
"""Bangun situs statis dari study-blog/blog/*.md.

Jalankan dari mana saja:
    python blog-site/build.py

Hasil: blog-site/dist/ (index.html + posts/*.html)
"""

from __future__ import annotations

import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def pilih_sumber() -> Path:
    """Folder artikel: workspace WorkBuddy dulu, lalu contoh di repo.

    Repo ini di-clone bersih oleh juri, dan folder study-blog/ tidak ikut
    karena itu data pengguna. Tanpa cadangan ini, build menghasilkan situs
    kosong dan terbaca sebagai proyek mati.
    """
    kandidat = [
        ROOT.parent / "study-blog" / "blog",
        # Repo sering ditaruh satu tingkat di dalam folder kerja (mis.
        # Claw/kopi-pagi-repo), sementara study-blog/ ada di folder kerja.
        # Tanpa cadangan ini, build diam-diam memakai samples/ dan artikel
        # yang baru di-approve tidak pernah muncul di situs.
        ROOT.parent.parent / "study-blog" / "blog",
        ROOT.parent / "samples" / "blog",
    ]
    for kandidat_dir in kandidat:
        if kandidat_dir.exists() and any(kandidat_dir.glob("*.md")):
            return kandidat_dir
    return kandidat[0]


SRC = pilih_sumber()
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


def slugify(teks: str) -> str:
    teks = re.sub(r"[^a-z0-9\s-]", "", teks.lower().strip())
    return re.sub(r"\s+", "-", teks)


def meta_baris(post: dict, prefix: str = "") -> str:
    bits = [f'<span>{html.escape(fmt_date(post["date"]))}</span>']
    if post.get("course"):
        slug = slugify(post["course"])
        sesi = html.escape(str(post.get("session", "")))
        bits.append(f'<a href="{prefix}kuliah/{slug}.html">{html.escape(post["course"])}</a>, sesi {sesi}')
    return '<span class="dot">·</span>'.join(bits)


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
  --ink:#2b2620; --muted:#6f6459; --desk:#e7ddcc; --paper:#fdfaf2; --rule:#dbe6f1;
  --margin:#e8a79c; --accent:#b04a2b; --high:#ffe98c; --note:#fff9c9; --tape:rgba(255,255,255,.62);
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; color:var(--ink);
  background:
    radial-gradient(1200px 600px at 50% -10%, #f4ecdd 0%, transparent 70%),
    var(--desk);
  font-family:"Nunito",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;
  font-size:18px; line-height:32px;
}
a{color:var(--accent); text-decoration:none}
a:hover{text-decoration:underline}

/* kertas buku catatan */
.wrap{
  max-width:800px; margin:32px auto; padding:52px 46px 44px 104px;
  background-color:var(--paper);
  background-image:repeating-linear-gradient(to bottom, transparent 0 31px, var(--rule) 31px 32px);
  border-radius:3px 6px 6px 3px; position:relative;
  box-shadow:0 20px 44px rgba(74,55,32,.20), 0 1px 0 #fff inset;
}
.wrap::before{ /* lubang spiral */
  content:""; position:absolute; left:0; top:0; bottom:0; width:64px;
  border-radius:3px 0 0 3px;
  background-image:radial-gradient(circle at 26px 50%, #cfc3ae 0 7px, #b9ab93 7px 8px, transparent 8.5px);
  background-size:64px 52px; background-repeat:repeat-y; background-position:0 26px;
  box-shadow:inset -10px 0 14px -12px rgba(80,60,30,.35);
}
.wrap::after{ /* garis margin merah */
  content:""; position:absolute; left:88px; top:0; bottom:0; width:2px;
  background:var(--margin); opacity:.55;
}

header.site{padding:0 0 24px}
header.site .kicker{
  font-family:"Caveat",cursive; font-size:24px; color:var(--accent);
  display:block; margin:0 0 2px; transform:rotate(-1.5deg); transform-origin:left center;
}
header.site h1{
  font-family:"Caveat",cursive; font-weight:700; font-size:clamp(44px,8vw,70px);
  line-height:1.02; margin:0; display:inline; padding:0 8px 2px 0;
  background-image:linear-gradient(transparent 58%, var(--high) 58%, var(--high) 90%, transparent 90%);
  background-repeat:no-repeat; background-size:100% 100%;
}
header.site p{margin:14px 0 0; color:var(--muted); font-size:17px}

/* catatan tempel: about */
.note{
  position:relative; margin:6px 0 30px; padding:20px 22px 16px;
  background:var(--note); border-radius:2px; transform:rotate(-.6deg);
  box-shadow:0 8px 18px rgba(90,70,40,.16), 0 1px 0 rgba(255,255,255,.7) inset;
}
.note::before{ /* selotip */
  content:""; position:absolute; top:-13px; left:50%; transform:translateX(-50%) rotate(-2.5deg);
  width:132px; height:26px; background:var(--tape);
  box-shadow:0 1px 4px rgba(90,70,40,.14);
  border-left:1px dashed rgba(120,100,60,.15); border-right:1px dashed rgba(120,100,60,.15);
}
.note h2{font-family:"Caveat",cursive; font-size:31px; line-height:1.1; margin:0 0 8px}
.note p{margin:0 0 10px; font-size:16px; line-height:26px; color:#4a4136}
.note p:last-child{margin-bottom:0}
.note ul.cast{list-style:none; margin:0 0 14px; padding:0; font-size:16px; line-height:26px; color:#4a4136}
.note ul.cast li{padding:3px 0; border-bottom:1px dashed rgba(120,100,60,.25)}
.note ul.cast li:last-child{border-bottom:0}
.note ul.cast strong{color:var(--ink)}

.list{padding:0}
.list-head{font-family:"Caveat",cursive; font-size:29px; margin:0 0 2px; line-height:1.2}
.list-head span{font-family:"Nunito",sans-serif; font-size:12px; letter-spacing:.12em; text-transform:uppercase; color:var(--muted); margin-left:8px}
.post-card{display:block; padding:14px 0 14px 34px; position:relative; color:inherit; border-bottom:1px dashed rgba(120,100,60,.28)}
.post-card::before{ /* kotak centang */
  content:""; position:absolute; left:4px; top:23px; width:13px; height:13px;
  border:1.5px solid #bfae92; border-radius:3px; transform:rotate(-3deg);
}
.post-card h2 a{color:inherit; text-decoration:none}
.post-card:hover h2 a{color:var(--accent)}
.post-meta{font-size:13px; line-height:20px; color:var(--muted); letter-spacing:.02em; margin-bottom:2px}
.post-meta .dot{margin:0 7px; opacity:.5}
.post-card h2{font-family:"Caveat",cursive; font-size:30px; line-height:1.15; margin:0 0 2px; transition:color .15s}
.post-card p{margin:0; font-size:16px; line-height:25px; color:var(--muted)}

article{padding:6px 0 10px}
article .post-meta{margin-bottom:6px}
article h1{font-family:"Caveat",cursive; font-weight:700; font-size:clamp(34px,6vw,52px); line-height:1.08; margin:0 0 6px}
article .lede{color:var(--muted); font-style:italic; margin:0 0 20px; padding-left:14px; border-left:3px solid var(--high)}
article h2{font-family:"Caveat",cursive; font-size:32px; line-height:1.15; margin:34px 0 4px}
article h3{font-family:"Caveat",cursive; font-size:26px; margin:26px 0 2px}
article p{margin:0 0 16px}
article ul,article ol{margin:0 0 16px; padding-left:24px}
article li{margin-bottom:4px}
article blockquote{
  margin:20px 0; padding:14px 18px; background:rgba(255,249,201,.75); color:#4a4136;
  border-radius:2px; transform:rotate(-.35deg); box-shadow:0 6px 14px rgba(90,70,40,.12);
  font-style:italic;
}
article hr{border:0; border-top:1px dashed rgba(120,100,60,.3); margin:28px 0}
article code{background:#efe7d6; padding:1px 5px; border-radius:4px; font-size:.9em}
article strong{font-weight:700}

.pager{display:flex; justify-content:space-between; gap:16px; margin:34px 0 0; padding-top:18px; font-size:15px; line-height:22px; border-top:1px dashed rgba(120,100,60,.3)}
.pager a{max-width:48%}
.pager .lbl{display:block; font-size:11px; color:var(--muted); letter-spacing:.1em; text-transform:uppercase; margin-bottom:2px}

footer.site{margin-top:34px; padding-top:16px; border-top:1px dashed rgba(120,100,60,.3); color:var(--muted); font-size:14px}
footer.site .sign{font-family:"Caveat",cursive; font-size:23px; color:var(--ink)}
.back{display:inline-block; margin-bottom:14px; font-size:15px}

.search{margin:0 0 16px}
.search input{
  width:100%; font:inherit; font-size:16px; color:inherit; padding:7px 12px;
  background:#fffdf6; border:1px dashed #bfae92; border-radius:4px; outline:none;
}
.search input:focus{border-style:solid; border-color:var(--accent); box-shadow:0 0 0 3px rgba(255,233,140,.55)}
.search .hint{display:block; margin-top:4px; font-size:12px; color:var(--muted)}
.hasil{list-style:none; margin:0 0 8px; padding:0}
.hasil li a{display:block; padding:9px 0; border-bottom:1px dashed rgba(120,100,60,.25)}
.hasil b{font-family:"Caveat",cursive; font-size:24px; font-weight:700; display:block}
.hasil span{font-size:13px; color:var(--muted)}
.hasil li.kosong{padding:9px 0; color:var(--muted); font-size:15px}
.list.nyaring .post-card{display:none}

@media (max-width:640px){
  body{font-size:17px; line-height:30px}
  .wrap{margin:0; padding:34px 22px 30px; border-radius:0; background-image:none}
  .wrap::before,.wrap::after{display:none}
  header.site h1{font-size:clamp(40px,12vw,56px)}
  article h2{font-size:28px}
  .post-card{padding-left:30px}
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
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&family=Nunito:wght@400;600;700&display=swap" rel="stylesheet">
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
            "excerpt": plain(re.sub(r"^\s*>.*$", "", re.sub(r"^#.*$", "", body, count=1, flags=re.M), flags=re.M)),
        })

    posts.sort(key=lambda p: (p["date"], p["session"]), reverse=True)

    DIST.mkdir(parents=True, exist_ok=True)
    (DIST / "posts").mkdir(exist_ok=True)
    (DIST / "style.css").write_text(CSS, encoding="utf-8")

    # ---- index
    cards = []
    for p in posts:
        cards.append(
            f'<div class="post-card">'
            f'<div class="post-meta">{meta_baris(p, "")}</div>'
            f'<h2><a href="posts/{p["slug"]}.html">{html.escape(p["title"])}</a></h2>'
            f'<p>{html.escape(p["excerpt"])}</p></div>'
        )

    about = """<aside class="note">
<h2>Panggil gue Raka</h2>
<p>Bukan nama sebenarnya, tapi cerita gue adalah keseharian yang mungkin lo alami juga. Siangnya kerja, malamnya kuliah. Udah kebayang kan sisa-sisa energi gue kayak apa? Capek, nggak bisa mikir. Baca segepok modul kuliah kayak masuk telinga kanan, keluar telinga kiri.</p>
<p>Tapi gue nggak mau nyerah, soalnya gue yakin ilmu Psikologi Islam yang gue dapet bakal berguna buat masa depan gue. Jadi sekarang gue belajar pagi, saat otak gue masih fresh.</p>
<p>Ini catatan belajar gue. Materi dari kampus yang gue tulis ulang dalam bentuk cerita, supaya gue bisa lihat gimana teori abstrak di modul bisa diterapin ke kehidupan sehari-hari.</p>
<p>Kalau lo juga mahasiswa yang struggling kayak gue, atau orang yang tertarik belajar Psikologi Islam, gue harap catatan gue sedikit banyak ngebantu lo. Baca dari mana aja bebas. Komen di blog, nanti gue bales.</p>

<h2>Orang-orang yang bakal sering muncul</h2>
<ul class="cast">
<li><strong>Mba Ratna</strong> &middot; kakak gue</li>
<li><strong>Nadia, Bima, Aya</strong> &middot; tiga keponakan gue, umur 7, 4, dan belum 2</li>
<li><strong>Sinta</strong> &middot; rekan kerja, mejanya sebelah gue</li>
<li><strong>Pak Yanto</strong> &middot; bos gue</li>
<li><strong>Bu Alina</strong> &middot; dosen kelas ini</li>
</ul>

<h2>Yang lagi gue pelajari</h2>
<ul class="cast">
<li><strong>Psikologi Anak</strong> &middot; dua kali seminggu, Senin dan Kamis</li>
<li><strong>Psikologi Perkembangan Masa Hidup, Psikologi Islam, Perspektif dalam Psikologi, Studi Islam 1, Studi Bahasa Inggris</strong> &middot; nyusul kalau yang pertama udah jalan</li>
</ul>

<h2>Soal nama</h2>
<p>Semua nama di sini samaran, termasuk nama gue. Nama kampus dan nama dosen juga nggak gue tulis. Isi materinya tetap sesuai modul, cuma cara nyampeinnya yang gue bikin kayak ngobrol.</p>
</aside>"""

    jumlah = f"{len(posts)} catatan" if posts else "belum ada"
    body = f"""<header class="site">
<div class="kicker">catatan pagi sebelum berangkat kerja</div>
<h1>{html.escape(SITE_TITLE)}</h1>
<p>{html.escape(SITE_TAGLINE)}</p>
</header>
{about}
<main class="list">
<div class="list-head">Catatan<span>{jumlah}</span></div>
<div class="search">
<input id="q" type="search" placeholder="Cari catatan... misal: regresi, ego, hafalan" autocomplete="off" aria-label="Cari catatan">
<span class="hint">Ketik satu kata. Nyaring judul dan isi, langsung di browser, tanpa server.</span>
</div>
<ul class="hasil" id="hasil" hidden></ul>
{''.join(cards) if cards else '<p style="color:#6f6659">Belum ada artikel.</p>'}
</main>
<footer class="site"><span class="sign">Raka</span><br>Ditulis tiap pagi sebelum berangkat kerja.</footer>
<script>
(function(){{
  var q=document.getElementById('q'), hasil=document.getElementById('hasil'), daftar=document.querySelector('.list'), idx=null;
  function tampil(items){{
    if(!items.length){{ hasil.innerHTML='<li class="kosong">Nggak ketemu. Coba kata lain.</li>'; }}
    else {{
      hasil.innerHTML=items.map(function(p){{
        return '<li><a href="'+p.u+'"><b>'+p.t+'</b><span>'+p.c+' · '+p.d+'</span></a></li>';
      }}).join('');
    }}
    hasil.hidden=false; daftar.classList.add('nyaring');
  }}
  q.addEventListener('input', function(){{
    var t=q.value.trim().toLowerCase();
    if(!t){{ hasil.hidden=true; hasil.innerHTML=''; daftar.classList.remove('nyaring'); return; }}
    if(idx){{ tampil(idx.filter(function(p){{ return p.x.indexOf(t)>-1; }}).slice(0,12)); return; }}
    fetch('search.json').then(function(r){{ return r.json(); }}).then(function(d){{
      idx=d; tampil(idx.filter(function(p){{ return p.x.indexOf(t)>-1; }}).slice(0,12));
    }}).catch(function(){{ hasil.innerHTML='<li class="kosong">Indeks pencarian belum siap.</li>'; hasil.hidden=false; }});
  }});
}})();
</script>"""

    (DIST / "index.html").write_text(page(SITE_TITLE, SITE_DESC, body), encoding="utf-8")

    # ---- indeks pencarian (statis; disaring di browser, tanpa server)
    def teks_mentah(md: str) -> str:
        t = re.sub(r"^#+\s*", "", md, flags=re.M)
        t = re.sub(r"[*_`>#]", " ", t)
        return re.sub(r"\s+", " ", t).strip()

    indeks = [
        {
            "t": q["title"],
            "u": f'posts/{q["slug"]}.html',
            "c": q["course"] or "Catatan",
            "d": fmt_date(q["date"]),
            "x": (q["title"] + " " + q["course"] + " " + teks_mentah(q["body"])).lower(),
        }
        for q in posts
    ]
    (DIST / "search.json").write_text(json.dumps(indeks, ensure_ascii=False), encoding="utf-8")

    # ---- halaman kategori per mata kuliah
    kategori: dict[str, dict] = {}
    for q in posts:
        if not q["course"]:
            continue
        s = slugify(q["course"])
        kategori.setdefault(s, {"nama": q["course"], "posts": []})["posts"].append(q)

    (DIST / "kuliah").mkdir(exist_ok=True)
    for s, k in kategori.items():
        kartu = "".join(
            f'<div class="post-card">'
            f'<div class="post-meta">{meta_baris(q, "../")}</div>'
            f'<h2><a href="../posts/{q["slug"]}.html">{html.escape(q["title"])}</a></h2>'
            f'<p>{html.escape(q["excerpt"])}</p></div>'
            for q in k["posts"]
        )
        isi = f"""<a class="back" href="../index.html">&larr; Semua catatan</a>
<header class="site">
<div class="kicker">mata kuliah</div>
<h1>{html.escape(k["nama"])}</h1>
<p>{len(k["posts"])} catatan dari mata kuliah ini.</p>
</header>
<main class="list">{kartu}</main>
<footer class="site"><span class="sign">Raka</span></footer>"""
        (DIST / "kuliah" / f"{s}.html").write_text(
            page(f'{k["nama"]}: catatan', f'Catatan {k["nama"]}', isi, root="../"), encoding="utf-8"
        )

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

        topic = f'<p class="lede">{html.escape(p["topic"])}</p>' if p["topic"] else ""

        content = f"""<a class="back" href="../index.html">&larr; Semua tulisan</a>
<article>
<div class="post-meta">{meta_baris(p, "../")}</div>
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

    # ---- kartu Instagram (1080x1080) + caption yang bisa dicopy
    ig_dir = DIST / "ig"
    ig_dir.mkdir(exist_ok=True)
    shorts_dir = ROOT.parent / "study-blog" / "shorts"
    ig_count = 0
    if shorts_dir.exists():
        for f in sorted(shorts_dir.glob("*.md")):
            raw = f.read_text(encoding="utf-8")
            if "## Instagram" not in raw:
                continue
            block = raw.split("## Instagram", 1)[1]
            m = re.search(r"Teks gambar:\s*(.+)", block)
            image_text = m.group(1).strip() if m else ""
            caption = re.sub(r"Teks gambar:.*", "", block).strip()
            caption = re.sub(r"\n{2,}", "\n\n", caption).strip()
            stem = f.stem.replace("-shorts", "")
            sesi = re.search(r"sesi-(\d+)", stem)
            label = f"Sesi {int(sesi.group(1))}" if sesi else ""

            card = f"""<!doctype html><html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kartu Instagram · {html.escape(label)}</title>
<style>
body{{margin:0;background:#efe9df;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;color:#1d1a16}}
.wrap{{max-width:760px;margin:0 auto;padding:28px 20px 60px}}
.hint{{font-size:14px;color:#6f665c;margin:0 0 14px}}
.card{{width:100%;aspect-ratio:1/1;background:#fbf8f3;border:1px solid #e7e0d5;border-radius:6px;
display:flex;flex-direction:column;justify-content:space-between;padding:9%;
box-shadow:0 8px 30px rgba(29,26,22,.10)}}
.kicker{{font-size:2.2vmin;letter-spacing:.22em;text-transform:uppercase;color:#a8462a;font-weight:700}}
.headline{{font-family:Georgia,"Times New Roman",serif;font-size:7.6vmin;line-height:1.16;letter-spacing:-.02em}}
.foot{{display:flex;justify-content:space-between;align-items:baseline;font-size:2.1vmin;color:#6f665c}}
.foot b{{color:#1d1a16}}
.cap{{margin-top:26px;background:#fff;border:1px solid #e7e0d5;border-radius:10px;padding:18px}}
.cap h2{{font-size:15px;margin:0 0 10px;letter-spacing:.06em;text-transform:uppercase;color:#6f665c}}
textarea{{width:100%;min-height:260px;border:1px solid #e7e0d5;border-radius:8px;padding:12px;
font-family:inherit;font-size:14px;line-height:1.6;background:#fbf8f3;color:#1d1a16;resize:vertical}}
button{{margin-top:12px;padding:10px 18px;border-radius:8px;border:0;background:#a8462a;color:#fff;
font-size:14px;font-weight:600;cursor:pointer}}
button:hover{{background:#8f3a22}}
</style></head><body><div class="wrap">
<p class="hint">Screenshot bagian kartu di atas untuk diunggah ke Instagram. Caption di bawah tinggal dicopy.</p>
<div class="card">
<div class="kicker">Kopi Pagi · {html.escape(label)}</div>
<div class="headline">{html.escape(image_text)}</div>
<div class="foot"><span><b>Kopi Pagi</b> · ngopi dulu, baru kuliah</span><span>{html.escape(label)}</span></div>
</div>
<div class="cap"><h2>Caption</h2>
<textarea id="c">{html.escape(caption)}</textarea>
<button onclick="navigator.clipboard.writeText(document.getElementById('c').value);this.textContent='Tercopy'">Copy caption</button>
</div></div></body></html>"""
            (ig_dir / f"{stem}.html").write_text(card, encoding="utf-8")
            ig_count += 1

    print(f"OK: {len(posts)} artikel -> {DIST}")
    print(f"    index.html, posts/*.html, standalone.html (satu file, bisa dikirim langsung)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
