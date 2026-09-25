const path = require("path");
const pptxgen = require("pptxgenjs");

const LOGO = path.join(__dirname, "..", "..", "logo_jbridgecenter.png");
const FONT = "Arial";

const C = {
  navy: "072142", navyCard: "133A6B", pill: "0A2342", gold: "EDAE2F", goldText: "F5C55A",
  light: "F3F7FB", white: "FFFFFF", cream: "FCFAF2", ink: "1A2433", body: "2A3340",
  mutedBlue: "C9D6E8", gray: "94A3B8", footer: "9AA3AE", romaji: "8A929C",
  blue: "2F7FD6", red: "EF4F4F", purple: "8B5CF6", orange: "E8A43A", san: "D4912A",
  green: "1F8A5B", tunjuk: "138A8A", verb: "2E9160", adj: "D6336C",
};

// Formula token helpers
const F = {
  kb: (n) => (n
    ? [{ text: "KB", options: { color: C.blue } }, { text: n, options: { subscript: true, color: C.blue } }]
    : [{ text: "KB", options: { color: C.blue } }]),
  plus: () => ({ text: "+ ", options: { color: C.gray } }),
  plusL: () => ({ text: " +", options: { color: C.gray } }),
  sep: (t) => ({ text: t, options: { color: C.gray } }),
  t: (t, color) => ({ text: t, options: { color } }),
};

function build(cfg, out) {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  const BOOK = cfg.book || "Minna no Nihongo I";
  pres.title = `${BOOK} - Bab ${cfg.bab} - Tata Bahasa`;

  const shadow = () => ({ type: "outer", color: "000000", blur: 6, offset: 2, angle: 90, opacity: 0.18 });

  const logoBox = (s) => {
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: 9.09, y: 0.09, w: 0.81, h: 0.82, rectRadius: 0.08,
      fill: { color: C.white }, line: { color: C.white },
    });
    s.addImage({ path: LOGO, x: 9.225, y: 0.235, w: 0.54, h: 0.526 });
  };
  const logoPlain = (s) => s.addImage({ path: LOGO, x: 9.225, y: 0.225, w: 0.55, h: 0.536 });
  const pill = (s, text, fill, color, y) => s.addText(text, {
    shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.16,
    x: 0.67, y, w: 1.5, h: 0.32, margin: 0,
    fill: { color: fill }, line: { color: fill },
    fontFace: FONT, fontSize: 9, bold: true, color, align: "center", valign: "middle", wrap: false,
    shadow: shadow(), isTextBox: true,
  });

  // Cover
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };
    logoBox(s);
    pill(s, `BAB ${cfg.bab} · TATA BAHASA`, C.gold, C.navy, 0.52);
    let titleSize = 44;
    while (titleSize > 28 && cfg.title.length * 0.62 * titleSize > 8.3 * 72) titleSize -= 1;
    s.addText(cfg.title, {
      x: 0.6, y: 1.9, w: 8.3, h: 0.9, margin: 0,
      fontFace: FONT, fontSize: titleSize, bold: true, color: C.white, isTextBox: true,
    });
    s.addText(cfg.titleJp, {
      x: 0.67, y: 2.85, w: 8.3, h: 0.55, margin: 0,
      fontFace: FONT, fontSize: 26, bold: true, color: C.goldText, isTextBox: true,
    });
    s.addText(cfg.hook, {
      x: 0.67, y: 3.7, w: 8.8, h: 0.4, margin: 0,
      fontFace: FONT, fontSize: 13, color: C.mutedBlue, isTextBox: true,
    });
  }

  // Pattern slides
  cfg.patterns.forEach((p, i) => {
    const s = pres.addSlide();
    s.background = { color: C.light };
    logoPlain(s);
    pill(s, `POLA ${i + 1}`, C.pill, C.white, 0.465);

    s.addText([
      { text: p.title, options: { fontSize: 23, bold: true, color: C.ink } },
      { text: "     ", options: { fontSize: 23 } },
      { text: p.tag, options: { fontSize: 13, bold: true, italic: true, color: C.orange } },
    ], { x: 0.67, y: 0.86, w: 8.5, h: 0.5, margin: 0, fontFace: FONT, valign: "middle", isTextBox: true });

    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: 0.67, y: 1.61, w: 8.65, h: 0.97, rectRadius: 0.08,
      fill: { color: C.white }, line: { color: C.white }, shadow: shadow(),
    });
    s.addText(p.formula, {
      x: 0.67, y: 1.61, w: 8.65, h: 0.97, margin: 0,
      fontFace: FONT, fontSize: 21, bold: true, align: "center", valign: "middle", isTextBox: true,
    });

    s.addText(p.desc, {
      x: 0.7, y: 2.78, w: 8.6, h: 0.62, margin: 0,
      fontFace: FONT, fontSize: 12, color: C.body, valign: "top", lineSpacingMultiple: 1.1, isTextBox: true,
    });

    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: 0.67, y: 4.08, w: 8.65, h: 1.16, rectRadius: 0.08,
      fill: { color: C.cream }, line: { color: C.cream }, shadow: shadow(),
    });
    s.addText("CONTOH", {
      x: 0.94, y: 4.2, w: 2, h: 0.18, margin: 0,
      fontFace: FONT, fontSize: 8, bold: true, color: C.orange, isTextBox: true,
    });
    s.addText(p.jp, {
      x: 0.94, y: 4.38, w: 8.2, h: 0.36, margin: 0,
      fontFace: FONT, fontSize: 17, bold: true, color: C.ink, valign: "middle", isTextBox: true,
    });
    s.addText([
      { text: p.romaji, options: { italic: true, color: C.romaji, fontSize: 9.5 } },
      { text: "   →  ", options: { color: C.green, fontSize: 9.5 } },
      { text: p.arti, options: { bold: true, color: C.green, fontSize: 11 } },
    ], { x: 0.94, y: 4.76, w: 8.2, h: 0.26, margin: 0, fontFace: FONT, valign: "middle", isTextBox: true });

    s.addText(`${BOOK}  ·  Bab ${cfg.bab} · ${cfg.title}`, {
      x: 0.67, y: 5.3, w: 5, h: 0.2, margin: 0,
      fontFace: FONT, fontSize: 8, color: C.footer, isTextBox: true,
    });
  });

  // Summary
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };
    logoBox(s);
    pill(s, "RANGKUMAN", C.gold, C.navy, 0.52);
    s.addText(`Pola Bab ${cfg.bab}`, {
      x: 0.67, y: 0.9, w: 5, h: 0.5, margin: 0,
      fontFace: FONT, fontSize: 23, bold: true, color: C.white, valign: "middle", isTextBox: true,
    });
    const step = 0.79, h = 0.67;
    cfg.summary.forEach(([label, j], i) => {
      const col = i % 2, row = Math.floor(i / 2);
      const x = col === 0 ? 0.67 : 5.25, y = 1.76 + row * step;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x, y, w: 4.08, h, rectRadius: 0.06,
        fill: { color: C.navyCard }, line: { color: C.navyCard }, shadow: shadow(),
      });
      s.addText(String(i + 1), {
        shape: pres.shapes.OVAL, x: x + 0.14, y: y + (h - 0.35) / 2, w: 0.35, h: 0.35, margin: 0,
        fill: { color: C.gold }, line: { color: C.gold },
        fontFace: FONT, fontSize: 11, bold: true, color: C.navy, align: "center", valign: "middle", isTextBox: true,
      });
      s.addText([
        { text: label, options: { color: C.white } },
        { text: "   " + j, options: { color: C.goldText } },
      ], { x: x + 0.63, y, w: 3.35, h, margin: 0, fontFace: FONT, fontSize: 11, bold: true, valign: "middle", isTextBox: true });
    });
  }

  // Closing
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };
    logoBox(s);
    s.addText("またね！", {
      x: 0, y: 1.65, w: 10, h: 1.1, margin: 0,
      fontFace: FONT, fontSize: 64, bold: true, color: C.white, align: "center", valign: "middle", isTextBox: true,
    });
    s.addText("matane — sampai jumpa!", {
      x: 0, y: 3.0, w: 10, h: 0.35, margin: 0,
      fontFace: FONT, fontSize: 15, color: C.mutedBlue, align: "center", valign: "middle", isTextBox: true,
    });
    s.addText(cfg.cta, {
      x: 0.5, y: 3.7, w: 9, h: 0.35, margin: 0,
      fontFace: FONT, fontSize: 14, bold: true, color: C.gold, align: "center", valign: "middle", isTextBox: true,
    });
  }

  return pres.writeFile({ fileName: out });
}

module.exports = { build, C, F };
