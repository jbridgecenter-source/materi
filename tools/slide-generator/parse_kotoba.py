import re

def extract_kosakata(md_path, section="A"):
    """Parse a 'Kotoba Bab N.md' file and return [(kana, romaji, arti), ...]
    from the given lettered section (default A. Kosakata)."""
    text = open(md_path, encoding="utf-8").read()
    lines = text.splitlines()
    start = None
    end = len(lines)
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
        _, kotoba, romaji, arti = cells[0], cells[1], cells[2], cells[3]
        kana = kotoba.split("<br>")[0].strip()
        romaji = romaji.strip()
        arti = arti.strip()
        if kana and romaji and arti:
            rows.append((kana, romaji, arti))
    return rows


if __name__ == "__main__":
    import sys
    for k, r, a in extract_kosakata(sys.argv[1]):
        print(k, "|", r, "|", a)
