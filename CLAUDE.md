# Format video (Hyperframes) — guna untuk task seterusnya

Rujukan projek terdahulu: `hyperframes/project/` (10 Minit Skipping) dan `hyperframes/scripts/`.

## Format asas
- 1080×1920 menegak, 60fps, dibina dengan Hyperframes.
- Tiada muzik latar.
- Voiceover asal tidak diubah (volume 100%, tiada potongan).
- Bunyi asal footage: setiap klip diselaraskan ke −57 LUFS (atau 27 dB di bawah VO kalau tahap VO berbeza).
  Klip kuat diperlahankan; klip perlahan dikuatkan dengan had +12 dB.
- Saiz video sasaran: 70MB.

## Potongan
- Maksimum 10 klip; intro satu shot sahaja (tak tukar laju).
- Setiap klip ada zoom masuk ringkas + kilatan putih pada potongan.
- Babak fitur guna footage sebenar.
- Potong klip dengan penapis `trim`/`atrim` (seek frame-tepat), bukan `-ss` sebelum `-i`: sesetengah fail sumber dah ada potongan dalaman.

## Teks & caption
Font Anton untuk tajuk/caption, Montserrat untuk label.

| Tulisan | Saiz (sekarang) | Sebelum |
|---|---|---|
| Headline | **100px** | 150px |
| Sub-headline / pelekat save | **47px** | 70px |
| Caption | **40px** | 60px |
| Nombor heart rate | **64px** | 96px |
| Chip, nama warna, label zon | **19px** | 28px |

- Caption huruf besar, stroke hitam. Perkataan aktif kuning, kata kunci hijau neon, 2–3 perkataan setiap kali, tengah bawah.
- Tak bertindih: kalau grafik dah tunjuk ayat yang sama, caption untuk klausa penuh itu disembunyikan.

## Sound effect
- Disintesis sendiri (`hyperframes/scripts/sfx.py`): whoosh, pop, ding, impact, cha-ching, riser, zap.
- Volume perlahan, di bawah voiceover.

## Semakan sebelum hantar
- Snapshot setiap babak.
- VO masih selari dengan asal.
- Frame akhir setiap blok grafik, terutama CTA.
- Pastikan nombor/teks pada grafik sepadan dengan apa yang nampak dalam footage.
