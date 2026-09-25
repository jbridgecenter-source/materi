const { C } = require("./gen");

// Formula mini-language: space-separated tokens, "_" = literal space inside a token.
//   KB KB1 KB2 KK KS  placeholders (blue / green / pink, digit -> subscript)
//   p: particle  d: です/ます  v: verb  a: adjective  t: demonstrative/question
//   o: affix/adverb  n: noun/placeholder  g: gray
//   + / → 、 operators
const JP = /[぀-ヿ一-鿿～〜「」]/;
const COL = { p: C.red, d: C.purple, v: C.verb, a: C.adj, t: C.tunjuk, o: C.san, n: C.blue, g: C.gray };
const PH = { KB: C.blue, KK: C.verb, KS: C.adj };

function parse(src) {
  const toks = src.trim().split(/\s+/).map((raw) => {
    const s = raw.replace(/_/g, " ");
    if (["+", "/", "→"].includes(s)) return { op: s, text: s };
    const ph = s.match(/^(KB|KK|KS)(\d)?$/);
    if (ph) return { text: ph[1], sub: ph[2], color: PH[ph[1]] };
    const m = s.match(/^([pdvatong]):(.+)$/);
    if (m) return { text: m[2], color: COL[m[1]] };
    return { text: s, color: C.ink };
  });
  const isJp = (t) => t && !t.op && JP.test(t.text);
  const runs = [];
  toks.forEach((t, i) => {
    const prev = toks[i - 1], next = toks[i + 1];
    if (t.op === "+") {
      const both = !isJp(prev) && !isJp(next);
      runs.push({ text: (isJp(prev) || both ? " " : "") + "+" + (isJp(next) || both ? " " : ""), options: { color: C.gray } });
      return;
    }
    if (t.op) {
      runs.push({ text: ` ${t.op} `, options: { color: C.gray } });
      return;
    }
    const needSpace = prev && !prev.op && !t.text.startsWith("、");
    runs.push({ text: (needSpace ? " " : "") + t.text, options: { color: t.color } });
    if (t.sub) runs.push({ text: t.sub, options: { color: t.color, subscript: true } });
  });
  return runs;
}

module.exports = { parse };
