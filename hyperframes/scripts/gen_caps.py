groups=[(1.5,2.6,"INI YANG JADI",[]),(2.6,3.85,"PADA BADAN KAU",["BADAN"]),
(10.6,12.2,"LEBIH BERAT,",["BERAT,"]),(12.2,13.85,"LEBIH BANYAK KALORI",["KALORI"]),
(20.0,21.0,"SEMUA KERJA",[]),(21.0,21.9,"SERENTAK!",["SERENTAK!"]),
(23.6,25.35,"KIRA SETIAP LOMPATAN",["LOMPATAN"]),
(25.6,27.9,"SEMUA DIKIRA AUTOMATIK",["AUTOMATIK"]),
(29.55,30.5,"TAK PERLU GYM,",["GYM,"]),(30.5,31.4,"JIMAT MASA",["JIMAT"])]
css=open('/home/user/work/common.css').read()
html=[];js=[]
for gi,(s,e,txt,kw) in enumerate(groups,1):
    words=txt.split(); n=len(words)
    spans="".join(f'<span id="cap{gi}w{wi}" class="w{" kw" if w in kw else ""}">{w}</span> ' for wi,w in enumerate(words,1)).strip()
    html.append(f'    <div id="cap{gi}" class="clip cg" data-start="{s}" data-duration="{round(e-s,3)}" data-track-index="0"><div id="cap{gi}i" class="ci">{spans}</div></div>')
    js.append(f'    tl.fromTo("#cap{gi}i", {{ scale: 0.82, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.16, ease: "back.out(2)" }}, {s});')
    # active word timing: weighted by letters
    L=[len(w) for w in words]; tot=sum(L)+n*2; span=(e-s-0.12); t=s
    for wi,w in enumerate(words,1):
        d=span*(len(w)+2)/tot
        base="#39FF14" if w in kw else "#ffffff"
        act="#39FF14" if w in kw else "#FFE600"
        js.append(f'    tl.set("#cap{gi}w{wi}", {{ color: "{act}", scale: 1.12 }}, {round(t,3)});')
        if wi<n: js.append(f'    tl.set("#cap{gi}w{wi}", {{ color: "{base}", scale: 1 }}, {round(t+d,3)});')
        t+=d
    js.append(f'    tl.to("#cap{gi}i", {{ opacity: 0, duration: 0.1, ease: "power2.in" }}, {round(e-0.1,3)});')
out=f'''<template>
  <style>
{css}
    .cg {{ position:absolute; left:0; top:1110px; width:1080px; height:100px; overflow: visible; }}
    .ci {{ width:1080px; text-align:center; font-family:"Anton",sans-serif; font-size:60px; line-height:100px; color:#fff; text-transform:uppercase;
          -webkit-text-stroke: 9px #000; paint-order: stroke fill; text-shadow: 0 5px 14px rgba(0,0,0,.6); letter-spacing: 1px; }}
    .w {{ display:inline-block; color:#fff; margin: 0 6px; }}
    .w.kw {{ color:#39FF14; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
{chr(10).join(html)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
    window.__timelines["captions"] = tl;
  </script>
</template>
'''
open('/home/user/hf/skipping/compositions/captions.html','w').write(out)
