# Slide Generator

Membuat slide PowerPoint tata bahasa (gaya JBridge Center) dari data per bab.

## Cara pakai

```bash
cd tools/slide-generator
npm install
npm run minna1            # build Minna 1 Bab 3–25
node build-minna1.js 5 7  # build bab tertentu saja
npm run minna1-bab2       # build Minna 1 Bab 2
```

Hasilnya langsung ditulis ke `Modul Minna 1/Bab N/NN. Minna 1 Tata Bahasa Bab N - Slide.pptx`.

Cek hasil (butuh LibreOffice): judul, rumus, contoh, dan kartu rangkuman harus tetap satu baris.

```bash
python3 check.py "../../Modul Minna 1/Bab 3/28. Minna 1 Tata Bahasa Bab 3 - Slide.pptx"
```

## File

| File | Isi |
| --- | --- |
| `gen.js` | Desain slide: cover, slide pola, rangkuman, penutup, warna, logo |
| `dsl.js` | Penulis rumus berwarna (lihat di bawah) |
| `minna1.js` | Data Minna 1 Bab 3–25 |
| `build-minna1.js` | Build data `minna1.js` |
| `build-minna1-bab2.js` | Data + build Minna 1 Bab 2 |
| `check.py` | Cek otomatis teks yang terpotong |

Bab 1 dibuat manual sebelum generator ini ada, jadi datanya tidak ada di sini.

## Menambah bab / modul baru

Salin satu entri di `minna1.js`. Setiap pola ditulis sebagai:

```js
[judul, tag, rumus, penjelasan, contohJepang, romaji, arti]
```

Rumus ditulis dengan token dipisah spasi (`_` = spasi di dalam token):

| Token | Arti | Warna |
| --- | --- | --- |
| `KB` `KB1` `KB2` | kata benda (angka jadi subscript) | biru |
| `KK` / `KS` | kata kerja / kata sifat | hijau / merah muda |
| `p:は` | partikel | merah |
| `d:です` | です・ます | ungu |
| `v:いきます` | kata kerja | hijau |
| `a:おおきい` | kata sifat | merah muda |
| `t:これ` | kata tunjuk / tanya | teal |
| `o:お` | awalan, keterangan | oranye |
| `n:tempat` | kata benda / isian | biru |
| `g:、～` | teks abu-abu | abu-abu |
| `+` `/` `→` | penghubung | abu-abu |

Contoh: `"n:tempat + p:へ + v:いきます"` → **tempat+ へ + いきます**.

Penjelasan yang panjang otomatis dipatah di spasi, supaya kata Jepang tidak terpotong di tengah.
