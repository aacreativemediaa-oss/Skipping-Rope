# 10 Minit Skipping — Transkrip & Senarai Edit

Video: 1080×1920, 60fps, 37.0 saat, dibina dengan HyperFrames 0.9.80.

## 1. Transkrip audio asal

Kesemua 46 fail dalam folder Drive telah ditranskrip (Whisper `small`, Bahasa Melayu).
**Tiada voiceover atau percakapan ditemui** — semua fail hanya ada bunyi latar
(bunyi tali, tapak kaki, angin, unboxing). Ayat "Terima kasih kerana menonton" yang keluar
pada beberapa fail ialah halusinasi Whisper atas bunyi senyap, bukan percakapan sebenar.

Atas persetujuan, video diedit **tanpa VO**: skrip di bawah dipaparkan sebagai teks
(grafik + caption).

## 2. Skrip atas skrin

| Masa | Babak | Teks | Dipaparkan sebagai |
|---|---|---|---|
| 0.0–4.0 | Hook | 10 MINIT SKIPPING / SETIAP HARI? | Headline 150px + sub 70px (caption disembunyikan) |
| 1.5–3.85 | Hook | INI YANG JADI · PADA **BADAN** KAU | Caption |
| 4.0–14.0 | Kalori (10s) | KALORI / TERBAKAR DALAM 10 MINIT + carta 50–90 kg | Grafik (caption disembunyikan) |
| 10.6–13.85 | Kalori | LEBIH **BERAT**, · LEBIH BANYAK **KALORI** | Caption |
| 14.0–22.0 | Otot | OTOT / YANG DILATIH — Bahu, Punggung, Lengan, Paha, Perut/Core, Betis, + Jantung & Paru-paru | Grafik |
| 20.0–21.9 | Otot | SEMUA KERJA · **SERENTAK!** | Caption |
| 22.0–25.5 | USP | TALI SKIPPING NI ADA / DIGITAL COUNTER | Grafik |
| 23.6–25.35 | USP | KIRA SETIAP **LOMPATAN** | Caption |
| 25.5–27.1 | USP | 176 KCAL — KALORI TERBAKAR (sama dengan bacaan '176 Cals' pada skrin counter; grafik keluar sebelum skrin bertukar mod) | Grafik |
| 25.6–27.9 | USP | SEMUA DIKIRA **AUTOMATIK** | Caption |
| 28.0–31.5 | USP | BOLEH SKIPPING / DALAM RUMAH JE | Grafik |
| 29.55–31.4 | USP | TAK PERLU **GYM**, · **JIMAT** MASA | Caption |
| 31.5–37.0 | CTA | NAK BADAN FIT 2027? / START SKIPPING / SEKARANG! | Grafik (caption disembunyikan) |

### Data kalori (10 minit, kadar sederhana)
Formula: kcal = MET × 3.5 × berat(kg) ÷ 200 × 10 minit, MET 11.8
(Compendium of Physical Activities, lompat tali kadar sederhana).

| Berat | Kalori |
|---|---|
| 50 kg | ~103 kcal |
| 60 kg | ~124 kcal |
| 70 kg | ~145 kcal |
| 80 kg | ~165 kcal |
| 90 kg | ~186 kcal |

## 3. Senarai klip (9 klip, maksimum 10)

| # | Masa | Sumber | Potongan sumber (anggaran ±0.5s) | LUFS asal | Gain → −57 LUFS |
|---|---|---|---|---|---|
| 1 | 0.0–4.0 (intro, satu shot, laju asal) | video_20260419_202731.mp4 | 0.5–4.5s | −26.7 | −30.3 dB |
| 2 | 4.0–9.0 | video_20260218_150009.mp4 | 3.0–8.0s | −27.1 | −29.9 dB |
| 3 | 9.0–14.0 | IMG_1097.MOV (HLG → SDR) | 2.0–7.0s | −40.8 | −16.2 dB |
| 4 | 14.0–18.0 | IMG_1206.MOV (HLG → SDR) | 2.0–6.0s | −33.7 | −23.3 dB |
| 5 | 18.0–22.0 | IMG_1099.MOV (HLG → SDR) | 1.0–5.0s | −45.9 | −11.1 dB |
| 6 | 22.0–25.5 | copy_C56E…mov (counter mula mengira) | 31.3–34.8s | −60.1 | +3.1 dB |
| 7 | 25.5–28.0 | copy_2AF7…mov (counter 176 Cals) | ~42–44.5s | −63.3 | +6.3 dB |
| 8 | 28.0–31.5 | copy_2AF7…mov (skipping dalam rumah) | 13.0–16.5s | −50.0 | −7.0 dB |
| 9 | 31.5–37.0 | video_20251025_145958_edit.mp4 | 12.0–17.5s | −20.7 | −36.3 dB |

Tiada klip yang perlukan lebih daripada +12 dB, jadi had +12 dB tidak tercapai.
Setiap klip: zoom masuk 1.00→1.08 (0.7s, expo.out) + kilatan putih 0.24s pada potongan.

## 4. Sound effect (disintesis sendiri — `scripts/sfx.py`)

whoosh, pop, ding, impact, cha-ching, riser, zap — semuanya dijana dengan numpy,
dilaraskan ke −36 LUFS momentary (di bawah aras rujukan VO −30 LUFS). Tiada muzik latar.
