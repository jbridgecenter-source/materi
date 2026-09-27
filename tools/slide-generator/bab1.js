// Minna no Nihongo I, Bab 1. Hand-authored before the generator existed;
// formalized here so it can feed the cheatsheet/infografis pipeline too.
module.exports = {
  book: "Minna no Nihongo I",
  bab: 1,
  file: "26",
  title: "Perkenalan Diri",
  titleJp: "じこしょうかい・自己紹介",
  hook: "は dibaca \"ha\" tapi jadi \"wa\"? Kenalan sama 6 pola kalimat dasar dan kosakata perkenalan diri dalam bahasa Jepang.",
  cta: "Coba perkenalkan dirimu sendiri dalam bahasa Jepang!",
  patterns: [
    {
      title: "KB1 wa KB2 desu", tag: "A adalah B",
      formula: "KB1 + は + KB2 + です",
      desc: "Pola paling dasar. Partikel は ditulis \"ha\" tapi dibaca \"wa\" saat jadi penanda topik. です membuat kalimat sopan.",
      jp: "わたしはブディです。", romaji: "watashi wa Budi desu", arti: "Saya (adalah) Budi.",
    },
    {
      title: "KB1 wa KB2 ja arimasen", tag: "bukan",
      formula: "KB1 + は + KB2 + じゃ ありません",
      desc: "Tukar です jadi じゃ ありません untuk bilang \"bukan\". Versi formal/tulisan: では ありません.",
      jp: "アンディさんはがくせいじゃ ありません。", romaji: "Andi-san wa gakusei ja arimasen", arti: "Andi bukan mahasiswa.",
    },
    {
      title: "KB1 wa KB2 desu ka", tag: "kalimat tanya",
      formula: "KB1 + は + KB2 + です + か",
      desc: "Tempelkan か di ujung kalimat, naikkan nada di akhir. Jawab はい (ya) atau いいえ (tidak).",
      jp: "ブディさんはインドネシアじんですか。", romaji: "Budi-san wa Indoneshia-jin desu ka", arti: "Apakah Budi orang Indonesia?",
    },
    {
      title: "KB mo KB desu", tag: "juga",
      formula: "KB + も + KB + です",
      desc: "も artinya \"juga\", dipakai kalau keterangan orang kedua sama dengan orang pertama. は diganti も.",
      jp: "アンディさんもかいしゃいんです。", romaji: "Andi-san mo kaishain desu", arti: "Andi juga pegawai perusahaan.",
    },
    {
      title: "KB1 no KB2", tag: "kepunyaan / asal",
      formula: "KB1 + の + KB2",
      desc: "の itu \"lem\" penyambung dua kata benda. KB1 menerangkan KB2 — bisa berarti milik, asal, atau bagian.",
      jp: "ブディさんはJBridge Centerのしゃいんです。", romaji: "Budi-san wa JBridge Center no shain desu", arti: "Budi pegawai (dari) JBridge Center.",
    },
    {
      title: "Nama Orang + san", tag: "panggilan sopan",
      formula: "Nama Orang + さん",
      desc: "さん itu panggilan sopan di belakang nama orang (mirip Bapak/Ibu/Kak). JANGAN dipakai untuk diri sendiri.",
      jp: "あの かたはブディさんです。", romaji: "ano kata wa Budi-san desu", arti: "Beliau (adalah) Budi.",
    },
  ],
  summary: [
    ["A adalah B", "です"], ["Bukan", "じゃ ありません"], ["Kalimat tanya", "か"],
    ["Juga", "も"], ["Kepunyaan/asal", "の"], ["Panggilan sopan", "さん"],
  ],
};
