import os, math
P='/home/user/hf/kesilapan'
# ---- format (CLAUDE.md, updated) ----
HL, SUB, CAP, CHIP = 85, 47, 40, 19
css=f'''    @font-face {{ font-family: "Anton"; src: url("assets/fonts/Anton-Regular.ttf") format("truetype"); font-weight: 400; }}
    @font-face {{ font-family: "MontserratV"; src: url("assets/fonts/Montserrat.ttf") format("truetype"); font-weight: 100 900; }}
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    .hl {{ font-family: "Anton", sans-serif; font-size: {HL}px; line-height: 1.04; color: #fff; text-transform: uppercase; text-align: center;
          -webkit-text-stroke: 7px #000; paint-order: stroke fill; text-shadow: 0 6px 18px rgba(0,0,0,.55); letter-spacing: 1px; }}
    .sub {{ font-family: "Anton", sans-serif; font-size: {SUB}px; line-height: 1.15; color: #fff; text-transform: uppercase; text-align: center;
           -webkit-text-stroke: 5px #000; paint-order: stroke fill; text-shadow: 0 4px 12px rgba(0,0,0,.5); letter-spacing: 1px; }}
    .y {{ color: #FFE600; }} .g {{ color: #39FF14; }}
    .lbl {{ font-family: "MontserratV", sans-serif; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; }}
    .topshade {{ display:none; }}
    .line {{ position: absolute; left: 0; width: 1080px; }}
    .left {{ left: 130px; width: 520px; text-align: left; }}
'''
def scene(cid, style, body, js):
    return f'''<template>
  <style>
{css}{style}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">
{body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
'''
IN_BLUR='{ opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power4.out" }'
IN_SLAM='{ opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: 0.3, ease: "expo.out" }'
def out(sel, t): return f'    tl.to({sel}, {{ opacity: 0, filter: "blur(8px)", duration: 0.2, ease: "power2.in" }}, {t});'
W={}
CHIPCSS=f'''
    .chiprow {{ position:absolute; left:90px; width:900px; display:flex; flex-wrap:wrap; justify-content:center; gap:16px; }}
    .pill {{ height:60px; padding: 0 22px 0 14px; border-radius:30px; background:#C8FF1E; border:none;
            display:flex; align-items:center; gap:9px; font-size:30px; color:#000; white-space:nowrap; box-shadow: 0 6px 18px rgba(0,0,0,.45); }}
    .pill.yb {{ background:#FFD60A; }} .pill.pk {{ background:#FF3C8E; color:#fff; }}
    .pill i {{ width:28px; height:28px; border-radius:50%; background:#000; display:flex; align-items:center; justify-content:center; flex:none; }}
    .pill i svg {{ width:16px; height:16px; }}'''
CHK='<i><svg viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg></i>'
def chiprows(prefix, rows, y0, step=96, colors=("","yb","pk")):
    out=[]; k=0
    for r,row in enumerate(rows):
        cells=[]
        for name in row:
            k+=1; cells.append(f'<div id="{prefix}-p{k}" class="pill lbl {colors[(k-1)%len(colors)]}">{CHK}{name}</div>')
        out.append(f'    <div class="chiprow" style="top:{y0+r*step}px">'+"".join(cells)+'</div>')
    return "\n".join(out), k
def pop(sel,t): return f'    tl.fromTo("{sel}", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(1.7)" }}, {t});'
# ===== shared comparison styles =====
LIME="#C8FF1E"; PINK="#FF3C8E"; YEL="#FFD60A"
CMPCSS=f'''
    .tag {{ position:absolute; left:0; right:0; margin:0 auto; width:max-content; top:300px; padding:4px 30px 8px 18px; background:{LIME};
           font-family:"Anton",sans-serif; font-size:{SUB}px; line-height:1.15; color:#000; text-transform:uppercase; transform:rotate(-2deg);
           display:flex; align-items:center; gap:14px; box-shadow:0 6px 18px rgba(0,0,0,.4); }}
    .tag b {{ width:46px; height:46px; border:3px solid #000; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:30px; font-weight:400; }}
    .panel {{ position:absolute; left:90px; width:900px; border-radius:34px; background:rgba(12,12,12,.82); border:6px solid #000; box-shadow:0 10px 30px rgba(0,0,0,.4); }}
    .colhead {{ font-family:"Anton",sans-serif; font-size:{SUB}px; line-height:1; text-transform:uppercase; text-align:center; }}
    .sk {{ color:{LIME}; }} .bw {{ color:#fff; }}
    .mchip {{ height:52px; padding:0 20px 0 12px; border-radius:26px; display:flex; align-items:center; gap:9px; font-size:26px; white-space:nowrap; }}
    .mchip i {{ width:28px; height:28px; border-radius:50%; background:#000; display:flex; align-items:center; justify-content:center; flex:none; }}
    .mchip i svg {{ width:17px; height:17px; }}
    .mchip.l {{ background:{LIME}; color:#000; }} .mchip.w {{ background:#fff; color:#000; }} .mchip.y {{ background:{YEL}; color:#000; }}
    .vs {{ width:84px; height:84px; border-radius:50%; background:#E8252B; border:5px solid #fff; color:#fff; font-family:"Anton",sans-serif; font-size:40px;
          display:flex; align-items:center; justify-content:center; box-shadow:0 6px 16px rgba(0,0,0,.5); }}
    .sticker {{ position:absolute; left:0; right:0; margin:0 auto; width:max-content; padding:6px 30px 10px; background:{PINK}; color:#fff;
               font-family:"Anton",sans-serif; font-size:{SUB}px; line-height:1.15; text-transform:uppercase; transform:rotate(-3deg); box-shadow:0 6px 18px rgba(0,0,0,.45); }}'''
SM_CHK='<i><svg viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="#fff" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/></svg></i>'
def mchips(prefix, items, cls):
    return "".join(f'<div id="{prefix}{k}" class="mchip lbl {cls}">{SM_CHK}{t}</div>' for k,t in enumerate(items,1))
def tag(cid,num,text): return f'    <div id="{cid}-tag" class="tag"><b>{num}</b>{text}</div>'
def tagin(cid,t=0.05): return f'    tl.fromTo("#{cid}-tag", {{ opacity: 0, scale: 1.25 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "expo.out" }}, {t});'
RED="#E8252B"
XICON='<i style="background:#fff"><svg viewBox="0 0 24 24"><path d="M7 7l10 10M17 7L7 17" stroke="#E8252B" stroke-width="3.6" stroke-linecap="round"/></svg></i>'
MISTAKECSS=CHIPCSS+CMPCSS+f'''
    .xtag {{ position:absolute; left:0; right:0; margin:0 auto; width:max-content; padding:4px 26px 8px; background:{RED}; color:#fff;
            font-family:"Anton",sans-serif; font-size:{SUB}px; line-height:1.15; transform:rotate(-2deg); box-shadow:0 6px 18px rgba(0,0,0,.4); }}
    .pill.xr {{ background:#fff; color:#000; }}
    .why {{ position:absolute; left:0; width:1080px; text-align:center; font-size:26px; letter-spacing:2px; color:#fff; -webkit-text-stroke:4px #000; paint-order:stroke fill; }}
    .fix {{ position:absolute; left:0; right:0; margin:0 auto; width:max-content; max-width:900px; padding:6px 26px 10px; background:{LIME}; color:#000; text-align:center;
           font-family:"Anton",sans-serif; font-size:{SUB}px; line-height:1.15; transform:rotate(-2deg); box-shadow:0 6px 18px rgba(0,0,0,.45); }}'''
def xpills(prefix, items, y):
    cells="".join(f'<div id="{prefix}-p{k}" class="pill lbl xr">{XICON}{t}</div>' for k,t in enumerate(items,1))
    return f'    <div class="chiprow" style="top:{y}px">{cells}</div>', len(items)
def mistake(cid, num, title_html, why, items, fix_html, fix_t, dur, extra_body="", extra_js="", dy=0):
    pills,n=xpills(cid,items,820+dy)
    body=f'''    <div id="{cid}-tag" class="xtag" style="top:{612+dy}px">✗ KESILAPAN #{num}</div>
    <div id="{cid}-t" class="hl line" style="top:{680+dy}px">{title_html}</div>
    <div id="{cid}-why" class="why lbl" style="top:{782+dy}px">{why}</div>
{pills}
    <div id="{cid}-fix" class="fix" style="top:{920+dy}px; opacity:0">{fix_html}</div>
{extra_body}'''
    js=f'''    tl.fromTo("#{cid}-tag", {{ opacity: 0, scale: 1.4, rotation: -10 }}, {{ opacity: 1, scale: 1, rotation: -2, duration: 0.35, ease: "back.out(2)" }}, 0.05);
    tl.fromTo("#{cid}-t", {IN_SLAM}, 0.2);
    tl.fromTo("#{cid}-why", {IN_BLUR}, 0.75);
'''+"\n".join(pop(f"#{cid}-p{i}",round(0.95+(i-1)*0.3,2)) for i in range(1,n+1))+f'''
    tl.fromTo("#{cid}-fix", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.8)" }}, {fix_t});
{extra_js}'''+out(f'["#{cid}-tag","#{cid}-t","#{cid}-why",".pill","#{cid}-fix"]',round(dur-0.22,2))
    return scene(cid, MISTAKECSS, body, js)
# ---------- HOOK (0-4) ----------
W['hook']=scene('hook',MISTAKECSS+'''
    .xb { width:84px; height:84px; border-radius:50%; background:#E8252B; border:5px solid #fff; display:flex; align-items:center; justify-content:center; box-shadow:0 6px 16px rgba(0,0,0,.5); }
    .xb svg { width:44px; height:44px; }''',
'''    <div id="hook-t1" class="hl line y" style="top:380px">3 KESILAPAN</div>
    <div id="hook-t2" class="hl line" style="top:470px">LATIHAN SKIPPING</div>
    <div class="chiprow" style="top:584px; gap:24px">'''+"".join(f'<div id="hook-x{i}" class="xb"><svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18" stroke="#fff" stroke-width="4" stroke-linecap="round"/></svg></div>' for i in (1,2,3))+'''</div>
    <div id="hook-st" class="sticker" style="top:706px">KAU BUAT YANG MANA?</div>''',
f'''    tl.fromTo("#hook-t1", {{ scale: 1.14, y: -10, opacity: 1 }}, {{ scale: 1, y: 0, duration: 0.32, ease: "expo.out" }}, 0);
    tl.fromTo("#hook-t2", {{ scale: 1.14, y: 10, opacity: 1 }}, {{ scale: 1, y: 0, duration: 0.32, ease: "expo.out" }}, 0.04);
'''+"\n".join(f'    tl.fromTo("#hook-x{i}", {{ opacity: 0, scale: 2, rotation: -40 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.3, ease: "back.out(2)" }}, {round(0.45+(i-1)*0.2,2)});' for i in (1,2,3))+'''
    tl.fromTo("#hook-st", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(1.7)" }, 1.2);
'''+out('["#hook-t1","#hook-t2",".xb","#hook-st"]',3.78))
# ---------- KESILAPAN 1 (4-11) ----------
W['k1']=mistake('k1',1,'LOMPAT <span class="y">TERLALU TINGGI</span>','BERI IMPAK PADA',["TAPAK KAKI","LUTUT"],
  '✓ BETUL: LOMPAT RENDAH, 2–5 CM CUKUP',3.6,7.0,dy=130)
# ---------- KESILAPAN 2 (11-17.5) ----------
W['k2']=mistake('k2',2,'TAK PAKAI <span class="y">KASUT</span>','WALAUPUN DALAM RUMAH',["HENTAKAN TERUS KE KAKI"],
  '✓ KASUT BANTU SERAP IMPAK<br>SETIAP KALI HENTAKAN',3.0,6.5)
# ---------- KESILAPAN 3 (17.5-23) ----------
ROPE_SVG='''<svg viewBox="0 0 100 140" style="width:110px;height:154px;flex:none"><circle cx="50" cy="16" r="10" fill="#fff"/>
<path d="M50 28 V80 M50 80 L38 124 M50 80 L62 124 M50 40 L30 58 M50 40 L70 58" stroke="#fff" stroke-width="7" stroke-linecap="round" fill="none"/>
<path d="M28 50 Q16 126 50 128 Q84 126 72 50" stroke="#C8FF1E" stroke-width="4" fill="none"/>
<rect x="22" y="42" width="10" height="18" rx="4" fill="#FF3C8E"/><rect x="68" y="42" width="10" height="18" rx="4" fill="#FF3C8E"/>
<path d="M84 42 H96" stroke="#FFD60A" stroke-width="3" stroke-dasharray="3 3"/></svg>'''
W['k3']=mistake('k3',3,'TALI <span class="y">TERLALU PENDEK</span>','SENANG',["SANGKUT KAKI","TERLIBAS LEHER"],
  '✓ UKURAN BETUL',2.8,5.5,
  extra_body=f'''    <div id="k3-guide" class="panel" style="top:1000px; height:150px; display:flex; align-items:center; gap:22px; padding:0 34px; opacity:0">{ROPE_SVG}
      <div class="lbl" style="font-size:30px; line-height:1.3; color:#fff; text-transform:none">Pijak <span style="color:#C8FF1E">tengah tali</span>,<br>pemegang sampai <span style="color:#FFD60A">paras ketiak</span></div></div>''',
  extra_js='''    tl.fromTo("#k3-guide", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.4, ease: "expo.out" }, 3.1);
''')
W['k3']=W['k3'].replace('out(','out(') 
W['k3']=W['k3'].replace('"#k3-fix"]','"#k3-fix","#k3-guide"]')
# ---------- COUNTER (23-26) ----------
ccb,nc_=chiprows("ctr",[["KIRAAN","KALORI","JARAK","MASA"]],610)
W['counter']=scene('counter',CHIPCSS,
f'''    <div id="ctr-t0" class="lbl line" style="top:330px; text-align:center; font-size:28px; color:#C8FF1E; letter-spacing:3px; -webkit-text-stroke:4px #000; paint-order:stroke fill">ADA SEKALI</div>
    <div id="ctr-t1" class="hl line" style="top:372px">DIGITAL</div>
    <div id="ctr-t2" class="hl line g" style="top:462px">COUNTER</div>
{ccb}''',
f'''    tl.fromTo("#ctr-t0", {IN_BLUR}, 0.05);
    tl.fromTo("#ctr-t1", {{ opacity: 0, scale: 1.3, x: -24 }}, {{ opacity: 1, scale: 1, x: 0, duration: 0.3, ease: "expo.out" }}, 0.1);
    tl.fromTo("#ctr-t2", {{ opacity: 0, scale: 1.3, x: 24 }}, {{ opacity: 1, scale: 1, x: 0, duration: 0.3, ease: "expo.out" }}, 0.22);
'''+"\n".join(pop(f"#ctr-p{i}",round(0.5+(i-1)*0.25,2)) for i in range(1,nc_+1))+"\n"+out('["#ctr-t0","#ctr-t1","#ctr-t2",".pill"]',2.78))
# ---------- DUAL MODE (29.5-35.5) — tajuk di bawah paras muka ----------
W['dual']=scene('dual','',
'''    <div id="dual-t1" class="hl line" style="top:820px">DUAL <span class="g">MODE</span></div>
    <div id="dual-m1" class="sub line" style="top:916px">MODE 1: <span class="y">BOLA PEMBERAT</span></div>
    <div id="dual-m2" class="sub line" style="top:916px; opacity:0">MODE 2: <span class="y">TALI PANJANG</span></div>''',
f'''    tl.fromTo("#dual-t1", {IN_SLAM}, 0.05);
    tl.fromTo("#dual-m1", {{ opacity: 0, y: 16, filter: "blur(8px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.25, ease: "power4.out" }}, 0.3);
'''+out('["#dual-m1"]',2.75)+f'''
    tl.fromTo("#dual-m2", {{ opacity: 0, y: 16, filter: "blur(8px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.25, ease: "power4.out" }}, 3.05);
'''+out('["#dual-t1","#dual-m2"]',5.78))
# ---------- MESRA BEGINNERS (35.5-39) ----------
pmb,np_=chiprows("pem",[["MULA PERLAHAN","SENANG GUNA","TANPA SKILL KHAS"]],806,colors=("","yb","pk"))
W['pemula']=scene('pemula',CHIPCSS,
f'''    <div id="pem-t1" class="hl line" style="top:700px">MESRA <span class="y">BEGINNERS</span></div>
{pmb}''',
f'''    tl.fromTo("#pem-t1", {IN_SLAM}, 0.05);
'''+"\n".join(pop(f"#pem-p{i}",round(0.5+(i-1)*0.3,2)) for i in range(1,np_+1))+"\n"+out('["#pem-t1",".pill"]',3.28))
# ---------- CTA (35.5-41.1) — pilih warna ----------
W['cta']=scene('cta',CHIPCSS+'''
    .sw { height:60px; padding:0 26px 0 14px; border-radius:30px; display:flex; align-items:center; gap:12px; font-size:30px; color:#000; background:#fff; box-shadow:0 6px 18px rgba(0,0,0,.45); }
    .sw b { width:34px; height:34px; border-radius:50%; border:3px solid #000; display:block; }
    #cta-btn { position:absolute; left:0; right:0; margin:0 auto; top:1030px; width:max-content; padding:6px 30px 10px; border-radius:40px; background:#C8FF1E;
               font-family:"Anton",sans-serif; font-size:47px; line-height:1.15; color:#000; box-shadow:0 8px 24px rgba(0,0,0,.5); }
    #cta-arrow { position:absolute; left:0; right:0; margin:0 auto; top:1112px; width:60px; height:60px; }''',
'''    <div id="cta-a" class="sub line" style="top:300px">TAHUN 2027</div>
    <div id="cta-b" class="hl line" style="top:356px">NAK START <span class="y">SKIPPING?</span></div>
    <div class="chiprow" style="top:946px"><div id="cta-pink" class="sw lbl"><b style="background:#F7A8C8"></b>PINK</div><div id="cta-ungu" class="sw lbl"><b style="background:#B9A3E8"></b>UNGU</div></div>
    <div id="cta-btn">PILIH WARNA DEKAT LINK BAWAH</div>
    <svg id="cta-arrow" viewBox="0 0 24 24"><path d="M12 3v16M5 13l7 7 7-7" stroke="#000" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" fill="none"/><path d="M12 3v16M5 13l7 7 7-7" stroke="#C8FF1E" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>''',
f'''    tl.fromTo("#cta-a", {IN_BLUR}, 0.05);
    tl.fromTo("#cta-b", {IN_SLAM}, 0.12);
    tl.fromTo("#cta-pink", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1.12, duration: 0.3, ease: "back.out(1.7)" }}, 0.6);
    tl.fromTo("#cta-ungu", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 0.55, scale: 1, duration: 0.3, ease: "back.out(1.7)" }}, 0.75);
    tl.to("#cta-pink", {{ scale: 1, opacity: 0.55, duration: 0.2 }}, 2.8);
    tl.to("#cta-ungu", {{ scale: 1.12, opacity: 1, duration: 0.2 }}, 2.8);
    tl.fromTo("#cta-btn", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.8)" }}, 1.3);
    tl.fromTo("#cta-arrow", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, 1.6);
    tl.fromTo("#cta-arrow", {{ y: -10 }}, {{ y: 10, duration: 0.35, ease: "sine.inOut", yoyo: true, repeat: 8 }}, 1.6);''')
# ---------- CAPTIONS ----------
groups=[(26.8,28.8,"TAK SANGKUT KAKI",["SANGKUT"]),(29.6,31.8,"NAK LEBIH CABARAN?",["CABARAN?"]),
(33.0,34.1,"SESUAI UNTUK",[]),(34.1,35.3,"SEMUA PERINGKAT",["SEMUA"])]
html=[];js=[]
for gi,(s,e,txt,kw) in enumerate(groups,1):
    words=txt.split(); n=len(words)
    spans=" ".join(f'<span id="cap{gi}w{wi}" class="w{" kw" if w in kw else ""}">{w}</span>' for wi,w in enumerate(words,1))
    html.append(f'    <div id="cap{gi}" class="clip cg" data-start="{s}" data-duration="{round(e-s,3)}" data-track-index="0"><div id="cap{gi}i" class="ci">{spans}</div></div>')
    js.append(f'    tl.fromTo("#cap{gi}i", {{ scale: 0.82, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.16, ease: "back.out(2)" }}, {s});')
    tot=sum(len(w)+2 for w in words); span=e-s-0.12; t=s
    for wi,w in enumerate(words,1):
        d=span*(len(w)+2)/tot; base="#39FF14" if w in kw else "#ffffff"; act="#39FF14" if w in kw else "#FFE600"
        js.append(f'    tl.set("#cap{gi}w{wi}", {{ color: "{act}", scale: 1.12 }}, {round(t,3)});')
        if wi<n: js.append(f'    tl.set("#cap{gi}w{wi}", {{ color: "{base}", scale: 1 }}, {round(t+d,3)});')
        t+=d
    js.append(f'    tl.to("#cap{gi}i", {{ opacity: 0, duration: 0.1, ease: "power2.in" }}, {round(e-0.1,3)});')
W['captions']=scene('captions',f'''
    .cg {{ position:absolute; left:0; top:1178px; width:1080px; height:70px; overflow: visible; }}
    .ci {{ width:1080px; text-align:center; font-family:"Anton",sans-serif; font-size:{CAP}px; line-height:70px; color:#fff; text-transform:uppercase;
          -webkit-text-stroke: 6px #000; paint-order: stroke fill; text-shadow: 0 4px 10px rgba(0,0,0,.6); letter-spacing: 1px; }}
    .w {{ display:inline-block; color:#fff; margin: 0 4px; }}
    .w.kw {{ color:#39FF14; }}''', "\n".join(html), "\n".join(js))
for k,v in W.items(): open(f'{P}/compositions/{k}.html','w').write(v)
# ---------- INDEX ----------
data=None
L={'m1_hook':-37.4,'m2_tinggi':-26.2,'m3_kasut':-32.9,'m4_tali':-32.9,'m5_counter':-49.7,'m6_bola':-50.7,'m7_panjang':-22.7,'m8_pemula':-33.5,'m9_pink':-48.4,'m10_ungu':-65.1}
clips=[("m1_hook",0,4.0),("m2_tinggi",4,7.0),("m3_kasut",11,6.5),("m4_tali",17.5,5.5),("m5_counter",23,3.0),("m6_bola",26,3.0),("m7_panjang",29,3.0),("m8_pemula",32,3.5),("m9_pink",35.5,2.8),("m10_ungu",38.3,2.8)]
DUR=41.1
cuts=[s for _,s,_ in clips[1:]]
sfx_len={"whoosh":0.55,"pop":0.12,"ding":1.4,"impact":0.9,"chaching":1.2,"riser":1.3,"zap":0.3}
sfx=[("impact",0.0),("zap",0.45),("zap",0.65),("zap",0.85),("pop",1.25),("riser",2.6)]+[("whoosh",round(c-0.3,2)) for c in cuts]
for s0,fx,np_ in ((4,3.6,2),(11,3.0,1),(17.5,2.8,2)):
    sfx+=[("impact",s0+0.05),("zap",round(s0+0.15,2))]+[("pop",round(s0+0.95+i*0.3,2)) for i in range(np_)]+[("ding",round(s0+fx,2))]
sfx+=[("pop",20.6)]
sfx+=[("impact",23.05)]+[("pop",round(23.5+i*0.25,2)) for i in range(4)]
sfx+=[("impact",26.05),("zap",29.05),("impact",32.05),("pop",32.5),("pop",32.8),("pop",33.1),("riser",34.2)]
sfx+=[("impact",35.55),("pop",36.1),("ding",36.8),("pop",38.3),("chaching",39.2)]
sfx.sort(key=lambda s:s[1]); lanes=[]; au=[]
for i,(n,t) in enumerate(sfx):
    e=t+sfx_len[n]
    for li,end in enumerate(lanes):
        if end<=t: lanes[li]=e; break
    else: lanes.append(e); li=len(lanes)-1
    au.append(f'      <audio id="sfx{i+1:02d}" class="clip" src="assets/sfx/{n}.wav" data-start="{t}" data-duration="{sfx_len[n]}" data-volume="1" data-track-index="{10+li}"></audio>')
vids=[]; gains=[]
for i,(n,s,d) in enumerate(clips):
    g=min(-57-L[n],12); v=round(10**(g/20),4); gains.append((n,L[n],round(g,1),v))
    vids.append(f'''      <div id="w{i+1}" class="wrap" style="z-index:{i+1}">
        <video id="v{i+1}" class="clip" src="assets/media/{n}.mp4" data-start="{s}" data-duration="{d}" data-media-start="0" data-volume="{v}" data-has-audio="true" playsinline data-track-index="0"></video>
      </div>''')
scenes=[("hook",0,4),("k1",4,7),("k2",11,6.5),("k3",17.5,5.5),("counter",23,3.0),("dual",26,6),("pemula",32,3.5),("cta",35.5,5.6)]
sc=[f'      <div id="{n}" data-composition-id="{n}" data-composition-src="compositions/{n}.html" data-start="{s}" data-duration="{d}" data-width="1080" data-height="1920" data-track-index="1" data-track-kind="graphics" style="z-index:20"></div>' for n,s,d in scenes]
zoom="\n".join(f'      tl.fromTo("#w{i+1}", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.7, ease: "expo.out" }}, {s});' for i,(n,s,d) in enumerate(clips))
flash="\n".join(f'      tl.fromTo("#flash", {{ opacity: 0.85 }}, {{ opacity: 0, duration: 0.24, ease: "power2.out" }}, {c});' for c in cuts)
nl="\n"
open(f'{P}/index.html','w').write(f'''<!doctype html>
<html lang="ms">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; }}
      #bg {{ position: absolute; inset: 0; background: #000; z-index: 0; }}
      .wrap {{ position: absolute; inset: 0; overflow: hidden; }}
      .wrap video {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
      #flash {{ position: absolute; inset: 0; background: #fff; opacity: 0; z-index: 40; pointer-events: none; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920" data-fps="60">
      <div id="bg"></div>
{nl.join(vids)}
{nl.join(sc)}
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920" data-track-index="2" data-track-kind="captions" style="z-index:30"></div>
      <div id="flash" data-layout-ignore></div>
{nl.join(au)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      // Zoom masuk ringkas pada setiap klip
{zoom}
      // Kilatan putih pada setiap potongan
      tl.set("#flash", {{ opacity: 0 }}, 0);
{flash}
      tl.set("#flash", {{ opacity: 0 }}, {DUR-0.01});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
''')
print("gains:",gains); print(len(au),"sfx",len(lanes),"lanes")
