import os, math
P='/home/user/hf/skipping15'
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
# ---------- HOOK (0-4) ----------
W['hook']=scene('hook','''
    #hook-shade { position:absolute; left:0; top:560px; width:1080px; height:420px; background: radial-gradient(ellipse at center, rgba(0,0,0,.42), rgba(0,0,0,0) 70%); }''',
'''    <div id="hook-shade"></div>
    <div id="hook-t1" class="hl line y" style="top:640px">15 MINIT</div>
    <div id="hook-t2" class="hl line" style="top:744px">SKIPPING</div>
    <div id="hook-sub" class="sub line" style="top:858px">SETIAP HARI?</div>''',
'''    tl.fromTo("#hook-t1", { scale: 1.14, y: -12, opacity: 1 }, { scale: 1, y: 0, duration: 0.32, ease: "expo.out" }, 0);
    tl.fromTo("#hook-t2", { scale: 1.14, y: 12, opacity: 1 }, { scale: 1, y: 0, duration: 0.32, ease: "expo.out" }, 0.04);
    tl.fromTo("#hook-sub", { opacity: 0, y: 20, filter: "blur(8px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.3, ease: "power4.out" }, 0.55);
'''+out('["#hook-t1","#hook-t2","#hook-sub","#hook-shade"]',3.78))
# ---------- CALORIES (4-14, 10 s) ----------
data=[(w, round(11.8*3.5*w/200*15)) for w in (50,60,70,80,90,100)]
mx=max(k for _,k in data)
rows="".join(f'\n      <div id="cal-r{i}" class="row"><div class="lbl kg">{w} KG</div><div class="track"><div id="cal-b{i}" class="bar" data-pct="{round(k/mx,4)}"></div></div><div class="val"><span id="cal-n{i}" data-v="{k}">0</span><small class="lbl">kcal</small></div></div>' for i,(w,k) in enumerate(data,1))
W['cal']=scene('cal',f'''
    #cal-card {{ position:absolute; left:240px; top:525px; width:540px; height:392px; border-radius:26px; background: rgba(10,10,10,.72); border: 2px solid rgba(57,255,20,.65); padding: 20px 24px 0; }}
    .row {{ display:flex; align-items:center; height:52px; }}
    .kg {{ width:84px; font-size:{CHIP}px; color:#fff; }}
    .track {{ flex:1; height:22px; border-radius:11px; background: rgba(255,255,255,.14); overflow:hidden; margin-right:14px; }}
    .bar {{ width:100%; height:100%; border-radius:11px; background: linear-gradient(90deg,#FFE600,#39FF14); transform-origin: 0 50%; }}
    .val {{ width:128px; text-align:right; font-family:"Anton",sans-serif; font-size:{SUB}px; color:#fff; line-height:1; }}
    .val small {{ font-size:{CHIP}px; margin-left:5px; color:#ddd; }}
    #cal-note {{ font-size:{CHIP}px; font-weight:600; color:#bbb; text-transform:none; letter-spacing:0; margin-top:8px; text-align:center; }}''',
f'''    <div class="topshade" id="cal-shade"></div>
    <div id="cal-t1" class="hl line g" style="top:330px">KALORI</div>
    <div id="cal-t2" class="sub line" style="top:440px">TERBAKAR DALAM <span class="y">15 MINIT</span></div>
    <div id="cal-card">{rows}
      <div id="cal-note" class="lbl">*Anggaran, kadar sederhana</div>
    </div>''',
f'''    tl.fromTo("#cal-t1", {IN_SLAM}, 0.05);
    tl.fromTo("#cal-t2", {IN_BLUR}, 0.35);
    tl.fromTo("#cal-card", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }}, 0.7);
    for (let i = 1; i <= 6; i++) {{
      const t0 = 1.2 + (i - 1) * 0.3;
      const bar = document.querySelector("#cal-b" + i), num = document.querySelector("#cal-n" + i);
      const pct = parseFloat(bar.dataset.pct), v = parseInt(num.dataset.v, 10);
      tl.fromTo("#cal-r" + i, {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "power4.out" }}, t0);
      tl.fromTo(bar, {{ scaleX: 0 }}, {{ scaleX: pct, duration: 1.2, ease: "power2.out" }}, t0 + 0.1);
      const o = {{ n: 0 }};
      tl.fromTo(o, {{ n: 0 }}, {{ n: v, duration: 1.2, ease: "power2.out", onUpdate: () => {{ num.textContent = Math.round(o.n); }} }}, t0 + 0.1);
    }}
    tl.fromTo("#cal-r6", {{ scale: 1 }}, {{ scale: 1.06, duration: 0.3, ease: "back.out(1.6)" }}, 6.6);
    tl.fromTo("#cal-n6", {{ color: "#ffffff" }}, {{ color: "#39FF14", duration: 0.2 }}, 6.6);
'''+out('["#cal-t1","#cal-t2","#cal-card","#cal-shade"]',9.75))
# ---------- OTOT (14-20, 6 s) ----------
pills=[("BAHU","L",560),("PUNGGUNG","R",560),("LENGAN","L",636),("PAHA","R",636),("PERUT / CORE","L",712),("BETIS","R",712)]
pb="\n".join(f'    <div id="otot-p{i}" class="pill lbl {s}" style="top:{y}px"><i></i>{n}</div>' for i,(n,s,y) in enumerate(pills,1))
W['otot']=scene('otot',f'''
    .pill {{ position:absolute; height:52px; padding: 0 18px; border-radius:26px; background: rgba(10,10,10,.72); border:2px solid #39FF14;
            display:flex; align-items:center; gap:9px; font-size:{CHIP}px; color:#fff; white-space:nowrap; }}
    .pill i {{ width:11px; height:11px; border-radius:50%; background:#39FF14; box-shadow: 0 0 10px #39FF14; display:block; }}
    .L {{ left:150px; }} .R {{ right:210px; }}
    #otot-p7 {{ left:0; right:0; margin:0 auto; width:max-content; border-color:#FFE600; }}
    #otot-p7 i {{ background:#FFE600; box-shadow: 0 0 10px #FFE600; }}''',
f'''    <div class="topshade" id="otot-shade"></div>
    <div id="otot-t1" class="hl line y" style="top:330px">OTOT</div>
    <div id="otot-t2" class="sub line" style="top:440px">YANG DILATIH</div>
{pb}
    <div id="otot-p7" class="pill lbl" style="top:788px"><i></i>+ JANTUNG &amp; PARU-PARU</div>''',
f'''    tl.fromTo("#otot-t1", {IN_SLAM}, 0.05);
    tl.fromTo("#otot-t2", {IN_BLUR}, 0.3);
    for (let i = 1; i <= 6; i++) {{
      tl.fromTo("#otot-p" + i, {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(1.7)" }}, 0.5 + (i - 1) * 0.3);
    }}
    tl.fromTo("#otot-p7", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(1.7)" }}, 2.6);
'''+out('["#otot-t1","#otot-t2","#otot-shade",".pill"]',5.78))
# ---------- USP (20-27.5) ----------
W['usp']=scene('usp','',
'''    <div class="topshade" id="usp-shade"></div>
    <div id="usp-a0" class="sub line" style="top:330px">TALI SKIPPING NI ADA</div>
    <div id="usp-a1" class="hl line g" style="top:388px">DIGITAL</div>
    <div id="usp-a2" class="hl line" style="top:492px">COUNTER</div>
    <div id="usp-a3" class="sub line" style="top:606px; opacity:0">KIRA <span class="g">LOMPATAN</span>, KALORI &amp; JARAK</div>
    <div id="usp-bshade" style="position:absolute; left:0; top:500px; width:1080px; height:420px; opacity:0; background: radial-gradient(ellipse at center, rgba(0,0,0,.4), rgba(0,0,0,0) 70%);"></div>
    <div id="usp-b0" class="sub line" style="top:560px; opacity:0">BOLEH SKIPPING</div>
    <div id="usp-b1" class="hl line y" style="top:616px; opacity:0">DALAM</div>
    <div id="usp-b2" class="hl line" style="top:720px; opacity:0">RUMAH JE</div>''',
f'''    tl.fromTo("#usp-a0", {IN_BLUR}, 0.05);
    tl.fromTo("#usp-a1", {{ opacity: 0, scale: 1.3, x: -24 }}, {{ opacity: 1, scale: 1, x: 0, duration: 0.3, ease: "expo.out" }}, 0.1);
    tl.fromTo("#usp-a2", {{ opacity: 0, scale: 1.3, x: 24 }}, {{ opacity: 1, scale: 1, x: 0, duration: 0.3, ease: "expo.out" }}, 0.22);
    tl.fromTo("#usp-a3", {{ opacity: 0, y: 16, filter: "blur(8px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.25, ease: "power4.out" }}, 1.2);
'''+out('["#usp-a0","#usp-a1","#usp-a2","#usp-a3","#usp-shade"]',3.28)+f'''
    tl.fromTo("#usp-bshade", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, 9.5);
    tl.fromTo("#usp-b0", {IN_BLUR}, 9.55);
    tl.fromTo("#usp-b1", {{ opacity: 0, scale: 1.3 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "expo.out" }}, 9.6);
    tl.fromTo("#usp-b2", {{ opacity: 0, scale: 1.3 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "expo.out" }}, 9.72);
'''+out('["#usp-b0","#usp-b1","#usp-b2","#usp-bshade"]',13.28))
# ---------- DUAL MODE (23.5-29.5) ----------
W['dual']=scene('dual',f'''
    .chip {{ position:absolute; left:0; right:0; margin:0 auto; width:max-content; height:46px; padding:0 18px; border-radius:23px; background: rgba(10,10,10,.75);
            border:2px solid #FFE600; display:flex; align-items:center; gap:9px; font-size:{CHIP}px; color:#fff; white-space:nowrap; }}
    .chip i {{ width:11px; height:11px; border-radius:50%; background:#FFE600; box-shadow:0 0 10px #FFE600; display:block; }}''',
'''    <div class="topshade" id="dual-shade"></div>
    <div id="dual-t1" class="hl line" style="top:330px">DUAL <span class="g">MODE</span></div>
    <div id="dual-m1" class="sub line" style="top:444px">MODE 1: <span class="y">BOLA PEMBERAT</span></div>
    <div id="dual-c1" class="chip lbl" style="top:512px"><i></i>SESUAI UNTUK PEMULA</div>
    <div id="dual-m2" class="sub line" style="top:444px; opacity:0">MODE 2: <span class="y">TALI PANJANG</span></div>''',
f'''    tl.fromTo("#dual-shade", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, 0);
    tl.fromTo("#dual-t1", {IN_SLAM}, 0.05);
    tl.fromTo("#dual-m1", {{ opacity: 0, y: 16, filter: "blur(8px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.25, ease: "power4.out" }}, 0.4);
    tl.fromTo("#dual-c1", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(1.7)" }}, 0.9);
'''+out('["#dual-m1","#dual-c1"]',2.8)+f'''
    tl.fromTo("#dual-m2", {{ opacity: 0, y: 16, filter: "blur(8px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.25, ease: "power4.out" }}, 3.1);
'''+out('["#dual-t1","#dual-m2","#dual-shade"]',5.78))
# ---------- CTA (27.5-33) ----------
W['cta']=scene('cta','''
    #cta-shade { position:absolute; inset:0; background: rgba(0,0,0,.36); }
    #cta-btn { position:absolute; left:0; right:0; margin:0 auto; top:812px; width:max-content; padding: 6px 40px 10px; border-radius:60px;
               background:#39FF14; font-family:"Anton",sans-serif; font-size:73px; line-height:1.1; color:#000; box-shadow: 0 0 30px rgba(57,255,20,.6), 0 8px 24px rgba(0,0,0,.5); }''',
'''    <div id="cta-shade"></div>
    <div id="cta-a" class="sub line" style="top:560px">NAK BADAN</div>
    <div id="cta-b" class="hl line" style="top:614px">FIT <span class="y">2027?</span></div>
    <div id="cta-c" class="sub line" style="top:738px">START SKIPPING</div>
    <div id="cta-btn">SEKARANG!</div>''',
f'''    tl.fromTo("#cta-shade", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, ease: "power2.inOut" }}, 0);
    tl.fromTo("#cta-a", {IN_BLUR}, 0.05);
    tl.fromTo("#cta-b", {{ opacity: 0, scale: 1.35 }}, {{ opacity: 1, scale: 1, duration: 0.32, ease: "expo.out" }}, 0.1);
    tl.fromTo("#cta-c", {{ opacity: 0, y: 20, filter: "blur(8px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.3, ease: "power4.out" }}, 1.8);
    tl.fromTo("#cta-btn", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.8)" }}, 2.5);''')
# ---------- CAPTIONS ----------
groups=[(1.5,2.6,"INI YANG JADI",[]),(2.6,3.85,"PADA BADAN KAU",["BADAN"]),
(10.6,12.2,"LEBIH BERAT,",["BERAT,"]),(12.2,13.85,"LEBIH BANYAK KALORI",["KALORI"]),
(17.6,18.7,"SEMUA KERJA",[]),(18.7,19.8,"SERENTAK!",["SERENTAK!"]),
(24.8,26.3,"TAK TERSANGKUT KAKI",["TERSANGKUT"]),(27.6,29.3,"NAK LEBIH CABARAN?",["CABARAN?"]),
(31.0,32.15,"TAK PERLU GYM,",["GYM,"]),(32.15,33.3,"JIMAT MASA",["JIMAT"])]
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
L={'d1_hook':-36.7,'d2_cal':-41.5,'d3_cal':-32.8,'d4_otot':-55.3,'d5_otot':-40.9,'d6_counter':-49.9,'d7_rumah':-32.5,'d8_cta':-33.3,'d9_bola':-47.5,'d10_tali':-35.7}
clips=[("d1_hook",0,4.0),("d2_cal",4,5.0),("d3_cal",9,5.0),("d4_otot",14,3.0),("d5_otot",17,3.0),("d6_counter",20,3.5),("d9_bola",23.5,3.0),("d10_tali",26.5,3.0),("d7_rumah",29.5,4.0),("d8_cta",33.5,5.5)]
DUR=39.0
cuts=[s for _,s,_ in clips[1:]]
sfx_len={"whoosh":0.55,"pop":0.12,"ding":1.4,"impact":0.9,"chaching":1.2,"riser":1.3,"zap":0.3}
sfx=[("impact",0.0),("pop",0.55),("riser",2.7)]+[("whoosh",round(c-0.3,2)) for c in cuts]
sfx+=[("impact",4.05)]+[("pop",round(5.2+0.3*i,2)) for i in range(6)]+[("chaching",8.05),("ding",10.6)]
sfx+=[("impact",14.05)]+[("pop",round(14.5+0.3*i,2)) for i in range(6)]+[("ding",16.6)]
sfx+=[("zap",20.1),("pop",21.2),("impact",23.55),("pop",23.9),("ding",24.4),("zap",26.55),("pop",26.6),("pop",29.6),("riser",32.2),("impact",33.5),("pop",34.0),("ding",35.3),("chaching",36.0)]
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
scenes=[("hook",0,4),("cal",4,10),("otot",14,6),("usp",20,13.5),("dual",23.5,6),("cta",33.5,5.5)]
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
