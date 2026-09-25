"""Render decks to PDF and flag text that wrapped where it must stay on one line."""
import subprocess, sys, glob, os
import pymupdf

# LibreOffice command; override with SOFFICE="python3 /path/to/soffice.py" where bare soffice hangs.
SOFFICE = os.environ.get("SOFFICE", "soffice").split()
decks = sys.argv[1:]

# (name, y_top_in, y_bottom_in, x_min_in, x_max_in, max_lines)
PATTERN = [("title", 0.80, 1.40, 0, 10, 1), ("formula", 1.61, 2.58, 0, 10, 1),
           ("desc", 2.74, 3.70, 0, 10, 2), ("jp", 4.36, 4.75, 0, 10, 1), ("romaji", 4.75, 5.05, 0, 10, 1)]
COVER = [("title", 1.85, 2.85, 0, 10, 1), ("titleJp", 2.85, 3.45, 0, 10, 1), ("hook", 3.6, 4.4, 0, 10, 1)]
CLOSE = [("cta", 3.6, 4.4, 0, 10, 1)]
SUMMARY = [(f"card{r}{c}", 1.76 + r * 0.79, 1.76 + r * 0.79 + 0.67, x0, x0 + 4.08, 1)
           for r in range(4) for c, x0 in enumerate([0.67 + 0.6, 5.25 + 0.6])]

def lines(page):
    out = []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            txt = "".join(s["text"] for s in l["spans"]).strip()
            if txt:
                x0, y0, x1, y1 = l["bbox"]
                out.append((x0 / 72, (y0 + y1) / 2 / 72, txt))
    return out

def check(page, regions):
    probs = []
    ls = lines(page)
    for name, t, b, xa, xb, mx in regions:
        ys = sorted({round(y, 1) for x, y, _ in ls if t <= y < b and xa <= x < xb})
        if len(ys) > mx:
            probs.append(f"{name}: {len(ys)} lines")
    return probs

for d in map(os.path.abspath, decks):
    base = os.path.splitext(d)[0]
    if os.path.exists(base + ".pdf"):
        os.remove(base + ".pdf")
    subprocess.run(["timeout", "180", *SOFFICE, "--headless", "--convert-to", "pdf",
                    "--outdir", os.path.dirname(d), d], capture_output=True, cwd=os.path.dirname(d))
    doc = pymupdf.open(base + ".pdf")
    n = len(doc)
    issues = []
    for i, p in enumerate(doc):
        regions = COVER if i == 0 else CLOSE if i == n - 1 else SUMMARY if i == n - 2 else PATTERN
        for pr in check(p, regions):
            issues.append(f"slide {i+1} {pr}")
    print(os.path.basename(d), n, "slides", "OK" if not issues else issues)
    doc.close()
    os.remove(base + ".pdf")
