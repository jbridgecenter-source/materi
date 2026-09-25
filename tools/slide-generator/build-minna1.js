const path = require("path");
const { build } = require("./gen");
const { parse } = require("./dsl");
const chapters = require("./minna1");

// Japanese may wrap between any two kana, so long descriptions get an explicit break at a space.
const JPC = /[　-ヿ一-鿿＀-￯～〜→]/;
const units = (s) => [...s].reduce((n, ch) => n + (JPC.test(ch) ? 2 : 1), 0);
function smartBreak(desc) {
  if (units(desc) <= 96) return desc;
  let best = -1;
  for (let i = 0; i < desc.length; i++) {
    if (desc[i] === " " && units(desc.slice(0, i)) <= 94) best = i;
  }
  if (best < 0) return desc;
  const rest = desc.slice(best + 1);
  if (units(rest) > 100) console.warn("  desc may need 3 lines:", desc.slice(0, 40));
  return desc.slice(0, best) + "\n" + rest;
}

const only = process.argv.slice(2).map(Number);
(async () => {
  for (const ch of chapters) {
    if (only.length && !only.includes(ch.bab)) continue;
    const cfg = {
      ...ch,
      patterns: ch.patterns.map(([title, tag, formula, desc, jp, romaji, arti]) =>
        ({ title, tag, formula: parse(formula), desc: smartBreak(desc), jp, romaji, arti })),
    };
    const out = path.join(__dirname, "..", "..", "Modul Minna 1", `Bab ${ch.bab}`,
      `${ch.file}. Minna 1 Tata Bahasa Bab ${ch.bab} - Slide.pptx`);
    await build(cfg, out);
    console.log("wrote", path.relative(process.cwd(), out));
  }
})();
