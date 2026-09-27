const path = require("path");
const { build, C, F } = require("./gen");

const tunjuk = (t) => F.t(t, C.tunjuk);
const desu = (t) => F.t(t, C.purple);
const part = (t) => F.t(t, C.red);

const cfg = {
  bab: 2,
  file: "27",
  title: "Kata Tunjuk Benda",
  titleJp: "これ・それ・あれ",
  hook: "\"Ini\", \"itu\", dan \"itu\" — kok beda-beda? Rahasianya ada di jarak.",
  cta: "Coba tunjuk benda di sekitarmu pakai kore, sore, are!",
  patterns: [
    {
      title: "Kore / Sore / Are", tag: "ini · itu · itu (jauh)",
      formula: [tunjuk("これ"), F.sep(" / "), tunjuk("それ"), F.sep(" / "), tunjuk("あれ")],
      desc: "Tiga penunjuk benda:  これ  = ini (dekat aku),  それ  = itu (dekat kamu),  あれ  = itu (jauh dari kita). Ketiganya bisa berdiri sendiri seperti kata benda.",
      jp: "それはじしょですか。", romaji: "sore wa jisho desu ka", arti: "Apakah itu kamus?",
    },
    {
      title: "Kono / Sono / Ano + KB", tag: "ditempel ke benda",
      formula: [tunjuk("この"), F.plusL(), ...F.kb(), F.plus(), desu("です")],
      desc: "この / その / あの  WAJIB ditempel di depan kata benda.  この  = ini,  その  = itu (dekatmu),  あの  = itu (jauh). Jadi  この ほん  = buku ini.",
      jp: "このほんはわたしのです。", romaji: "kono hon wa watashi no desu", arti: "Buku ini punya saya.",
    },
    {
      title: "Sou desu / Chigaimasu", tag: "jawaban ya / bukan",
      formula: [desu("そうです"), F.sep(" / "), F.t("ちがいます", C.verb)],
      desc: "Untuk menjawab \"apakah ini X?\". Kalau benar:  はい、そうです . Kalau salah:  いいえ、ちがいます .",
      jp: "はい、そうです。", romaji: "hai, sou desu", arti: "Ya, betul.",
    },
    {
      title: "~ka, ~ka", tag: "pilih A atau B",
      formula: [...F.kb("1"), F.sep(" "), desu("ですか、"), F.sep(" "), ...F.kb("2"), F.sep(" "), desu("ですか")],
      desc: "Untuk nanya \"A atau B?\". Sebut dua pilihan, masing-masing diakhiri  か . Jawabnya langsung sebut yang benar, tanpa  はい / いいえ .",
      jp: "これは「9」ですか、「7」ですか。", romaji: "kore wa \"9\" desu ka, \"7\" desu ka", arti: "Ini \"9\" atau \"7\"?",
    },
    {
      title: "KB no KB", tag: "jenis / milik",
      formula: [...F.kb("1"), F.plus(), part("の"), F.plusL(), ...F.kb("2")],
      desc: "の  = lem penyambung dua benda. Bisa berarti jenis/topik ( コンピューターの ほん  = buku tentang komputer) atau pemilik ( わたしの  = punya saya).",
      jp: "これはコンピューターのほんです。", romaji: "kore wa konpyuutaa no hon desu", arti: "Ini buku (tentang) komputer.",
    },
    {
      title: "No pengganti KB", tag: "hindari pengulangan",
      formula: [...F.kb("1"), F.plus(), part("の")],
      desc: "Kalau bendanya sudah jelas dari obrolan, kata benda di belakang boleh dihilangkan — cukup  の  saja.",
      jp: "このかばんはあなたのですか。", romaji: "kono kaban wa anata no desu ka", arti: "Tas ini punya Anda?",
    },
    {
      title: "O~ (awalan sopan)", tag: "lebih halus",
      formula: [F.t("お", C.san), F.plusL(), ...F.kb()],
      desc: "お  ditempel di depan beberapa kata benda biar lebih sopan. Contoh:  なまえ → おなまえ ,  さけ → おさけ ,\nみやげ → おみやげ .",
      jp: "おなまえは？", romaji: "onamae wa?", arti: "Siapa nama (Anda)?",
    },
    {
      title: "Sou desu ka", tag: "oh, begitu",
      formula: [desu("そうですか")],
      desc: "Ungkapan saat dapat info baru: \"Oh, begitu\". Nada TURUN di akhir. (Kalau naik, jadi pertanyaan  そうですか ?)",
      jp: "そうですか。", romaji: "sou desu ka", arti: "Oh, begitu.",
    },
  ],
  summary: [
    ["Kore/sore/are", "これ・それ・あれ"],
    ["Kono/sono/ano", "この・その・あの"],
    ["Jawab ya/bukan", "そうです・ちがいます"],
    ["Pilih A atau B", "か、か"],
    ["Jenis / milik", "の"],
    ["Pengganti benda", "の"],
    ["Awalan sopan", "お〜"],
    ["Oh, begitu", "そうですか"],
  ],
};

module.exports = cfg;

if (require.main === module) {
  const out = process.argv[2] ||
    path.join(__dirname, "..", "..", "Modul Minna 1", "Bab 2", "27. Minna 1 Tata Bahasa Bab 2 - Slide.pptx");
  build(cfg, out).then((f) => console.log("wrote", f));
}
