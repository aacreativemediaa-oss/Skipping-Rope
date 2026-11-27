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
- Footage iPhone HDR (HLG/Dolby Vision, `color_transfer` bermula `arib-std-b67`) mesti ditukar ke SDR bt709 (zscale + tonemap). Semak warna klip yang disediakan berbanding sumber sebelum render — kalau pucat/kelabu, penukaran tak berlaku.

## Warna footage — JANGAN KACAU colour grading asal
- Tiada colour grading, LUT, filter, atau ubah kontras / saturation / kecerahan / suhu warna pada footage. Tiada `media-treatment`, `eq`, `curves` atau penapis warna CSS.
- Footage SDR (bt709): hanya scale / crop / fps — warna dibiarkan seperti asal.
- Footage HDR iPhone: hanya penukaran teknikal HDR → SDR (langkah di atas) supaya rupa sama seperti asal, bukan untuk ubah gaya. Bandingkan frame klip yang disediakan dengan sumber; kalau warna lari, betulkan penukaran, jangan grade.
- Jangan gelapkan seluruh frame (contoh: lapisan hitam separa lut sinar penuh skrin pada CTA). Untuk bacaan teks, guna panel / pelekat / stroke pada teks itu sendiri, atau bayang setempat yang kecil di belakang teks sahaja.

## Teks & caption
Font Anton untuk tajuk/caption, Montserrat untuk label.

| Tulisan | Saiz (sekarang) | Sebelum |
|---|---|---|
| Headline | **85px** | 100px |
| Sub-headline / pelekat save | **47px** | 70px |
| Caption | **40px** | 60px |
| Nombor heart rate | **64px** | 96px |
| Chip, nama warna, label zon | **19px** | 28px |

### Proporsi infografik (ikut contoh `Proportion.mp4`, Drive)
| Elemen | Ukuran |
|---|---|
| Chip / pill (STEPS, MASA, KALORI, nama otot…) | pill tinggi **60px**, radius 30px, tulisan Montserrat ExtraBold **30px**, isi warna penuh (lime #C8FF1E / kuning #FFD60A / pink #FF3C8E), ikon ✓ bulat hitam 28px, jarak 16px. Ini menggantikan chip 19px dalam jadual di atas. |
| Kotak jadual / panel infografik (panel hitam) | lebar **900px** (di tengah, x 90 → 990), tinggi ~760px (y 310 → 1070), radius **34px**, garis hitam **6px** |
| Setiap baris jadual | tinggi **104px** |
| Label berat (50KG…100KG) | **Anton 50px** |
| Nombor kalori | Anton 47px |
| Bar | tebal 24px |
| Header lajur jadual (BERAT, KALORI…) | Montserrat ExtraBold 24px |
| Nota kaki (*Anggaran…) | 19px |

- Susunan pill: semua pill dalam **satu baris** dahulu (di tengah). Baris kedua hanya bila tak muat dalam lebar yang ada.

- Caption huruf besar, stroke hitam. Perkataan aktif kuning, kata kunci hijau neon, 2–3 perkataan setiap kali, tengah bawah.
- Kedudukan caption: bahagian atas kotak caption pada **y = 1300px** (dahulu 1140px). Pastikan panel / grafik lain tak turun melepasi ~y 1280 supaya tak bertindih.
- Tak bertindih: kalau grafik dah tunjuk ayat yang sama, caption untuk klausa penuh itu disembunyikan.

## Sound effect
- Disintesis sendiri (`hyperframes/scripts/sfx.py`): whoosh, pop, ding, impact, cha-ching, riser, zap.
- Volume perlahan, di bawah voiceover.

## Semakan sebelum hantar
- Snapshot setiap babak.
- VO masih selari dengan asal.
- Frame akhir setiap blok grafik, terutama CTA.
- Pastikan nombor/teks pada grafik sepadan dengan apa yang nampak dalam footage.
