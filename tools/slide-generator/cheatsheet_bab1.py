import os
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

pdfmetrics.registerFont(TTFont("JP", "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"))
pdfmetrics.registerFont(TTFont("Helv-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Helv", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("Helv-Oblique", "/mnt/skills/examples/canvas-design/canvas-fonts/InstrumentSans-Italic.ttf"))

NAVY = (0x07/255, 0x21/255, 0x42/255)
GOLD = (0xED/255, 0xAE/255, 0x2F/255)
INK = (0x1A/255, 0x24/255, 0x33/255)
BODY = (0x2A/255, 0x33/255, 0x40/255)
CREAM = (0xFC/255, 0xFA/255, 0xF2/255)
LIGHT = (0xF3/255, 0xF7/255, 0xFB/255)
WHITE = (1, 1, 1)
GREEN = (0x1F/255, 0x8A/255, 0x5B/255)
ROMAJI = (0x6B/255, 0x74/255, 0x80/255)
ORANGE = (0xB8/255, 0x7A/255, 0x1A/255)
RULE = (0xDD/255, 0xE2/255, 0xE8/255)

W, H = A4
MARGIN = 26
ROOT = Path(__file__).resolve().parent.parent.parent
OUT = os.environ.get("OUT") or str(ROOT / "Modul Minna 1" / "Bab 1" / "26. Minna 1 Cheatsheet Bab 1.pdf")
LOGO = str(ROOT / "logo_jbridgecenter.png")

patterns = [
    ("1", "KB1 wa KB2 desu", "A adalah B", "watashi wa Budi desu", "Saya (adalah) Budi."),
    ("2", "KB1 wa KB2 ja arimasen", "bukan", "Andi-san wa gakusei ja arimasen", "Andi bukan mahasiswa."),
    ("3", "KB1 wa KB2 desu ka", "kalimat tanya", "Budi-san wa Indoneshia-jin desu ka", "Apakah Budi orang Indonesia?"),
    ("4", "KB mo KB desu", "juga", "Andi-san mo kaishain desu", "Andi juga pegawai perusahaan."),
    ("5", "KB1 no KB2", "kepunyaan/asal", "Budi-san wa JBridge Center no shain desu", "Budi pegawai JBridge Center."),
    ("6", "Nama + san", "panggilan sopan", "ano kata wa Budi-san desu", "Beliau (adalah) Budi."),
]

kosakata = [
    ("watashi", "saya"), ("anata", "Anda"), ("ano hito", "orang itu"), ("ano kata", "beliau"),
    ("~san", "Bpk/Ibu ~"), ("~chan", "sapaan akrab anak"), ("~jin", "orang ~ (WN)"),
    ("sensei", "guru/dosen"), ("kyoushi", "guru/dosen"), ("gakusei", "mahasiswa"),
    ("kaishain", "karyawan"), ("shain", "karyawan (+nama PT)"), ("ginkouin", "pegawai bank"),
    ("isha", "dokter"), ("kenkyuusha", "peneliti"), ("daigaku", "universitas"),
    ("byouin", "rumah sakit"), ("dare", "siapa"), ("donata", "siapa (sopan)"),
    ("~sai", "~ tahun"), ("nansai", "umur berapa"), ("oikutsu", "umur berapa (sopan)"),
    ("hai", "ya"), ("iie", "tidak/bukan"),
]

ungkapan = [
    ("hajimemashite", "Perkenalkan."),
    ("~kara kimashita", "datang/berasal dari ~"),
    ("douzo yoroshiku onegaishimasu", "Salam kenal."),
    ("shitsurei desu ga", "permisi, maaf"),
    ("onamae wa?", "Siapa namanya?"),
    ("kochira wa ~san desu", "Ini Bapak/Ibu ~"),
]

negara = [
    ("amerika", "Amerika Serikat"), ("igirisu", "Inggris"), ("indo", "India"),
    ("indoneshia", "Indonesia"), ("kankoku", "Korea Selatan"), ("tai", "Thailand"),
    ("chuugoku", "Cina"), ("doitsu", "Jerman"), ("nihon", "Jepang"), ("burajiru", "Brasil"),
]


def draw_pill(c, x, y, w, h, text, fill, textcolor, size=8, font="Helv-Bold"):
    c.setFillColorRGB(*fill)
    c.roundRect(x, y, w, h, h / 2, stroke=0, fill=1)
    c.setFillColorRGB(*textcolor)
    c.setFont(font, size)
    c.drawCentredString(x + w / 2, y + h / 2 - size * 0.35, text)


def section_title(c, x, y, text, w):
    tw = pdfmetrics.stringWidth(text, "Helv-Bold", 8.5)
    draw_pill(c, x, y - 14, tw + 16, 16, text, NAVY, WHITE, size=8.5)
    return y - 14


def wrap_text(text, font, size, max_w):
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if pdfmetrics.stringWidth(trial, font, size) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


c = canvas.Canvas(OUT, pagesize=A4)

# ---- Header band ----
HEAD_H = 68
c.setFillColorRGB(*NAVY)
c.rect(0, H - HEAD_H, W, HEAD_H, stroke=0, fill=1)
try:
    img = ImageReader(LOGO)
    box_h = 46
    box_w = 46
    box_x = W - MARGIN - box_w
    box_y = H - HEAD_H + (HEAD_H - box_h) / 2
    c.setFillColorRGB(*WHITE)
    c.roundRect(box_x, box_y, box_w, box_h, 5, stroke=0, fill=1)
    pad = 5
    c.drawImage(img, box_x + pad, box_y + pad, box_w - 2 * pad, box_h - 2 * pad, mask="auto")
except Exception as e:
    pass

draw_pill(c, MARGIN, H - 30, 118, 16, "MINNA 1 · BAB 1", GOLD, NAVY, size=8.5)
c.setFillColorRGB(*WHITE)
c.setFont("Helv-Bold", 20)
c.drawString(MARGIN, H - 54, "Cheatsheet: Perkenalan Diri")
c.setFont("JP", 12)
c.setFillColorRGB(*GOLD)
c.drawString(MARGIN, H - 65, "じこしょうかい ・ 自己紹介")

y_top = H - HEAD_H - 16
col_gap = 16
col_w = (W - 2 * MARGIN - col_gap) / 2
xL = MARGIN
xR = MARGIN + col_w + col_gap

# ================= LEFT COLUMN: Pola Kalimat =================
y = y_top
y = section_title(c, xL, y, "POLA KALIMAT", col_w)
y -= 10

row_h = 60
for num, formula, tag, romaji, arti in patterns:
    c.setFillColorRGB(*WHITE)
    c.setStrokeColorRGB(*RULE)
    c.roundRect(xL, y - row_h, col_w, row_h, 5, stroke=1, fill=1)

    c.setFillColorRGB(*GOLD)
    c.circle(xL + 12, y - 12, 8, stroke=0, fill=1)
    c.setFillColorRGB(*NAVY)
    c.setFont("Helv-Bold", 9)
    c.drawCentredString(xL + 12, y - 15, num)

    c.setFillColorRGB(*INK)
    c.setFont("Helv-Bold", 10)
    c.drawString(xL + 26, y - 15, formula)
    c.setFillColorRGB(*ORANGE)
    c.setFont("Helv-Oblique", 8)
    c.drawRightString(xL + col_w - 8, y - 15, tag)

    c.setStrokeColorRGB(*RULE)
    c.line(xL + 8, y - 24, xL + col_w - 8, y - 24)

    c.setFillColorRGB(*ROMAJI)
    c.setFont("Helv-Oblique", 7.6)
    for i, ln in enumerate(wrap_text(romaji, "Helv-Oblique", 7.6, col_w - 16)):
        c.drawString(xL + 8, y - 34 - i * 9, ln)
    ry = y - 34 - len(wrap_text(romaji, "Helv-Oblique", 7.6, col_w - 16)) * 9
    c.setFillColorRGB(*GREEN)
    c.setFont("Helv-Bold", 7.8)
    for i, ln in enumerate(wrap_text("→ " + arti, "Helv-Bold", 7.8, col_w - 16)):
        c.drawString(xL + 8, ry - 2 - i * 9, ln)

    y -= row_h + 8

# Legend box
c.setFillColorRGB(*LIGHT)
c.roundRect(xL, y - 40, col_w, 40, 5, stroke=0, fill=1)
c.setFillColorRGB(*NAVY)
c.setFont("Helv-Bold", 8)
c.drawString(xL + 8, y - 14, "Ingat:")
c.setFillColorRGB(*BODY)
c.setFont("Helv", 7.6)
c.setFillColorRGB(*BODY)
c.setFont("Helv", 7.6)
c.drawString(xL + 8, y - 25, "Partikel")
ix = xL + 8 + pdfmetrics.stringWidth("Partikel ", "Helv", 7.6)
c.setFont("JP", 8.2)
c.drawString(ix, y - 25, "は")
ix2 = ix + pdfmetrics.stringWidth("は", "JP", 8.2)
c.setFont("Helv", 7.6)
c.drawString(ix2 + 3, y - 25, "ditulis \"ha\" tapi dibaca \"wa\" sebagai penanda topik.")
note_rest2 = "Bentuk formal negatif: dewa arimasen. Jangan pakai ~san untuk nama sendiri."
for i, ln in enumerate(wrap_text(note_rest2, "Helv", 7.6, col_w - 16)):
    c.drawString(xL + 8, y - 34 - i * 9, ln)

# ================= RIGHT COLUMN =================
y = y_top
y = section_title(c, xR, y, "KOSAKATA INTI", col_w)
y -= 10

sub_gap = 10
sub_w = (col_w - sub_gap) / 2
row_h2 = 12.5
n_left = (len(kosakata) + 1) // 2
c.setFont("JP", 7.8)
for idx, (romaji, arti) in enumerate(kosakata):
    col = 0 if idx < n_left else 1
    row = idx if idx < n_left else idx - n_left
    x0 = xR + col * (sub_w + sub_gap)
    yy = y - row * row_h2
    c.setFillColorRGB(*INK)
    c.setFont("Helv-Bold", 7.6)
    c.drawString(x0, yy - 8, romaji)
    c.setFillColorRGB(*BODY)
    c.setFont("Helv", 7.2)
    c.drawRightString(x0 + sub_w, yy - 8, arti)
    c.setStrokeColorRGB(*RULE)
    c.setDash(1, 2)
    c.line(x0, yy - 10, x0 + sub_w, yy - 10)
    c.setDash()

y = y - n_left * row_h2 - 14

y = section_title(c, xR, y, "UNGKAPAN", col_w)
y -= 10
for romaji, arti in ungkapan:
    c.setFillColorRGB(*CREAM)
    lines_r = wrap_text(romaji, "Helv-Bold", 7.6, col_w - 12)
    lines_a = wrap_text(arti, "Helv", 7.4, col_w - 12)
    box_h = 7 + len(lines_r) * 9 + len(lines_a) * 8.5
    c.roundRect(xR, y - box_h, col_w, box_h, 4, stroke=0, fill=1)
    c.setFillColorRGB(*NAVY)
    c.setFont("Helv-Bold", 7.6)
    yy = y - 9
    for ln in lines_r:
        c.drawString(xR + 6, yy, ln)
        yy -= 9
    c.setFillColorRGB(*GREEN)
    c.setFont("Helv", 7.4)
    for ln in lines_a:
        c.drawString(xR + 6, yy, ln)
        yy -= 8.5
    y -= box_h + 5

y -= 4
y = section_title(c, xR, y, "NAMA NEGARA", col_w)
y -= 10
neg_cols = 2
neg_w = (col_w - sub_gap) / neg_cols
n_left2 = (len(negara) + 1) // 2
c.setFont("Helv", 7.4)
for idx, (romaji, arti) in enumerate(negara):
    col = 0 if idx < n_left2 else 1
    row = idx if idx < n_left2 else idx - n_left2
    x0 = xR + col * (neg_w + sub_gap)
    yy = y - row * 11
    c.setFillColorRGB(*INK)
    c.setFont("Helv-Bold", 7.4)
    c.drawString(x0, yy - 8, romaji)
    c.setFillColorRGB(*BODY)
    c.setFont("Helv", 7.2)
    c.drawString(x0 + 52, yy - 8, arti)

# ---- Footer ----
c.setFillColorRGB(*ROMAJI)
c.setFont("Helv", 7)
c.drawString(MARGIN, 16, "JBridge Center  ·  Minna no Nihongo I  ·  Bab 1: Perkenalan Diri")
c.drawRightString(W - MARGIN, 16, "Cheatsheet untuk latihan mandiri")

c.showPage()
c.save()
print("wrote", OUT)
