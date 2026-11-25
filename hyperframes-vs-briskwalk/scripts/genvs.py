import os, math
P='/home/user/hf/skippingvs'
# ---- format (CLAUDE.md, updated) ----
HL, SUB, CAP, CHIP = 100, 47, 40, 19
css=f'''    @font-face {{ font-family: "Anton"; src: url("assets/fonts/Anton-Regular.ttf") format("truetype"); font-weight: 400; }}
    @font-face {{ font-family: "MontserratV"; src: url("assets/fonts/Montserrat.ttf") format("truetype"); font-weight: 100 900; }}
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    .hl {{ font-family: "Anton", sans-serif; font-size: {HL}px; line-height: 1.04; color: #fff; text-transform: uppercase; text-align: center;
          -webkit-text-stroke: 7px #000; paint-order: stroke fill; text-shadow: 0 6px 18px rgba(0,0,0,.55); letter-spacing: 1px; }}
    .sub {{ font-family: "Anton", sans-serif; font-size: {SUB}px; line-height: 1.15; color: #fff; text-transform: uppercase; text-align: center;
           -webkit-text-stroke: 5px #000; paint-order: stroke fill; text-shadow: 0 4px 12px rgba(0,0,0,.5); letter-spacing: 1px; }}
    .y {{ color: #FFE600; }} .g {{ color: #39FF14; }}
    .lbl {{ font-family: "MontserratV", sans-serif; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; }}
    .topshade {{ position: absolute; left: 0; top: 0; width: 1080px; height: 760px; background: linear-gradient(rgba(0,0,0,.5), rgba(0,0,0,0)); }}
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
    .chiprow {{ position:absolute; left:0; width:1080px; display:flex; justify-content:center; gap:20px; }}
    .pill {{ height:80px; padding: 0 30px 0 20px; border-radius:40px; background:#C8FF1E; border:none;
            display:flex; align-items:center; gap:12px; font-size:40px; color:#000; white-space:nowrap; box-shadow: 0 6px 18px rgba(0,0,0,.45); }}
    .pill.yb {{ background:#FFD60A; }} .pill.pk {{ background:#FF3C8E; color:#fff; }}
    .pill i {{ width:38px; height:38px; border-radius:50%; background:#000; display:flex; align-items:center; justify-content:center; flex:none; }}
    .pill i svg {{ width:22px; height:22px; }}'''
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
    .panel {{ position:absolute; left:40px; width:1000px; border-radius:34px; background:rgba(12,12,12,.82); border:6px solid #000; box-shadow:0 10px 30px rgba(0,0,0,.4); }}
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
    #hook-shade { position:absolute; left:0; top:330px; width:1080px; height:560px; background: radial-gradient(ellipse at center, rgba(0,0,0,.45), rgba(0,0,0,0) 70%); }
    #hook-vsw { position:absolute; left:0; width:1080px; top:500px; display:flex; justify-content:center; }''',
'''    <div id="hook-shade"></div>
    <div id="hook-t1" class="hl line g" style="top:388px">SKIPPING</div>
    <div id="hook-vsw"><div id="hook-vs" class="vs">VS</div></div>
    <div id="hook-t2" class="hl line" style="top:590px">BRISKWALK</div>
    <div id="hook-st" class="sticker" style="top:724px">MANA LAGI BERKESAN?</div>''',
f'''    tl.fromTo("#hook-t1", {{ scale: 1.14, x: -20, opacity: 1 }}, {{ scale: 1, x: 0, duration: 0.32, ease: "expo.out" }}, 0);
    tl.fromTo("#hook-t2", {{ scale: 1.14, x: 20, opacity: 1 }}, {{ scale: 1, x: 0, duration: 0.32, ease: "expo.out" }}, 0.04);
    tl.fromTo("#hook-vs", {{ scale: 1.6, rotation: -30, opacity: 1 }}, {{ scale: 1, rotation: 0, duration: 0.4, ease: "back.out(2)" }}, 0.1);
    tl.fromTo("#hook-st", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(1.7)" }}, 0.6);
'''+out('["#hook-t1","#hook-t2","#hook-vs","#hook-st","#hook-shade"]',3.78))
# ---------- 1. JENIS PERGERAKAN (4-9.5) ----------
ICON_JUMP='''<svg viewBox="0 0 100 100"><circle cx="50" cy="20" r="8" fill="#000"/><path d="M50 30 L50 56 M50 38 L34 48 M50 38 L66 48 M50 56 L40 74 M50 56 L60 74" stroke="#000" stroke-width="7" stroke-linecap="round" fill="none"/>
<path d="M34 48 Q50 104 66 48" stroke="#E8252B" stroke-width="3.5" fill="none" stroke-dasharray="5 4"/><path d="M30 86 L70 86" stroke="#000" stroke-width="3" opacity=".35"/><path d="M50 80 L50 92 M45 86 L50 92 L55 86" stroke="#E8252B" stroke-width="3" fill="none" transform="rotate(180 50 86)"/></svg>'''
ICON_WALK='''<svg viewBox="0 0 100 100"><circle cx="54" cy="18" r="8" fill="#000"/><path d="M52 28 L46 54 M50 36 L36 46 M50 36 L64 44 M46 54 L36 76 M46 54 L60 74" stroke="#000" stroke-width="7" stroke-linecap="round" fill="none"/>
<path d="M24 88 L78 88 M70 82 L78 88 L70 94" stroke="#E8252B" stroke-width="4" stroke-linecap="round" fill="none"/></svg>'''
W['gerak']=scene('gerak',CMPCSS+'''
    #gerak-p { top:392px; height:520px; display:flex; align-items:flex-start; justify-content:space-between; padding:30px 34px 0; }
    .gcol { width:400px; display:flex; flex-direction:column; align-items:center; gap:14px; }
    .gicon { width:170px; height:170px; border-radius:50%; background:#fff; display:flex; align-items:center; justify-content:center; }
    .gicon svg { width:130px; height:130px; }
    .gchips { display:flex; flex-direction:column; align-items:center; gap:10px; margin-top:4px; }
    #gerak-vsw { align-self:center; margin-top:-60px; }''',
f'''    <div class="topshade" id="gerak-shade"></div>
{tag("gerak","1","JENIS PERGERAKAN")}
    <div id="gerak-p" class="panel">
      <div class="gcol" id="gerak-c1"><div class="colhead sk">SKIPPING</div><div class="gicon" id="gerak-i1">{ICON_JUMP}</div>
        <div class="gchips">{mchips("gerak-a",["LOMPAT DI TEMPAT","KARDIO TINGGI","RUANG KECIL CUKUP"],"l")}</div></div>
      <div id="gerak-vsw"><div id="gerak-vs" class="vs">VS</div></div>
      <div class="gcol" id="gerak-c2"><div class="colhead bw">BRISKWALK</div><div class="gicon" id="gerak-i2">{ICON_WALK}</div>
        <div class="gchips">{mchips("gerak-b",["JALAN KE DEPAN","INTENSITI SEDERHANA","PERLU LALUAN"],"w")}</div></div>
    </div>''',
f'''{tagin("gerak")}
    tl.fromTo("#gerak-p", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "expo.out" }}, 0.2);
    tl.fromTo("#gerak-vs", {{ scale: 0.3, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2)" }}, 0.55);
    tl.fromTo("#gerak-i1", {{ y: 0 }}, {{ y: -16, duration: 0.25, ease: "power2.out", yoyo: true, repeat: 5 }}, 0.8);
    tl.fromTo("#gerak-i2", {{ x: -10 }}, {{ x: 10, duration: 0.75, ease: "sine.inOut", yoyo: true, repeat: 1 }}, 0.8);
'''+"\n".join(pop(f"#gerak-a{i}",round(1.0+(i-1)*0.6,2))+"\n"+pop(f"#gerak-b{i}",round(1.3+(i-1)*0.6,2)) for i in range(1,4))+"\n"+out('["#gerak-tag","#gerak-p","#gerak-shade"]',5.28))
# ---------- 2. KALORI 10 MINIT (9.5-19.5) ----------
MET_SK, MET_BW = 11.8, 4.3
data=[(w, int(MET_BW*3.5*w/200*10+0.5), int(MET_SK*3.5*w/200*10+0.5)) for w in (50,60,70,80,90,100)]
mx=max(s for _,_,s in data); ratio=round(MET_SK/MET_BW,1)
rows="".join(f'''
      <div id="cal-r{i}" class="crow"><div class="ckg">{w}KG</div>
        <div class="ctr bwt"><div id="cal-bb{i}" class="cbar bwb" data-pct="{round(b/mx,4)}"></div></div><div class="cnum"><span id="cal-nb{i}" data-v="{b}">0</span></div>
        <div class="ctr skt"><div id="cal-sb{i}" class="cbar skb" data-pct="{round(s/mx,4)}"></div></div><div class="cnum sk"><span id="cal-ns{i}" data-v="{s}">0</span></div></div>''' for i,(w,b,s) in enumerate(data,1))
W['cal']=scene('cal',CMPCSS+f'''
    #cal-p {{ top:392px; height:740px; padding:20px 40px 0; }}
    .chead {{ display:flex; height:44px; align-items:center; font-size:24px; letter-spacing:2px; color:#9a9a9a; }}
    .crow {{ display:flex; align-items:center; height:104px; border-top:1px solid rgba(255,255,255,.06); }}
    .ckg {{ width:160px; font-family:"Anton",sans-serif; font-size:50px; line-height:1; color:#fff; }}
    .ctr {{ height:24px; border-radius:12px; background:rgba(255,255,255,.12); overflow:hidden; }}
    .bwt {{ width:170px; }} .skt {{ width:250px; margin-left:14px; }}
    .cbar {{ width:100%; height:100%; border-radius:12px; transform-origin:0 50%; }}
    .bwb {{ background:#9aa3a8; }} .skb {{ background:linear-gradient(90deg,{YEL},{LIME}); }}
    .cnum {{ width:96px; text-align:right; font-family:"Anton",sans-serif; font-size:{SUB}px; color:#fff; line-height:1; padding-right:6px; }}
    .cnum.sk {{ color:{LIME}; width:110px; }}
    #cal-note {{ font-size:{CHIP}px; font-weight:600; color:#bbb; text-transform:none; letter-spacing:0; margin-top:12px; text-align:center; }}''',
f'''    <div class="topshade" id="cal-shade"></div>
{tag("cal","2","KALORI DALAM 10 MINIT")}
    <div id="cal-p" class="panel">
      <div class="chead lbl"><span style="width:160px">BERAT</span><span style="width:266px">BRISKWALK</span><span class="sk" style="width:374px; text-align:center">SKIPPING</span></div>{rows}
      <div id="cal-note" class="lbl">*Anggaran. MET briskwalk {MET_BW}, skipping {MET_SK} (Compendium of Physical Activities)</div>
    </div>
    <div id="cal-st" class="sticker" style="top:1150px; opacity:0">SKIPPING ±{ratio}X LEBIH BANYAK!</div>''',
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
W['otot']=scene('otot',CMPCSS+'''
    #otot-p { top:392px; height:700px; display:flex; justify-content:space-between; padding:26px 34px 0; }
    .ocol { width:440px; display:flex; flex-direction:column; align-items:center; gap:12px; }
    .bodysvg { width:190px; height:388px; }
    .ochips { display:flex; flex-wrap:wrap; justify-content:center; gap:8px; }''',
f'''    <div class="topshade" id="otot-shade"></div>
{tag("otot","3","OTOT YANG DILATIH")}
    <div id="otot-p" class="panel">
      <div class="ocol"><div class="colhead sk">SKIPPING</div>{body("osk",SK_PARTS,LIME)}
        <div class="ochips">{mchips("otot-a",["BAHU & LENGAN","PERUT / CORE","PEHA","BETIS"],"l")}</div></div>
      <div class="ocol"><div class="colhead bw">BRISKWALK</div>{body("obw",BW_PARTS,YEL)}
        <div class="ochips">{mchips("otot-b",["PEHA","BETIS"],"y")}</div></div>
    </div>
    <div id="otot-st" class="sticker" style="top:1150px; opacity:0">SKIPPING = TOTAL BODY WORKOUT!</div>''',
f'''{tagin("otot")}
    tl.fromTo("#otot-p", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "expo.out" }}, 0.2);
'''+"\n".join(f'    tl.fromTo("#obw-{p}", {{ fill: "#3a3a3a" }}, {{ fill: "{YEL}", duration: 0.25 }}, {round(0.8+i*0.3,2)});' for i,p in enumerate(BW_PARTS))
+"\n"+"\n".join(pop(f"#otot-b{i}",round(0.9+(i-1)*0.3,2)) for i in range(1,3))
+"\n"+"\n".join(f'    tl.fromTo("#osk-{p}", {{ fill: "#3a3a3a" }}, {{ fill: "{LIME}", duration: 0.25 }}, {round(1.8+i*0.3,2)});' for i,p in enumerate(SK_PARTS))
+"\n"+"\n".join(pop(f"#otot-a{i}",round(1.9+(i-1)*0.35,2)) for i in range(1,5))
+f'''
    tl.fromTo("#otot-st", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.8)" }}, 3.6);
'''+out('["#otot-tag","#otot-p","#otot-st","#otot-shade"]',5.78))
# ---------- DUAL MODE (25.5-31.5) ----------
W['dual']=scene('dual',CHIPCSS,
f'''    <div id="dual-shade" style="position:absolute; left:0; top:560px; width:1080px; height:420px; background: radial-gradient(ellipse at center, rgba(0,0,0,.42), rgba(0,0,0,0) 70%);"></div>
    <div id="dual-t1" class="hl line" style="top:640px">DUAL <span class="g">MODE</span></div>
    <div id="dual-m1" class="sub line" style="top:752px">MODE 1: <span class="y">BOLA PEMBERAT</span></div>
    <div class="chiprow" style="top:824px"><div id="dual-c1" class="pill lbl yb" style="opacity:0">{CHK}SESUAI UNTUK PEMULA</div></div>
    <div id="dual-m2" class="sub line" style="top:752px; opacity:0">MODE 2: <span class="y">TALI PANJANG</span></div>''',
f'''    tl.fromTo("#dual-shade", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, 0);
    tl.fromTo("#dual-t1", {IN_SLAM}, 0.05);
    tl.fromTo("#dual-m1", {{ opacity: 0, y: 16, filter: "blur(8px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.25, ease: "power4.out" }}, 0.3);
'''+pop("#dual-c1",0.65)+"\n"+out('["#dual-m1","#dual-c1"]',2.75)+f'''
    tl.fromTo("#dual-m2", {{ opacity: 0, y: 16, filter: "blur(8px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.25, ease: "power4.out" }}, 3.05);
'''+out('["#dual-t1","#dual-m2","#dual-shade"]',5.78))
# ---------- COUNTER (31.5-34.5) ----------
ccb,nc_=chiprows("ctr",[["KIRAAN","KALORI"],["JARAK","MASA"]],584,step=92)
W['counter']=scene('counter',CHIPCSS,
f'''    <div class="topshade" id="ctr-shade"></div>
    <div id="ctr-t0" class="lbl line" style="top:318px; text-align:center; font-size:28px; color:#C8FF1E; letter-spacing:3px">ADA SEKALI</div>
    <div id="ctr-t1" class="hl line" style="top:356px">DIGITAL</div>
    <div id="ctr-t2" class="hl line g" style="top:460px">COUNTER</div>
{ccb}''',
f'''    tl.fromTo("#ctr-t0", {IN_BLUR}, 0.05);
    tl.fromTo("#ctr-t1", {{ opacity: 0, scale: 1.3, x: -24 }}, {{ opacity: 1, scale: 1, x: 0, duration: 0.3, ease: "expo.out" }}, 0.1);
    tl.fromTo("#ctr-t2", {{ opacity: 0, scale: 1.3, x: 24 }}, {{ opacity: 1, scale: 1, x: 0, duration: 0.3, ease: "expo.out" }}, 0.22);
'''+"\n".join(pop(f"#ctr-p{i}",round(0.6+(i-1)*0.3,2)) for i in range(1,nc_+1))+"\n"+out('["#ctr-t0","#ctr-t1","#ctr-t2","#ctr-shade",".pill"]',2.78))
# ---------- RUMAH (34.5-38) ----------
W['rumah']=scene('rumah','''
    #rum-shade { position:absolute; left:0; top:580px; width:1080px; height:400px; background: radial-gradient(ellipse at center, rgba(0,0,0,.42), rgba(0,0,0,0) 70%); }''',
'''    <div id="rum-shade"></div>
    <div id="rum-t0" class="sub line" style="top:660px">BOLEH BERLATIH</div>
    <div id="rum-t1" class="hl line y" style="top:716px">DI RUMAH</div>''',
f'''    tl.fromTo("#rum-shade", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, 0);
    tl.fromTo("#rum-t0", {IN_BLUR}, 0.05);
    tl.fromTo("#rum-t1", {IN_SLAM}, 0.12);
'''+out('["#rum-t0","#rum-t1","#rum-shade"]',3.28))
# ---------- CTA (38-43.5) ----------
W['cta']=scene('cta','''
    #cta-shade { position:absolute; inset:0; background: rgba(0,0,0,.34); }
    #cta-cal { position:absolute; left:0; right:0; margin:0 auto; top:560px; width:260px; height:250px; border-radius:24px; background:#fff; overflow:hidden; box-shadow:0 10px 30px rgba(0,0,0,.5); }
    #cta-cal .hd { height:64px; background:#E8252B; color:#fff; font-family:"MontserratV",sans-serif; font-weight:800; font-size:28px; letter-spacing:3px; display:flex; align-items:center; justify-content:center; }
    #cta-cal .yr { font-family:"Anton",sans-serif; font-size:110px; line-height:186px; text-align:center; color:#111; }
    .ring { position:absolute; top:-14px; width:14px; height:34px; border-radius:7px; background:#222; }
    #cta-st { position:absolute; left:0; right:0; margin:0 auto; width:max-content; top:888px; padding:4px 26px 8px; background:#C8FF1E; color:#000; font-family:"Anton",sans-serif; font-size:47px; line-height:1.15; transform:rotate(-2deg); box-shadow:0 6px 18px rgba(0,0,0,.45); }
    #cta-btn { position:absolute; left:0; right:0; margin:0 auto; top:990px; width:max-content; padding: 8px 40px 12px; border-radius:60px;
               background:#fff; font-family:"Anton",sans-serif; font-size:64px; line-height:1.1; color:#000; box-shadow: 0 8px 24px rgba(0,0,0,.5); }''',
'''    <div id="cta-shade"></div>
    <div id="cta-cal"><div class="ring" style="left:70px"></div><div class="ring" style="right:70px"></div><div class="hd">JANUARI</div><div class="yr">2027</div></div>
    <div id="cta-a" class="sub line" style="top:826px">TAHUN 2027</div>
    <div id="cta-st">NAK START BERSENAM?</div>
    <div id="cta-btn">START SKIPPING SEKARANG!</div>''',
f'''    tl.fromTo("#cta-shade", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, ease: "power2.inOut" }}, 0);
    tl.fromTo("#cta-cal", {{ opacity: 0, y: -60, rotation: -8 }}, {{ opacity: 1, y: 0, rotation: 0, duration: 0.5, ease: "back.out(1.6)" }}, 0.05);
    tl.fromTo("#cta-a", {IN_BLUR}, 0.5);
    tl.fromTo("#cta-st", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.8)" }}, 0.8);
    tl.fromTo("#cta-btn", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.8)" }}, 2.3);''')
# ---------- CAPTIONS ----------
groups=[(26.4,28.1,"TAK TERSANGKUT KAKI",["TERSANGKUT"]),(29.1,31.3,"NAK LEBIH CABARAN?",["CABARAN?"]),
(35.4,36.5,"TAK PERLU GYM,",["GYM,"]),(36.5,37.8,"JIMAT MASA",["JIMAT"])]
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
    .cg {{ position:absolute; left:0; top:1140px; width:1080px; height:70px; overflow: visible; }}
    .ci {{ width:1080px; text-align:center; font-family:"Anton",sans-serif; font-size:{CAP}px; line-height:70px; color:#fff; text-transform:uppercase;
          -webkit-text-stroke: 6px #000; paint-order: stroke fill; text-shadow: 0 4px 10px rgba(0,0,0,.6); letter-spacing: 1px; }}
    .w {{ display:inline-block; color:#fff; margin: 0 4px; }}
    .w.kw {{ color:#39FF14; }}''', "\n".join(html), "\n".join(js))
for k,v in W.items(): open(f'{P}/compositions/{k}.html','w').write(v)
# ---------- INDEX ----------
L={'g1_hook':-45.3,'g2_gerak':-27.9,'g3_cal':-34.8,'g4_cal':-19.6,'g5_otot':-25.3,'g6_bola':-40.9,'g7_tali':-24.0,'g8_counter':-57.6,'g9_rumah':-34.1,'g10_cta':-37.4}
clips=[("g1_hook",0,4.0),("g2_gerak",4,5.5),("g3_cal",9.5,5.0),("g4_cal",14.5,5.0),("g5_otot",19.5,6.0),("g6_bola",25.5,3.0),("g7_tali",28.5,3.0),("g8_counter",31.5,3.0),("g9_rumah",34.5,3.5),("g10_cta",38,5.5)]
DUR=43.5
cuts=[s for _,s,_ in clips[1:]]
sfx_len={"whoosh":0.55,"pop":0.12,"ding":1.4,"impact":0.9,"chaching":1.2,"riser":1.3,"zap":0.3}
sfx=[("impact",0.0),("zap",0.1),("pop",0.6),("riser",2.6)]+[("whoosh",round(c-0.3,2)) for c in cuts if c not in (14.5,)]
sfx+=[("impact",4.05),("zap",4.6)]+[("pop",round(5.0+(i//2)*0.6+(i%2)*0.3,2)) for i in range(6)]
sfx+=[("impact",9.55),("pop",10.2),("pop",11.9),("chaching",13.0),("ding",14.55)]
sfx+=[("impact",19.55),("pop",20.3),("pop",20.6),("pop",21.4),("pop",21.75),("pop",22.1),("pop",22.45),("ding",23.1)]
sfx+=[("impact",25.55),("pop",26.15),("zap",28.55),("pop",32.1),("pop",32.4),("pop",32.7),("pop",33.0)]
sfx+=[("impact",34.6),("riser",36.7),("impact",38.05),("pop",38.8),("ding",40.3),("chaching",41.0)]
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
scenes=[("hook",0,4),("gerak",4,5.5),("cal",9.5,10),("otot",19.5,6),("dual",25.5,6),("counter",31.5,3.0),("rumah",34.5,3.5),("cta",38,5.5)]
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
