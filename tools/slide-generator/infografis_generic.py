"""Generic infographic generator (HTML + Playwright screenshot): N pola kalimat
timeline + kosakata grid, all showing Japanese script + romaji + Indonesian meaning.
Usage: python3 infografis_generic.py <bab_number> [out.png]
"""
import html
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cheatsheet_generic import (ROOT, extract_kosakata, formula_plain,
                                 kotoba_path, load_chapter)

HERE = Path(__file__).resolve().parent
JP_RE = re.compile(r"[　-ヿ㐀-鿿＀-￯]+")


def e(s):
    return html.escape(s or "", quote=False)


def jp_html(s):
    """Escape and wrap Japanese runs in a <span class="jp"> for the CJK font."""
    return JP_RE.sub(lambda m: f'<span class="jp">{m.group(0)}</span>', e(s))


CSS = """
@font-face { font-family: 'JP'; src: local('IPAGothic'); }
:root{
  --navy:#072142; --navy2:#0d2e57; --gold:#EDAE2F; --goldtext:#F5C55A;
  --ink:#1A2433; --body:#2A3340; --cream:#FCFAF2; --light:#F3F7FB;
  --green:#1F8A5B; --romaji:#8A929C; --line:#DCE3EA; --orange:#B87A1A;
}
*{box-sizing:border-box; margin:0; padding:0;}
body{ width:1080px; font-family: Arial, sans-serif; color:var(--ink); background:#fff; }
.jp{ font-family:"IPAGothic", Arial, sans-serif; }
.header{ background: linear-gradient(135deg, var(--navy) 0%, var(--navy2) 100%);
  padding:44px 56px 40px 56px; position:relative; overflow:hidden; }
.header::after{ content:""; position:absolute; right:-60px; top:-60px; width:280px; height:280px;
  border-radius:50%; background: rgba(237,174,47,0.08); }
.header::before{ content:""; position:absolute; right:80px; bottom:-90px; width:180px; height:180px;
  border-radius:50%; background: rgba(255,255,255,0.05); }
.pill{ display:inline-block; background:var(--gold); color:var(--navy); font-weight:700;
  font-size:13px; padding:7px 16px; border-radius:14px; letter-spacing:.5px; }
.logo-box{ position:absolute; right:56px; top:40px; background:#fff; width:64px; height:64px;
  border-radius:12px; display:flex; align-items:center; justify-content:center;
  box-shadow:0 4px 14px rgba(0,0,0,.25); }
.logo-box img{ width:48px; height:48px; }
.header h1{ color:#fff; font-size:38px; margin-top:18px; font-weight:800; position:relative; z-index:1;}
.header .jpline{ color:var(--goldtext); font-size:20px; margin-top:6px; font-weight:700; position:relative; z-index:1;}
.header p{ color:#C9D6E8; font-size:15px; margin-top:12px; max-width:640px; position:relative; z-index:1;}
.sec{ padding:0 56px; }
.sec-title{ display:flex; align-items:center; gap:10px; margin:40px 0 22px 0; }
.sec-num{ width:30px; height:30px; border-radius:50%; background:var(--navy); color:#fff;
  font-weight:800; font-size:14px; display:flex; align-items:center; justify-content:center; }
.sec-title h2{ font-size:21px; color:var(--navy); font-weight:800; }
.timeline{ position:relative; padding-left:44px; }
.timeline::before{ content:""; position:absolute; left:19px; top:8px; bottom:8px; width:3px;
  background: repeating-linear-gradient(to bottom, var(--gold) 0 8px, transparent 8px 14px); }
.step{ position:relative; margin-bottom:22px; }
.step-dot{ position:absolute; left:-44px; top:2px; width:40px; height:40px; border-radius:50%;
  background:var(--gold); color:var(--navy); font-weight:800; font-size:16px;
  display:flex; align-items:center; justify-content:center; border:4px solid #fff;
  box-shadow:0 0 0 2px var(--gold); }
.step-card{ background:var(--light); border-radius:12px; padding:16px 20px; border:1px solid var(--line); }
.step-head{ display:flex; align-items:baseline; gap:10px; flex-wrap:wrap; margin-bottom:8px;}
.step-head .formula{ font-size:16px; font-weight:800; color:var(--ink); }
.step-head .tag{ font-size:12.5px; font-weight:700; color:var(--orange); font-style:italic; }
.step-desc{ font-size:13px; color:var(--body); line-height:1.5; margin-bottom:10px; }
.step-ex{ background:#fff; border-radius:8px; padding:10px 14px; border-left:4px solid var(--gold); }
.step-ex .jpx{ font-size:15px; font-weight:700; color:var(--ink); }
.step-ex .rmj{ font-size:11.5px; color:var(--romaji); font-style:italic; margin-top:2px; }
.step-ex .art{ font-size:12.5px; color:var(--green); font-weight:700; }
.vocab-grid{ display:grid; grid-template-columns: repeat(2, 1fr); gap:10px; }
.vocab-card{ background:var(--light); border:1px solid var(--line); border-radius:8px;
  padding:10px 14px; display:flex; align-items:baseline; gap:10px; }
.vocab-card .k{ font-size:14px; font-weight:700; color:var(--ink); min-width:110px; }
.vocab-card .r{ font-size:10.5px; color:var(--romaji); font-style:italic; min-width:90px; }
.vocab-card .a{ font-size:11.5px; color:var(--body); flex:1; }
.footer{ margin-top:46px; padding:20px 56px; background:var(--navy); color:#9AA3AE; font-size:11.5px;
  display:flex; justify-content:space-between; align-items:center; }
.footer b{ color:#fff; }
"""


def build_html(ch, vocab):
    steps = []
    for i, p in enumerate(ch["patterns"], 1):
        steps.append(f"""
      <div class="step">
        <div class="step-dot">{i}</div>
        <div class="step-card">
          <div class="step-head"><span class="formula">{jp_html(formula_plain(p['formula']))}</span><span class="tag">{e(p['tag'])}</span></div>
          <div class="step-desc">{jp_html(p['desc'])}</div>
          <div class="step-ex">
            <div class="jpx">{jp_html(p['jp'])}</div>
            <div class="rmj">{e(p['romaji'])}</div>
            <div class="art">&rarr; {jp_html(p['arti'])}</div>
          </div>
        </div>
      </div>""")

    vocab_cards = "\n".join(
        f'<div class="vocab-card"><span class="k jp">{e(k)}</span>'
        f'<span class="r">{e(r)}</span><span class="a">{jp_html(a)}</span></div>'
        for k, r, a in vocab
    )

    return f"""<!DOCTYPE html>
<html lang="id"><head><meta charset="utf-8"><style>{CSS}</style></head><body>
  <div class="header">
    <span class="pill">INFOGRAFIS &middot; {e(ch['book'].upper())} &middot; BAB {ch['bab']}</span>
    <div class="logo-box"><img src="LOGO_SRC"></div>
    <h1>{e(ch['title'])}</h1>
    <div class="jpline jp">{e(ch['titleJp'])}</div>
    <p>{jp_html(ch['hook'])}</p>
  </div>
  <div class="sec">
    <div class="sec-title"><div class="sec-num">1</div><h2>{len(ch['patterns'])} Pola Kalimat</h2></div>
    <div class="timeline">{''.join(steps)}</div>
  </div>
  <div class="sec">
    <div class="sec-title"><div class="sec-num">2</div><h2>Kosakata Bab {ch['bab']} ({len(vocab)} kata)</h2></div>
    <div class="vocab-grid">{vocab_cards}</div>
  </div>
  <div class="footer">
    <div><b>JBridge Center</b> &middot; {e(ch['book'])} &middot; Bab {ch['bab']}: {e(ch['title'])}</div>
    <div>Infografis untuk latihan mandiri</div>
  </div>
</body></html>"""


def build(bab, out_path=None):
    ch = load_chapter(bab)
    kp = kotoba_path(ch["book"], bab)
    vocab = extract_kosakata(kp)
    book_folder = "Modul Minna 1" if ("II" not in ch["book"]) else "Modul Minna 2"
    book_num = "1" if book_folder.endswith("1") else "2"
    out_path = out_path or str(ROOT / book_folder / f"Bab {bab}" / f"{ch['file']}. Minna {book_num} Infografis Bab {bab}.png")

    tmp_html = HERE / f"_infografis_bab{bab}.html"
    tmp_html.write_text(build_html(ch, vocab), encoding="utf-8")
    subprocess.run(["node", str(HERE / "render_infografis.js"), str(tmp_html), out_path], check=True, cwd=str(HERE))
    tmp_html.unlink()
    return out_path


if __name__ == "__main__":
    bab = int(sys.argv[1])
    out = sys.argv[2] if len(sys.argv) > 2 else None
    p = build(bab, out)
    print("wrote", p)
