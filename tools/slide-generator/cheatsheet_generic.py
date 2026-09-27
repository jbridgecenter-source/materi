"""Generic multi-page cheatsheet generator: Pola Kalimat + Kosakata, always
showing Japanese script + romaji + Indonesian meaning together.
Usage: python3 cheatsheet_generic.py <bab_number> [out.pdf]
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether,
                                 NextPageTemplate, PageTemplate, Paragraph,
                                 Spacer, Table, TableStyle)

ROOT = Path(__file__).resolve().parent.parent.parent
HERE = Path(__file__).resolve().parent

pdfmetrics.registerFont(TTFont("JP", "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"))
pdfmetrics.registerFont(TTFont("Helv", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("Helv-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))

NAVY = colors.HexColor("#072142")
GOLD = colors.HexColor("#EDAE2F")
GOLDTEXT = colors.HexColor("#F5C55A")
INK = colors.HexColor("#1A2433")
BODY = colors.HexColor("#2A3340")
CREAM = colors.HexColor("#FCFAF2")
LIGHT = colors.HexColor("#F3F7FB")
GREEN = colors.HexColor("#1F8A5B")
ROMAJI = colors.HexColor("#6B7480")
ORANGE = colors.HexColor("#B87A1A")
MUTED = colors.HexColor("#C9D6E8")
RULE = colors.HexColor("#DDE2E8")

JP_RE = re.compile(r"[　-ヿ㐀-鿿＀-￯]+")


def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def wrap_jp(s):
    """Escape text and wrap contiguous Japanese runs in a JP-font span."""
    s = esc(s)
    return JP_RE.sub(lambda m: f'<font face="JP">{m.group(0)}</font>', s)


def formula_plain(s):
    s = re.sub(r"\s+", " ", s.strip())
    toks = s.split(" ")
    out = []
    for t in toks:
        m = re.match(r"^[a-z]:(.+)$", t)
        if m:
            out.append(m.group(1).replace("_", " "))
        else:
            out.append(t)
    return " ".join(out)


def load_chapter(bab):
    data = json.loads(subprocess.run(
        ["node", str(HERE / "export_data.js")], cwd=str(HERE),
        capture_output=True, check=True).stdout)
    for c in data:
        if c["bab"] == bab:
            return c
    raise SystemExit(f"bab {bab} not found")


def kotoba_path(book, bab):
    folder = "Modul Minna 1" if "I" == book.strip()[-1] and "II" not in book else "Modul Minna 2"
    d = ROOT / folder / f"Bab {bab}"
    matches = sorted(d.glob("*Kotoba*.md"))
    return matches[0] if matches else None


def clean_sdr(text):
    text = re.sub(r"Sdr\.\s*~,\s*", "", text)
    text = re.sub(r",\s*Sdr\.\s*~", "", text)
    text = re.sub(r"/\s*Sdr\.\s*~", "", text)
    text = re.sub(r"Sdr\.\s*~\s*", "", text)
    return text


def extract_kosakata(md_path, section="A"):
    if md_path is None or not md_path.exists():
        return []
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    start, end = None, len(lines)
    sec_re = re.compile(r"^\*\*([A-Z])\.\s")
    for i, ln in enumerate(lines):
        m = sec_re.match(ln)
        if m and start is None and m.group(1) == section:
            start = i
        elif m and start is not None:
            end = i
            break
    if start is None:
        return []
    rows = []
    for ln in lines[start:end]:
        if not re.match(r"^\|\s*\d+\s*\|", ln):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        kana = cells[1].split("<br>")[0].strip()
        romaji, arti = cells[2].strip(), clean_sdr(cells[3].strip())
        if kana and romaji and arti:
            rows.append((kana, romaji, arti))
    return rows


# ---------- styles ----------
P = ParagraphStyle("body", fontName="Helv", fontSize=9, leading=12.5, textColor=BODY)
P_desc = ParagraphStyle("desc", parent=P, fontSize=8.7, leading=12.2)
P_title = ParagraphStyle("ptitle", fontName="Helv-Bold", fontSize=12.5, leading=15, textColor=INK)
P_tag = ParagraphStyle("ptag", fontName="Helv-Bold", fontSize=8.7, leading=11, textColor=ORANGE)
P_formula = ParagraphStyle("formula", fontName="Helv-Bold", fontSize=13, leading=17, textColor=INK, alignment=1)
P_jp = ParagraphStyle("jpline", fontName="Helv-Bold", fontSize=11.5, leading=15, textColor=INK)
P_romaji = ParagraphStyle("romaji", fontName="Helv", fontSize=8.3, leading=11, textColor=ROMAJI)
P_arti = ParagraphStyle("arti", fontName="Helv-Bold", fontSize=9.3, leading=12, textColor=GREEN)
P_sec = ParagraphStyle("sec", fontName="Helv-Bold", fontSize=10.5, leading=13, textColor=colors.white,
                        backColor=NAVY, borderPadding=(4, 8, 4, 8))
P_h1 = ParagraphStyle("h1", fontName="Helv-Bold", fontSize=22, leading=26, textColor=colors.white)
P_h1jp = ParagraphStyle("h1jp", fontName="Helv-Bold", fontSize=13, leading=17, textColor=GOLDTEXT)
P_hook = ParagraphStyle("hook", fontName="Helv", fontSize=9.5, leading=13, textColor=MUTED)
P_pill = ParagraphStyle("pill", fontName="Helv-Bold", fontSize=8.5, leading=10, textColor=NAVY,
                         backColor=GOLD, borderPadding=(3, 8, 3, 8))
P_voc_k = ParagraphStyle("vk", fontName="Helv-Bold", fontSize=10, leading=13, textColor=INK)
P_voc_r = ParagraphStyle("vr", fontName="Helv", fontSize=8, leading=11, textColor=ROMAJI)
P_voc_a = ParagraphStyle("va", fontName="Helv", fontSize=8.5, leading=11.5, textColor=BODY)
P_voc_head = ParagraphStyle("vhead", fontName="Helv-Bold", fontSize=9, leading=12, textColor=colors.white)
P_foot = ParagraphStyle("foot", fontName="Helv", fontSize=7.5, textColor=ROMAJI)


CARD_W = 523
INNER_W = CARD_W - 20


def pattern_card(i, p):
    formula = wrap_jp(formula_plain(p["formula"]))
    rows = [
        [Paragraph(f'{esc(p["title"])} <font color="#B87A1A" size="8.7">{esc(p["tag"])}</font>', P_title)],
        [Table([[Paragraph(formula, P_formula)]], colWidths=[INNER_W],
               style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.white),
                                  ("BOX", (0, 0), (-1, -1), 0.6, RULE),
                                  ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))],
        [Paragraph(wrap_jp(p["desc"]), P_desc)],
        [Table([[Paragraph(wrap_jp(p["jp"]), P_jp)],
                [Paragraph(f'{esc(p["romaji"])}  <font color="#1F8A5B">→</font> '
                           f'<font face="Helv-Bold" color="#1F8A5B" size="9.3">{wrap_jp(p["arti"])}</font>', P_romaji)]],
               colWidths=[INNER_W],
               style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), CREAM),
                                  ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                                  ("LEFTPADDING", (0, 0), (-1, -1), 10)]))],
    ]
    t = Table(rows, colWidths=[CARD_W])
    t.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.7, RULE),
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ]))
    return KeepTogether([Paragraph(f"POLA {i}", P_pill), Spacer(1, 4), t, Spacer(1, 10)])


def build(bab, out_path=None):
    ch = load_chapter(bab)
    kp = kotoba_path(ch["book"], bab)
    vocab = extract_kosakata(kp)
    out_path = out_path or str(ROOT / ("Modul Minna 1" if ch["book"].strip().endswith("I") and "II" not in ch["book"] else "Modul Minna 2")
                                / f"Bab {bab}" / f"{ch['file']}. Minna {'1' if 'II' not in ch['book'] else '2'} Cheatsheet Bab {bab}.pdf")

    story = []
    header = Table([[Paragraph(f"CHEATSHEET · BAB {bab}", P_pill)],
                     [Spacer(1, 6)],
                     [Paragraph(esc(ch["title"]), P_h1)],
                     [Paragraph(wrap_jp(ch["titleJp"]), P_h1jp)],
                     [Spacer(1, 4)],
                     [Paragraph(wrap_jp(ch["hook"]), P_hook)]],
                    colWidths=[523])
    header.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 14), ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (0, 0), 14), ("BOTTOMPADDING", (-1, -1), (-1, -1), 16),
    ]))
    story.append(header)
    story.append(Spacer(1, 14))
    story.append(Paragraph("POLA KALIMAT", P_sec))
    story.append(Spacer(1, 8))
    for i, p in enumerate(ch["patterns"], 1):
        story.append(pattern_card(i, p))

    if vocab:
        story.append(Spacer(1, 6))
        story.append(Paragraph(f"KOSAKATA ({len(vocab)} kata)", P_sec))
        story.append(Spacer(1, 8))
        rows = [[Paragraph("Kana", P_voc_head), Paragraph("Romaji", P_voc_head), Paragraph("Arti", P_voc_head)]]
        for kana, romaji, arti in vocab:
            rows.append([Paragraph(wrap_jp(kana), P_voc_k), Paragraph(esc(romaji), P_voc_r), Paragraph(wrap_jp(arti), P_voc_a)])
        tbl = Table(rows, colWidths=[120, 110, 293], repeatRows=1)
        style = [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("LINEBELOW", (0, 0), (-1, 0), 1, NAVY),
            ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("LINEBELOW", (0, 1), (-1, -2), 0.4, RULE),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]
        for r in range(1, len(rows), 2):
            style.append(("BACKGROUND", (0, r), (-1, r), LIGHT))
        tbl.setStyle(TableStyle(style))
        story.append(tbl)

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helv", 7.5)
        canvas.setFillColor(ROMAJI)
        canvas.drawString(36, 20, f"JBridge Center  ·  {ch['book']}  ·  Bab {bab}: {ch['title']}")
        canvas.drawRightString(A4[0] - 36, 20, f"Halaman {doc.page}")
        canvas.restoreState()

    doc = BaseDocTemplate(out_path, pagesize=A4, topMargin=28, bottomMargin=34, leftMargin=36, rightMargin=36)
    frame = Frame(36, 34, A4[0] - 72, A4[1] - 62, id="main")
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=footer)])
    doc.build(story)
    return out_path


if __name__ == "__main__":
    bab = int(sys.argv[1])
    out = sys.argv[2] if len(sys.argv) > 2 else None
    p = build(bab, out)
    print("wrote", p)
