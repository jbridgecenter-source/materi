// Dumps all chapter data (Minna 1 Bab 1-25, Minna 2 Bab 26-50) as JSON on stdout,
// normalizing each pattern's `formula` to a plain string (dsl-token form) and each
// chapter to a common shape, for reuse by the Python cheatsheet/infografis generators.
const bab1 = require("./bab1");
const bab2 = require("./build-minna1-bab2");
const minna1 = require("./minna1");
const minna2 = require("./minna2");

function normChapter(ch, book) {
  return {
    book: ch.book || book,
    bab: ch.bab,
    file: ch.file,
    title: ch.title,
    titleJp: ch.titleJp,
    hook: ch.hook,
    cta: ch.cta,
    patterns: ch.patterns.map((p) => {
      if (Array.isArray(p)) {
        const [title, tag, formula, desc, jp, romaji, arti] = p;
        return { title, tag, formula, desc, jp, romaji, arti };
      }
      const formula = typeof p.formula === "string" ? p.formula : p.formula.map((r) => r.text).join(" ");
      return { title: p.title, tag: p.tag, formula, desc: p.desc, jp: p.jp, romaji: p.romaji, arti: p.arti };
    }),
  };
}

const chapters = [
  normChapter(bab1, "Minna no Nihongo I"),
  normChapter(bab2, "Minna no Nihongo I"),
  ...minna1.map((c) => normChapter(c, "Minna no Nihongo I")),
  ...minna2.map((c) => normChapter(c, "Minna no Nihongo II")),
];
chapters.sort((a, b) => a.bab - b.bab);
process.stdout.write(JSON.stringify(chapters));
