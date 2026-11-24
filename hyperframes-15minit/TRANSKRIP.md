# 15 Minit Skipping — Transkrip & Senarai Edit

Video: 1080×1920, 60fps, 39.0 saat, 62.3MB, dibina dengan HyperFrames 0.9.80.
Format: `CLAUDE.md` (saiz teks dikemas kini — headline 100px, sub 47px, caption 40px, chip/label 19px).

## 1. Transkrip audio asal

Folder Drive ada 47 fail (46 lama + `copy_9492…MOV` yang baru). Semua telah ditranskrip
(Whisper `small`, Bahasa Melayu): **tiada voiceover atau percakapan** — hanya bunyi latar.
Video diedit tanpa VO; skrip dipaparkan sebagai grafik + caption.

## 2. Skrip atas skrin

| Masa | Babak | Teks | Dipaparkan sebagai |
|---|---|---|---|
| 0.0–4.0 | Hook | 15 MINIT SKIPPING / SETIAP HARI? | Headline 100px + sub 47px (caption disembunyikan) |
| 1.5–3.85 | Hook | INI YANG JADI · PADA **BADAN** KAU | Caption |
| 4.0–14.0 | Kalori (10s) | KALORI / TERBAKAR DALAM 15 MINIT + carta 50–100 kg | Grafik |
| 10.6–13.85 | Kalori | LEBIH **BERAT**, · LEBIH BANYAK **KALORI** | Caption |
| 14.0–20.0 | Otot (6s) | OTOT / YANG DILATIH — Bahu, Punggung, Lengan, Paha, Perut/Core, Betis, + Jantung & Paru-paru | Grafik (chip 19px) |
| 17.6–19.8 | Otot | SEMUA KERJA · **SERENTAK!** | Caption |
| 20.0–23.5 | USP | TALI SKIPPING NI ADA / DIGITAL COUNTER / KIRA LOMPATAN, KALORI & JARAK | Grafik sahaja (caption disembunyikan supaya skrin counter tak tertutup) |
| 23.5–29.5 | USP | DUAL MODE / MODE 1: BOLA PEMBERAT + chip "SESUAI UNTUK PEMULA" / MODE 2: TALI PANJANG | Grafik |
| 24.8–26.3 | USP | TAK **TERSANGKUT** KAKI | Caption (mod bola) |
| 27.6–29.3 | USP | NAK LEBIH **CABARAN?** | Caption (mod tali) |
| 29.5–33.5 | USP | BOLEH SKIPPING / DALAM RUMAH JE | Grafik (di bawah muka) |
| 31.0–33.3 | USP | TAK PERLU **GYM**, · **JIMAT** MASA | Caption |
| 33.5–39.0 | CTA | NAK BADAN FIT 2027? / START SKIPPING / SEKARANG! | Grafik (caption disembunyikan) |

Nota counter: skrin dalam klip ini berada dalam mod **Km/Miles** (0001), jadi teks grafik
menyebut "lompatan, kalori & jarak" — fungsi yang memang nampak pada counter dalam footage
(kiraan, Cals, Km/Miles). Tiada nombor dipaparkan supaya tidak bercanggah dengan skrin.

### Data kalori (15 minit, kadar sederhana)
kcal = MET × 3.5 × berat(kg) ÷ 200 × 15 minit, MET 11.8 (lompat tali kadar sederhana).

| Berat | Kalori |
|---|---|
| 50 kg | ~155 kcal |
| 60 kg | ~186 kcal |
| 70 kg | ~217 kcal |
| 80 kg | ~248 kcal |
| 90 kg | ~279 kcal |
| 100 kg | ~310 kcal |

## 3. Senarai klip (10 klip — semua berbeza dari video 10 minit)

| # | Masa | Sumber | Potongan sumber | LUFS asal | Gain → −57 LUFS |
|---|---|---|---|---|---|
| 1 | 0.0–4.0 (intro, satu shot, laju asal) | copy_9492…MOV (baru) | 0.5–4.5s | −36.7 | −20.3 dB |
| 2 | 4.0–9.0 | IMG_1987.MOV (HLG → SDR) | 3.5–8.5s | −41.5 | −15.5 dB |
| 3 | 9.0–14.0 | video_20260419_202843.mp4 | 2.0–7.0s | −32.8 | −24.2 dB |
| 4 | 14.0–17.0 | IMG_1093.MOV (HLG → SDR) | 2.0–5.0s | −55.3 | −1.7 dB |
| 5 | 17.0–20.0 | IMG_1161.MOV (HLG → SDR) | 3.0–6.0s | −40.9 | −16.1 dB |
| 6 | 20.0–23.5 | lv_0_20251026143250.mp4 (counter) | 26.2–29.7s | −49.9 | −7.1 dB |
| 7 | 23.5–26.5 | IMG_1207.MOV (mod bola pemberat, HLG → SDR) | 2.5–5.5s | −47.5 | −9.5 dB |
| 8 | 26.5–29.5 | IMG_1100.MOV (mod tali panjang, HLG → SDR) | 1.5–4.5s | −35.7 | −21.3 dB |
| 9 | 29.5–33.5 | IMG_1073.MOV (dalam rumah, HLG → SDR) | 0.5–4.5s | −32.5 | −24.5 dB |
| 10 | 33.5–39.0 | video_20260419_202951.mp4 | 5.0–10.5s | −33.3 | −23.7 dB |

Semua dipotong dengan penapis `trim`/`atrim` (frame-tepat) dan disemak: tiada potongan
dalaman atau frame beku. Tiada klip perlukan lebih daripada +12 dB.
Setiap klip: zoom masuk 1.00→1.08 (0.7s) + kilatan putih 0.24s pada potongan.

## 4. Sound effect
whoosh, pop, ding, impact, cha-ching, riser, zap — disintesis sendiri (`hyperframes/scripts/sfx.py`).
Paling kuat −31 LUFS momentary. Tiada muzik.
