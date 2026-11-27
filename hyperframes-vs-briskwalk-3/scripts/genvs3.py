import os, math
P='/home/user/hf/skippingvs3'
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
# ---------- HOOK (0-4) ----------
W['hook']=scene('hook',CMPCSS+'''
    #hook-shade { display:none; }
    #hook-vsw { position:absolute; left:0; width:1080px; top:536px; display:flex; justify-content:center; }''',
'''    <div id="hook-shade"></div>
    <div id="hook-t1" class="hl line g" style="top:440px">SKIPPING</div>
    <div id="hook-vsw"><div id="hook-vs" class="vs">VS</div></div>
    <div id="hook-t2" class="hl line" style="top:624px">BRISKWALK</div>
    <div id="hook-st" class="sticker" style="top:744px">MANA LAGI BERKESAN?</div>''',
f'''    tl.fromTo("#hook-t1", {{ scale: 1.14, x: -20, opacity: 1 }}, {{ scale: 1, x: 0, duration: 0.32, ease: "expo.out" }}, 0);
    tl.fromTo("#hook-t2", {{ scale: 1.14, x: 20, opacity: 1 }}, {{ scale: 1, x: 0, duration: 0.32, ease: "expo.out" }}, 0.04);
    tl.fromTo("#hook-vs", {{ scale: 1.6, rotation: -30, opacity: 1 }}, {{ scale: 1, rotation: 0, duration: 0.4, ease: "back.out(2)" }}, 0.1);
    tl.fromTo("#hook-st", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(1.7)" }}, 0.6);
'''+out('["#hook-t1","#hook-t2","#hook-vs","#hook-st","#hook-shade"]',3.78))
# ---------- 2. KALORI 10 MINIT (9.5-19.5) ----------
MET_SK, MET_BW = 11.8, 4.3
data=[(w, int(MET_BW*3.5*w/200*20+0.5), int(MET_SK*3.5*w/200*20+0.5)) for w in (50,60,70,80,90,100)]
mx=max(v for _,_,v in data); ratio=round(MET_SK/MET_BW,1)
rows="".join(f'''
      <div id="cal-r{i}" class="crow"><div class="ckg">{w}KG</div>
        <div class="ctr bwt"><div id="cal-bb{i}" class="cbar bwb" data-pct="{round(b/mx,4)}"></div></div><div class="cnum"><span id="cal-nb{i}" data-v="{b}">0</span></div>
        <div class="ctr skt"><div id="cal-sb{i}" class="cbar skb" data-pct="{round(s/mx,4)}"></div></div><div class="cnum sk"><span id="cal-ns{i}" data-v="{s}">0</span></div></div>''' for i,(w,b,s) in enumerate(data,1))
W['cal']=scene('cal',CMPCSS+f'''
    #cal-p {{ top:404px; height:740px; padding:20px 40px 0; }}
    .chead {{ display:flex; height:44px; align-items:center; font-size:24px; letter-spacing:2px; color:#9a9a9a; }}
    .crow {{ display:flex; align-items:center; height:104px; border-top:1px solid rgba(255,255,255,.06); }}
    .ckg {{ width:140px; font-family:"Anton",sans-serif; font-size:50px; line-height:1; color:#fff; }}
    .ctr {{ height:24px; border-radius:12px; background:rgba(255,255,255,.12); overflow:hidden; }}
    .bwt {{ width:150px; }} .skt {{ width:220px; margin-left:14px; }}
    .cbar {{ width:100%; height:100%; border-radius:12px; transform-origin:0 50%; }}
    .bwb {{ background:#9aa3a8; }} .skb {{ background:linear-gradient(90deg,{YEL},{LIME}); }}
    .cnum {{ width:96px; text-align:right; font-family:"Anton",sans-serif; font-size:{SUB}px; color:#fff; line-height:1; padding-right:6px; }}
    .cnum.sk {{ color:{LIME}; width:110px; }}
    #cal-note {{ font-size:{CHIP}px; font-weight:600; color:#bbb; text-transform:none; letter-spacing:0; margin-top:12px; text-align:center; }}''',
f'''    <div class="topshade" id="cal-shade"></div>
{tag("cal","1","KALORI DALAM 20 MINIT")}
    <div id="cal-p" class="panel">
      <div class="chead lbl"><span style="width:140px">BERAT</span><span style="width:246px">BRISKWALK</span><span class="sk" style="width:330px; text-align:center">SKIPPING</span></div>{rows}
      <div id="cal-note" class="lbl">*Anggaran. MET briskwalk {MET_BW}, skipping {MET_SK} (Compendium of Physical Activities)</div>
    </div>
    <div id="cal-st" class="sticker" style="top:1160px; opacity:0">SKIPPING ±{ratio}X LEBIH BANYAK!</div>''',
f'''{tagin("cal")}
    tl.fromTo("#cal-p", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "expo.out" }}, 0.2);
    for (let i = 1; i <= 6; i++) {{
      for (const k of ["b","s"]) {{
        const bar = document.querySelector("#cal-" + k + "b" + i), num = document.querySelector("#cal-n" + k + i);
        const pct = parseFloat(bar.dataset.pct), v = parseInt(num.dataset.v, 10);
        const t0 = k === "b" ? 0.7 : 2.4;
        tl.fromTo(bar, {{ scaleX: 0 }}, {{ scaleX: pct, duration: 1.4, ease: "power2.out" }}, t0);
        const o = {{ n: 0 }};
        tl.fromTo(o, {{ n: 0 }}, {{ n: v, duration: 1.4, ease: "power2.out", onUpdate: () => {{ num.textContent = Math.round(o.n); }} }}, t0);
      }}
    }}
    tl.fromTo("#cal-st", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.8)" }}, 5.0);
'''+out('["#cal-tag","#cal-p","#cal-st","#cal-shade"]',9.78))
# ---------- 3. OTOT (19.5-25.5) ----------
def body(prefix, hi, col):
    # front-view figure; hi = set of parts to highlight
    parts={"head":'<circle cx="60" cy="22" r="15"/>',
           "bahu":'<path d="M30 46 Q60 34 90 46 L86 58 Q60 50 34 58 Z"/>',
           "dada":'<rect x="38" y="58" width="44" height="24" rx="6"/>',
           "core":'<rect x="42" y="84" width="36" height="34" rx="6"/>',
           "lengan":'<rect x="16" y="50" width="14" height="62" rx="7"/><rect x="90" y="50" width="14" height="62" rx="7"/>',
           "pinggul":'<rect x="40" y="120" width="40" height="16" rx="6"/>',
           "peha":'<rect x="40" y="138" width="18" height="50" rx="8"/><rect x="62" y="138" width="18" height="50" rx="8"/>',
           "betis":'<rect x="42" y="192" width="15" height="46" rx="7"/><rect x="63" y="192" width="15" height="46" rx="7"/>'}
    g=[]
    for k,v in parts.items():
        on = k in hi
        g.append(f'<g id="{prefix}-{k}" fill="{"#3a3a3a" if not on else "#3a3a3a"}" stroke="#777" stroke-width="2" data-on="{1 if on else 0}">{v}</g>')
    return f'<svg viewBox="0 0 120 245" class="bodysvg">{"".join(g)}</svg>'
SK_PARTS=["bahu","lengan","core","peha","betis"]; BW_PARTS=["peha","betis"]
def meter(prefix,n,col):
    return '<div class="meter">'+"".join(f'<span id="{prefix}{k}" class="dot" data-c="{col if k<=n else ""}"></span>' for k in range(1,6))+'</div>'
W['otot']=scene('otot',CMPCSS+f'''
    #otot-p {{ top:404px; height:740px; display:flex; justify-content:space-between; padding:24px 34px 0; }}
    .ocol {{ width:400px; display:flex; flex-direction:column; align-items:center; gap:12px; }}
    .bodysvg {{ width:170px; height:347px; }}
    .ochips {{ display:flex; flex-wrap:wrap; justify-content:center; gap:8px; min-height:112px; align-content:flex-start; }}
    .klabel {{ font-size:24px; letter-spacing:2px; color:#9a9a9a; margin-top:6px; }}
    .meter {{ display:flex; gap:10px; }}
    .dot {{ width:46px; height:18px; border-radius:9px; background:rgba(255,255,255,.14); }}''',
f'''    <div class="topshade" id="otot-shade"></div>
{tag("otot","2","OTOT &amp; KOORDINASI")}
    <div id="otot-p" class="panel">
      <div class="ocol"><div class="colhead sk">SKIPPING</div>{body("osk",SK_PARTS,LIME)}
        <div class="ochips">{mchips("otot-a",["BAHU &amp; LENGAN","PERUT / CORE","PEHA","BETIS"],"l")}</div>
        <div class="klabel lbl">KOORDINASI</div>{meter("osk-k",5,LIME)}</div>
      <div class="ocol"><div class="colhead bw">BRISKWALK</div>{body("obw",BW_PARTS,YEL)}
        <div class="ochips">{mchips("otot-b",["PEHA","BETIS"],"y")}</div>
        <div class="klabel lbl">KOORDINASI</div>{meter("obw-k",2,YEL)}</div>
    </div>
    <div id="otot-st" class="sticker" style="top:1160px; opacity:0">TANGAN + KAKI SERENTAK!</div>''',
f'''{tagin("otot")}
    tl.fromTo("#otot-p", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "expo.out" }}, 0.2);
'''+"\n".join(f'    tl.fromTo("#obw-{p}", {{ fill: "#3a3a3a" }}, {{ fill: "{YEL}", duration: 0.25 }}, {round(0.8+i*0.3,2)});' for i,p in enumerate(BW_PARTS))
+"\n"+"\n".join(pop(f"#otot-b{i}",round(0.9+(i-1)*0.3,2)) for i in range(1,3))
+"\n"+"\n".join(f'    tl.fromTo("#osk-{p}", {{ fill: "#3a3a3a" }}, {{ fill: "{LIME}", duration: 0.25 }}, {round(1.8+i*0.3,2)});' for i,p in enumerate(SK_PARTS))
+"\n"+"\n".join(pop(f"#otot-a{i}",round(1.9+(i-1)*0.35,2)) for i in range(1,5))
+"\n"+"\n".join(f'    tl.fromTo("#obw-k{k}", {{ backgroundColor: "rgba(255,255,255,0.14)" }}, {{ backgroundColor: "{YEL}", duration: 0.15 }}, {round(3.6+k*0.12,2)});' for k in range(1,3))
+"\n"+"\n".join(f'    tl.fromTo("#osk-k{k}", {{ backgroundColor: "rgba(255,255,255,0.14)" }}, {{ backgroundColor: "{LIME}", duration: 0.15 }}, {round(4.0+k*0.12,2)});' for k in range(1,6))
+f'''
    tl.fromTo("#otot-st", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.8)" }}, 4.8);
'''+out('["#otot-tag","#otot-p","#otot-st","#otot-shade"]',6.78))
# ---------- 3. RUANG & PERALATAN (21-26.5) ----------
ICON_ROOM='''<svg viewBox="0 0 100 100"><rect x="18" y="18" width="64" height="64" rx="6" fill="none" stroke="#000" stroke-width="5"/><path d="M18 50 H82 M50 18 V82" stroke="#000" stroke-width="2" opacity=".25"/><circle cx="50" cy="40" r="6" fill="#000"/><path d="M50 47 V64 M42 54 L58 54" stroke="#000" stroke-width="5" stroke-linecap="round"/><path d="M38 58 Q50 86 62 58" stroke="#E8252B" stroke-width="3" fill="none"/></svg>'''
ICON_ROAD='''<svg viewBox="0 0 100 100"><path d="M36 92 L46 8 M64 92 L54 8" stroke="#000" stroke-width="5" stroke-linecap="round"/><path d="M50 84 V72 M50 60 V50 M50 40 V32 M50 24 V18" stroke="#E8252B" stroke-width="4" stroke-linecap="round"/></svg>'''
W['ruang']=scene('ruang',CMPCSS+'''
    #ruang-tag { top:590px; }
    #ruang-p { top:676px; height:452px; display:flex; justify-content:space-between; padding:22px 34px 0; }
    .rcol { width:400px; display:flex; flex-direction:column; align-items:center; gap:10px; }
    .ricon { width:120px; height:120px; border-radius:50%; background:#fff; display:flex; align-items:center; justify-content:center; }
    .ricon svg { width:92px; height:92px; }
    .rlabel { font-size:24px; letter-spacing:2px; color:#9a9a9a; margin-top:2px; }
    .rchips { display:flex; flex-direction:column; align-items:center; gap:8px; }''',
f'''{tag("ruang","3","RUANG &amp; PERALATAN")}
    <div id="ruang-p" class="panel">
      <div class="rcol"><div class="colhead sk">SKIPPING</div><div class="ricon" id="ruang-i1">{ICON_ROOM}</div>
        <div class="rlabel lbl">RUANG</div><div class="rchips">{mchips("ruang-a",["KECIL, ±2M × 2M"],"l")}</div>
        <div class="rlabel lbl">PERALATAN</div><div class="rchips">{mchips("ruang-c",["SEUTAS TALI, MUAT BEG"],"l")}</div></div>
      <div class="rcol"><div class="colhead bw">BRISKWALK</div><div class="ricon" id="ruang-i2">{ICON_ROAD}</div>
        <div class="rlabel lbl">RUANG</div><div class="rchips">{mchips("ruang-b",["LALUAN PANJANG / TREK"],"w")}</div>
        <div class="rlabel lbl">PERALATAN</div><div class="rchips">{mchips("ruang-d",["KASUT SESUAI"],"w")}</div></div>
    </div>''',
f'''{tagin("ruang")}
    tl.fromTo("#ruang-p", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "expo.out" }}, 0.2);
'''+"\n".join([pop("#ruang-a1",0.9),pop("#ruang-b1",1.3),pop("#ruang-c1",2.0),pop("#ruang-d1",2.4)])+"\n"+out('["#ruang-tag","#ruang-p"]',5.28))
# ---------- DUAL MODE# ---------- DUAL MODE (25.5-31.5) ----------
# ---------- COUNTER (26.5-29.5) ----------
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
# ---------- CTA (39-44.5) — di bawah paras muka ----------
W['cta']=scene('cta','''
    #cta-cal { position:absolute; left:0; right:0; margin:0 auto; top:740px; width:220px; height:210px; border-radius:22px; background:#fff; overflow:hidden; box-shadow:0 10px 30px rgba(0,0,0,.5); }
    #cta-cal .hd { height:56px; background:#E8252B; color:#fff; font-family:"MontserratV",sans-serif; font-weight:800; font-size:24px; letter-spacing:3px; display:flex; align-items:center; justify-content:center; }
    #cta-cal .yr { font-family:"Anton",sans-serif; font-size:96px; line-height:154px; text-align:center; color:#111; }
    #cta-st { position:absolute; left:0; right:0; margin:0 auto; width:max-content; top:1022px; padding:4px 26px 8px; background:#C8FF1E; color:#000; font-family:"Anton",sans-serif; font-size:47px; line-height:1.15; transform:rotate(-2deg); box-shadow:0 6px 18px rgba(0,0,0,.45); }
    #cta-btn { position:absolute; left:0; right:0; margin:0 auto; top:1112px; width:max-content; padding: 6px 36px 10px; border-radius:60px;
               background:#fff; font-family:"Anton",sans-serif; font-size:64px; line-height:1.1; color:#000; box-shadow: 0 8px 24px rgba(0,0,0,.5); }''',
'''    <div id="cta-cal"><div class="hd">JANUARI</div><div class="yr">2027</div></div>
    <div id="cta-a" class="sub line" style="top:962px">TAHUN 2027</div>
    <div id="cta-st">NAK UPGRADE BODY?</div>
    <div id="cta-btn">START SKIPPING SEKARANG!</div>''',
f'''    tl.fromTo("#cta-cal", {{ opacity: 0, y: -60, rotation: -8 }}, {{ opacity: 1, y: 0, rotation: 0, duration: 0.5, ease: "back.out(1.6)" }}, 0.05);
    tl.fromTo("#cta-a", {IN_BLUR}, 0.5);
    tl.fromTo("#cta-st", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.8)" }}, 0.8);
    tl.fromTo("#cta-btn", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.8)" }}, 2.3);''')
# ---------- CAPTIONS ----------
groups=[(30.3,32.2,"TAK TERSANGKUT KAKI",["TERSANGKUT"]),(33.1,35.3,"NAK LEBIH CABARAN?",["CABARAN?"]),
(36.5,37.6,"SESUAI UNTUK",[]),(37.6,38.8,"SEMUA PERINGKAT",["SEMUA"])]
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
L={'k1_hook':-40.5,'k2_cal':-54.8,'k3_cal':-38.2,'k4_otot':-28.0,'k5_ruang':-52.1,'k6_counter':-63.4,'k7_bola':-37.4,'k8_tali':-39.5,'k9_pemula':-44.7,'k10_cta':-29.4}
clips=[("k1_hook",0,4.0),("k2_cal",4,5.0),("k3_cal",9,5.0),("k4_otot",14,7.0),("k5_ruang",21,5.5),("k6_counter",26.5,3.0),("k7_bola",29.5,3.0),("k8_tali",32.5,3.0),("k9_pemula",35.5,3.5),("k10_cta",39,5.5)]
DUR=44.5
cuts=[s for _,s,_ in clips[1:]]
sfx_len={"whoosh":0.55,"pop":0.12,"ding":1.4,"impact":0.9,"chaching":1.2,"riser":1.3,"zap":0.3}
sfx=[("impact",0.0),("zap",0.1),("pop",0.6),("riser",2.6)]+[("whoosh",round(c-0.3,2)) for c in cuts if c!=9]
sfx+=[("impact",4.05),("pop",4.7),("pop",6.4),("chaching",9.05),("ding",10.0)]
sfx+=[("impact",14.05),("pop",14.9),("pop",15.2),("pop",15.9),("pop",16.25),("pop",16.6),("pop",16.95),("zap",18.1),("ding",18.8)]
sfx+=[("impact",21.05),("pop",21.9),("pop",22.3),("pop",23.0),("pop",23.4)]
sfx+=[("impact",26.55),("pop",27.0),("pop",27.25),("pop",27.5),("pop",27.75)]
sfx+=[("impact",29.55),("zap",32.55),("impact",35.55),("pop",36.0),("pop",36.3),("pop",36.6),("riser",37.7)]
sfx+=[("impact",39.05),("pop",39.8),("ding",41.3),("chaching",41.9)]
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
scenes=[("hook",0,4),("cal",4,10),("otot",14,7),("ruang",21,5.5),("counter",26.5,3.0),("dual",29.5,6),("pemula",35.5,3.5),("cta",39,5.5)]
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
print("calories:",data); print("gains:",gains); print(len(au),"sfx",len(lanes),"lanes")
