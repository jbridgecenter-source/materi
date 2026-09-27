import re, sys

def apply(path, triples, sdr_lines):
    s = open(path, encoding="utf-8").read()
    for old, new in triples:
        assert old in s, f"NOT FOUND in {path}: {old[:60]}"
        s = s.replace(old, new)
    for old in sdr_lines:
        assert old in s, f"SDR NOT FOUND in {path}: {old[:60]}"
        new = old.replace("Sdr. ", "")
        s = s.replace(old, new)
    open(path, "w", encoding="utf-8").write(s)

minna1_triples = [
    ('"きょうとへいきます。", "Kyouto e ikimasu", "Pergi ke Kyoto."',
     '"バンドンへいきます。", "Bandon e ikimasu", "Pergi ke Bandung."'),
    ('"このでんしゃはこうしえんへいきますよ。", "kono densha wa Koushien e ikimasu yo", "Kereta ini ke Koushien, lho."',
     '"このでんしゃはボゴールへいきますよ。", "kono densha wa Bogooru e ikimasu yo", "Kereta ini ke Bogor, lho."'),
    ('"いっしょにきょうとへいきませんか。", "issho ni Kyouto e ikimasen ka", "Mau pergi ke Kyoto bareng?"',
     '"いっしょにバンドンへいきませんか。", "issho ni Bandon e ikimasen ka", "Mau pergi ke Bandung bareng?"'),
    ('"きょうとですか。いいですね。", "Kyouto desu ka. ii desu ne", "Oh, ke Kyoto ya? Asyik."',
     '"バンドンですか。いいですね。", "Bandon desu ka. ii desu ne", "Oh, ke Bandung ya? Asyik."'),
    ('"ふじさんはたかいです。", "Fujisan wa takai desu", "Gunung Fuji tinggi."',
     '"ブロモさんはたかいです。", "Buromo-san wa takai desu", "Gunung Bromo tinggi."'),
    ('"ペキンはとてもさむいです。", "Pekin wa totemo samui desu", "Beijing sangat dingin."',
     '"ディエンはとてもさむいです。", "Dien wa totemo samui desu", "Dieng sangat dingin."'),
    ('"ならはどんなまちですか。", "Nara wa donna machi desu ka", "Nara kota yang seperti apa?"',
     '"ジョグジャカルタはどんなまちですか。", "Jogjakarta wa donna machi desu ka", "Yogyakarta kota yang seperti apa?"'),
    ('"こうべへえいがをみにいきます。", "Koube e eiga o mi ni ikimasu", "Pergi ke Kobe untuk nonton film."',
     '"マランへえいがをみにいきます。", "Maran e eiga o mi ni ikimasu", "Pergi ke Malang untuk nonton film."'),
    ('"わたしはおおさかにすんでいます。", "watashi wa Oosaka ni sunde imasu", "Saya tinggal di Osaka."',
     '"わたしはスラバヤにすんでいます。", "watashi wa Surabaya ni sunde imasu", "Saya tinggal di Surabaya."'),
    ('"おおさかはたべものがおいしいです。", "Oosaka wa tabemono ga oishii desu", "Osaka makanannya enak."',
     '"スラバヤはたべものがおいしいです。", "Surabaya wa tabemono ga oishii desu", "Surabaya makanannya enak."'),
    ('"なかなかふじさんをみることができません。", "nakanaka Fujisan o miru koto ga dekimasen", "Sulit sekali bisa melihat Gunung Fuji."',
     '"なかなかブロモさんをみることができません。", "nakanaka Buromo-san o miru koto ga dekimasen", "Sulit sekali bisa melihat Gunung Bromo."'),
    ('"ぜひほっかいどうへいきたいです。", "zehi Hokkaidou e ikitai desu", "Saya benar-benar ingin ke Hokkaido."',
     '"ぜひロンボクへいきたいです。", "zehi Ronbok e ikitai desu", "Saya benar-benar ingin ke Lombok."'),
    ('"ほっかいどうへいったことがあります。", "Hokkaidou e itta koto ga arimasu", "Pernah pergi ke Hokkaido."',
     '"ロンボクへいったことがあります。", "Ronbok e itta koto ga arimasu", "Pernah pergi ke Lombok."'),
    ('"あしたとうきょうへいく。", "ashita Toukyou e iku", "Besok pergi ke Tokyo. (santai)"',
     '"あしたジャカルタへいく。", "ashita Jakaruta e iku", "Besok pergi ke Jakarta. (santai)"'),
    ('"とうきょうでサッカーのしあいがあります。", "Toukyou de sakkaa no shiai ga arimasu", "Di Tokyo ada pertandingan sepak bola."',
     '"ジャカルタでサッカーのしあいがあります。", "Jakaruta de sakkaa no shiai ga arimasu", "Di Jakarta ada pertandingan sepak bola."'),
    ('"パリへいくとき、かばんをかいました。", "Pari e iku toki, kaban o kaimashita", "Waktu mau ke Paris, saya beli tas."',
     '"メダンへいくとき、かばんをかいました。", "Medan e iku toki, kaban o kaimashita", "Waktu mau ke Medan, saya beli tas."'),
]

minna1_sdr = [
    '"アンディさんはじむしょです。", "Andi-san wa jimusho desu", "Sdr. Andi ada di kantor."',
    '"アンディさんはいまでんわをかけています。", "Andi-san wa ima denwa o kakete imasu", "Sdr. Andi sedang menelepon."',
    '"ブディさんのかさはどれですか。", "Budi-san no kasa wa dore desu ka", "Payung Sdr. Budi yang mana?"',
    '"ブディさんはあしたやすむといいました。", "Budi-san wa ashita yasumu to iimashita", "Sdr. Budi bilang besok libur."',
    '"これはブディさんがつくったケーキです。", "kore wa Budi-san ga tsukutta keeki desu", "Ini kue yang dibuat Sdr. Budi."',
    '"アンディさんはわたしをえきまでおくってくれました。", "Andi-san wa watashi o eki made okutte kuremashita", "Sdr. Andi mengantar saya ke stasiun."',
]

minna2_triples = [
    ('"しんかんせんからふじさんがみえます。", "shinkansen kara Fuji-san ga miemasu", "Dari Shinkansen terlihat Gunung Fuji."',
     '"しんかんせんからブロモさんがみえます。", "shinkansen kara Buromo-san ga miemasu", "Dari kereta cepat terlihat Gunung Bromo."'),
    ('"おおさかでてんらんかいがひらかれました。", "Oosaka de tenrankai ga hirakaremashita", "Di Osaka diadakan pameran."',
     '"スラバヤでてんらんかいがひらかれました。", "Surabaya de tenrankai ga hirakaremashita", "Di Surabaya diadakan pameran."'),
    ('"うまれたのはチェンマイです。", "umareta no wa Chenmai desu", "Yang (tempat) lahir saya adalah Chiang Mai."',
     '"うまれたのはソロです。", "umareta no wa Solo desu", "Yang (tempat) lahir saya adalah Solo."'),
]

minna2_sdr = [
    '"アンディさんはにほんごがはなせます。", "Andi-san wa nihongo ga hanasemasu", "Sdr. Andi bisa berbahasa Jepang."',
    '"ブディさんがけっこんするのをしって いますか。", "Budi-san ga kekkon suru no o shitte imasu ka", "Apakah Anda tahu bahwa Sdr. Budi akan menikah?"',
    '"アンディさんはがっこうでどうでしょうか。", "Andi-san wa gakkou de dou deshou ka", "Bagaimana keadaan Sdr. Andi di sekolah, ya?"',
    '"ブディさんはきょうくるはずです。", "Budi-san wa kyou kuru hazu desu", "Sdr. Budi seharusnya datang hari ini."',
    '"アンディさんがねつをだしまして、けさは げんきが なかったんです。", "Andi-san ga netsu o dashimashite, kesa wa genki ga nakattan desu", "Sdr. Andi demam, sehingga pagi ini kurang sehat."',
]

apply("minna1.js", minna1_triples, minna1_sdr)
apply("minna2.js", minna2_triples, minna2_sdr)
print("all replacements applied")
