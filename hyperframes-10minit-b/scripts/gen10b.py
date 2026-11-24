import os, math
P='/home/user/hf/skipping10b'
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
    .pill {{ position:absolute; height:52px; padding: 0 18px; border-radius:26px; background: rgba(10,10,10,.72); border:2px solid #39FF14;
            display:flex; align-items:center; gap:9px; font-size:{CHIP}px; color:#fff; white-space:nowrap; }}
    .pill i {{ width:11px; height:11px; border-radius:50%; background:#39FF14; box-shadow: 0 0 10px #39FF14; display:block; }}
    .pill.yb {{ border-color:#FFE600; }} .pill.yb i {{ background:#FFE600; box-shadow:0 0 10px #FFE600; }}
    .L {{ left:150px; }} .R {{ right:210px; }}
    .C {{ left:0; right:0; margin:0 auto; width:max-content; }}'''
def pop(sel,t): return f'    tl.fromTo("{sel}", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(1.7)" }}, {t});'
# ---------- CALORIES = HOOK (0-10) ----------
data=[(w, int(11.8*3.5*w/200*10+0.5)) for w in (50,60,70,80,90,100)]
mx=max(k for _,k in data)
rows="".join(f'\n      <div id="cal-r{i}" class="row"><div class="lbl kg">{w} KG</div><div class="track"><div id="cal-b{i}" class="bar" data-pct="{round(k/mx,4)}"></div></div><div class="val"><span id="cal-n{i}" data-v="{k}">{k}</span><small class="lbl">kcal</small></div></div>' for i,(w,k) in enumerate(data,1))
W['cal']=scene('cal',f'''
    #cal-card {{ position:absolute; left:40px; top:310px; width:1000px; height:760px; border-radius:34px; background: rgba(10,10,10,.76); border: 6px solid #000; padding: 16px 40px 0; }}
    #cal-head {{ font-family:"Anton",sans-serif; font-size:{SUB}px; line-height:62px; height:62px; color:#fff; text-align:center; text-transform:uppercase; letter-spacing:1px; }}
    .row {{ display:flex; align-items:center; height:104px; }}
    .kg {{ width:230px; font-size:50px; color:#fff; white-space:nowrap; }}
    .track {{ flex:1; height:40px; border-radius:20px; background: rgba(255,255,255,.14); overflow:hidden; margin-right:24px; }}
    .bar {{ width:100%; height:100%; border-radius:20px; background: linear-gradient(90deg,#FFE600,#39FF14); transform-origin: 0 50%; }}
    .val {{ width:210px; text-align:right; font-family:"Anton",sans-serif; font-size:64px; color:#fff; line-height:1; white-space:nowrap; }}
    .val small {{ font-size:30px; margin-left:6px; color:#ddd; }}
    #cal-note {{ font-size:{CHIP}px; font-weight:600; color:#bbb; text-transform:none; letter-spacing:0; margin-top:4px; text-align:center; }}''',
f'''    <div class="topshade" id="cal-shade"></div>
    <div id="cal-t1" class="hl line" style="top:196px"><span class="y">10 MINIT</span> SKIPPING</div>
    <div id="cal-card">
      <div id="cal-head"><span class="g">KALORI</span> TERBAKAR</div>{rows}
      <div id="cal-note" class="lbl">*Anggaran, kadar sederhana</div>
    </div>''',
f'''    // frame 0 sudah ada tajuk + kad (hook); bar dan nombor naik serentak supaya susunan sentiasa betul
    tl.fromTo("#cal-t1", {{ scale: 1.12, opacity: 1 }}, {{ scale: 1, duration: 0.32, ease: "expo.out" }}, 0);
    tl.fromTo("#cal-card", {{ opacity: 1, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "expo.out" }}, 0);
    for (let i = 1; i <= 6; i++) {{
      const bar = document.querySelector("#cal-b" + i), num = document.querySelector("#cal-n" + i);
      const pct = parseFloat(bar.dataset.pct), v = parseInt(num.dataset.v, 10);
      tl.fromTo(bar, {{ scaleX: pct * 0.6 }}, {{ scaleX: pct, duration: 1.6, ease: "power2.out" }}, 0);
      const o = {{ n: 0 }};
      tl.fromTo(o, {{ n: v * 0.6 }}, {{ n: v, duration: 1.6, ease: "power2.out", onUpdate: () => {{ num.textContent = Math.round(o.n); }} }}, 0);
    }}
    tl.fromTo("#cal-r6", {{ scale: 1 }}, {{ scale: 1.04, duration: 0.3, ease: "back.out(1.6)" }}, 7.6);
    tl.fromTo("#cal-n6", {{ color: "#ffffff" }}, {{ color: "#39FF14", duration: 0.2 }}, 7.6);
'''+out('["#cal-t1","#cal-card","#cal-shade"]',9.78))
# ---------- OTOT (10-16) ----------
pills=[("BAHU","L",700),("PUNGGUNG","R",700),("LENGAN","L",776),("PAHA","R",776),("PERUT / CORE","L",852),("BETIS","R",852)]
pb="\n".join(f'    <div id="otot-p{i}" class="pill lbl {s}" style="top:{y}px"><i></i>{n}</div>' for i,(n,s,y) in enumerate(pills,1))
W['otot']=scene('otot',CHIPCSS,
f'''    <div class="topshade" id="otot-shade"></div>
    <div id="otot-t1" class="hl line y" style="top:500px">OTOT</div>
    <div id="otot-t2" class="sub line" style="top:610px">YANG DILATIH</div>
{pb}''',
f'''    tl.fromTo("#otot-t1", {IN_SLAM}, 0.05);
    tl.fromTo("#otot-t2", {IN_BLUR}, 0.3);
'''+"\n".join(pop(f"#otot-p{i}",round(0.5+(i-1)*0.3,2)) for i in range(1,7))+"\n"+out('["#otot-t1","#otot-t2","#otot-shade",".pill"]',5.78))
# ---------- TOTAL BODY (16-21) ----------
tb=[("KARDIO","L",700),("KEKUATAN","R",700),("KOORDINASI","L",776),("STAMINA","R",776)]
tbb="\n".join(f'    <div id="tot-p{i}" class="pill lbl {s}" style="top:{y}px"><i></i>{n}</div>' for i,(n,s,y) in enumerate(tb,1))
W['total']=scene('total',CHIPCSS,
f'''    <div class="topshade" id="tot-shade"></div>
    <div id="tot-t1" class="hl line" style="top:500px">TOTAL <span class="g">BODY</span></div>
    <div id="tot-t2" class="sub line" style="top:610px">WORKOUT</div>
{tbb}
    <div id="tot-p5" class="pill lbl yb C" style="top:852px"><i></i>ATAS + TENGAH + BAWAH BADAN</div>''',
f'''    tl.fromTo("#tot-t1", {{ opacity: 0, scale: 1.3, x: -24 }}, {{ opacity: 1, scale: 1, x: 0, duration: 0.3, ease: "expo.out" }}, 0.05);
    tl.fromTo("#tot-t2", {IN_BLUR}, 0.3);
'''+"\n".join(pop(f"#tot-p{i}",round(0.7+(i-1)*0.35,2)) for i in range(1,6))+"\n"+out('["#tot-t1","#tot-t2","#tot-shade",".pill"]',4.78))
# ---------- DUAL MODE (21-30) ----------
W['dual']=scene('dual',CHIPCSS,
'''    <div class="topshade" id="dual-shade"></div>
    <div id="dual-t1" class="hl line" style="top:330px">DUAL <span class="g">MODE</span></div>
    <div id="dual-s0" class="sub line" style="top:444px">BOLA PEMBERAT <span class="y">+</span> TALI PANJANG</div>
    <div id="dual-m1" class="sub line" style="top:444px; opacity:0">MODE 1: <span class="y">BOLA PEMBERAT</span></div>
    <div id="dual-c1" class="pill lbl yb C" style="top:512px; opacity:0"><i></i>SESUAI UNTUK PEMULA</div>
    <div id="dual-m2" class="sub line" style="top:444px; opacity:0">MODE 2: <span class="y">TALI PANJANG</span></div>''',
f'''    tl.fromTo("#dual-t1", {IN_SLAM}, 0.05);
    tl.fromTo("#dual-s0", {IN_BLUR}, 0.4);
'''+out('["#dual-s0"]',2.8)+f'''
    tl.fromTo("#dual-m1", {{ opacity: 0, y: 16, filter: "blur(8px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.25, ease: "power4.out" }}, 3.1);
'''+pop("#dual-c1",3.5)+"\n"+out('["#dual-m1","#dual-c1"]',5.8)+f'''
    tl.fromTo("#dual-m2", {{ opacity: 0, y: 16, filter: "blur(8px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.25, ease: "power4.out" }}, 6.1);
'''+out('["#dual-t1","#dual-m2","#dual-shade"]',8.78))
# ---------- COUNTER (30-33.5) ----------
cc=[("KIRAAN","L",600),("KALORI","R",600),("JARAK","L",676),("MASA","R",676)]
ccb="\n".join(f'    <div id="ctr-p{i}" class="pill lbl {s}" style="top:{y}px"><i></i>{n}</div>' for i,(n,s,y) in enumerate(cc,1))
W['counter']=scene('counter',CHIPCSS,
f'''    <div class="topshade" id="ctr-shade"></div>
    <div id="ctr-t0" class="sub line" style="top:330px">TALI SKIPPING NI ADA</div>
    <div id="ctr-t1" class="hl line g" style="top:388px">DIGITAL</div>
    <div id="ctr-t2" class="hl line" style="top:492px">COUNTER</div>
{ccb}''',
f'''    tl.fromTo("#ctr-t0", {IN_BLUR}, 0.05);
    tl.fromTo("#ctr-t1", {{ opacity: 0, scale: 1.3, x: -24 }}, {{ opacity: 1, scale: 1, x: 0, duration: 0.3, ease: "expo.out" }}, 0.1);
    tl.fromTo("#ctr-t2", {{ opacity: 0, scale: 1.3, x: 24 }}, {{ opacity: 1, scale: 1, x: 0, duration: 0.3, ease: "expo.out" }}, 0.22);
'''+"\n".join(pop(f"#ctr-p{i}",round(0.8+(i-1)*0.4,2)) for i in range(1,5))+"\n"+out('["#ctr-t0","#ctr-t1","#ctr-t2","#ctr-shade",".pill"]',3.28))
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
groups=[(6.0,7.5,"LEBIH BERAT,",["BERAT,"]),(7.5,9.6,"LEBIH BANYAK KALORI",["KALORI"]),
(13.4,14.5,"SEMUA KERJA",[]),(14.5,15.7,"SERENTAK!",["SERENTAK!"]),
(18.5,19.6,"SATU SENAMAN,",[]),(19.6,20.8,"SELURUH BADAN",["SELURUH"]),
(22.3,23.8,"DUA CARA, SATU TALI",["DUA"]),
(24.8,26.6,"TAK TERSANGKUT KAKI",["TERSANGKUT"]),(27.6,29.6,"NAK LEBIH CABARAN?",["CABARAN?"])]
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
L={'e1_cal':-37.0,'e2_cal':-33.8,'e3_otot':-41.0,'e4_otot':-34.9,'e5_total':-48.2,'e6_dual':-65.7,'e7_bola':-49.3,'e8_tali':-47.3,'e9_counter':-65.4,'e10_cta':-53.7}
clips=[("e1_cal",0,5.0),("e2_cal",5,5.0),("e3_otot",10,3.0),("e4_otot",13,3.0),("e5_total",16,5.0),("e6_dual",21,3.0),("e7_bola",24,3.0),("e8_tali",27,3.0),("e9_counter",30,3.5),("e10_cta",33.5,5.5)]
DUR=39.0
cuts=[s for _,s,_ in clips[1:]]
sfx_len={"whoosh":0.55,"pop":0.12,"ding":1.4,"impact":0.9,"chaching":1.2,"riser":1.3,"zap":0.3}
sfx=[("impact",0.0),("riser",0.3),("chaching",2.5),("ding",7.6)]+[("whoosh",round(c-0.3,2)) for c in cuts]
sfx+=[("impact",10.05)]+[("pop",round(10.5+0.3*i,2)) for i in range(6)]
sfx+=[("impact",16.05)]+[("pop",round(16.7+0.35*i,2)) for i in range(5)]
sfx+=[("impact",21.05),("pop",21.4),("ding",24.5),("pop",24.6),("zap",27.1),("pop",30.1)]+[("pop",round(30.8+0.4*i,2)) for i in range(4)]
sfx+=[("riser",32.2),("impact",33.5),("pop",34.0),("ding",35.3),("chaching",36.0)]
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
scenes=[("cal",0,10),("otot",10,6),("total",16,5),("dual",21,9),("counter",30,3.5),("cta",33.5,5.5)]
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
