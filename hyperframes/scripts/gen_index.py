clips=[("c1_hook",0,4.0,0.0305),("c2_cal",4,5.0,0.032),("c3_cal",9,5.0,0.1549),("c4_otot",14,4.0,0.0684),
("c5_otot",18,4.0,0.2786),("c6_counter",22,3.5,1.4289),("c7_count",25.5,2.5,2.0654),("c8_rumah",28,3.5,0.4467),("c9_cta",31.5,5.5,0.0153)]
sfx_len={"whoosh":0.55,"pop":0.12,"ding":1.4,"impact":0.9,"chaching":1.2,"riser":1.3,"zap":0.3}
cuts=[4,9,14,18,22,25.5,28,31.5]
sfx=[("impact",0.0),("pop",0.55),("riser",2.7)]
sfx+=[("whoosh",round(c-0.3,2)) for c in cuts]
sfx+=[("impact",4.05),("pop",5.2),("pop",5.5),("pop",5.8),("pop",6.1),("pop",6.4),("pop",6.7),("chaching",8.05),("ding",10.6),
("impact",14.05),("pop",14.8),("pop",15.3),("pop",15.8),("pop",16.3),("pop",16.8),("pop",17.3),("ding",19.0),
("zap",22.1),("ding",25.6),("chaching",26.6),("pop",28.1),("zap",28.4),
("riser",30.2),("impact",31.5),("pop",32.0),("ding",33.3),("chaching",34.0)]
sfx.sort(key=lambda s:s[1])
# lanes: assign lowest lane with no overlap
lanes=[]; out=[]
for i,(n,t) in enumerate(sfx):
    e=t+sfx_len[n]
    for li,end in enumerate(lanes):
        if end<=t: lanes[li]=e; break
    else: lanes.append(e); li=len(lanes)-1
    out.append(f'      <audio id="sfx{i+1:02d}" class="clip" src="assets/sfx/{n}.wav" data-start="{t}" data-duration="{sfx_len[n]}" data-volume="1" data-track-index="{10+li}"></audio>')
vids=[]; 
for i,(n,s,d,v) in enumerate(clips):
    vids.append(f'''      <div id="w{i+1}" class="wrap" style="z-index:{i+1}">
        <video id="v{i+1}" class="clip" src="assets/media/{n}.mp4" data-start="{s}" data-duration="{d}" data-media-start="0" data-volume="{v}" data-has-audio="true" playsinline data-track-index="0"></video>
      </div>''')
scenes=[("hook",0,4),("cal",4,10),("otot",14,8),("usp",22,9.5),("cta",31.5,5.5)]
sc=[f'      <div id="{n}" data-composition-id="{n}" data-composition-src="compositions/{n}.html" data-start="{s}" data-duration="{d}" data-width="1080" data-height="1920" data-track-index="1" data-track-kind="graphics" style="z-index:20"></div>' for n,s,d in scenes]
zoom="\n".join(f'      tl.fromTo("#w{i+1}", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.7, ease: "expo.out" }}, {s});' for i,(n,s,d,v) in enumerate(clips))
flash="\n".join(f'      tl.fromTo("#flash", {{ opacity: 0.85 }}, {{ opacity: 0, duration: 0.24, ease: "power2.out" }}, {c});' for c in cuts)
html=f'''<!doctype html>
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
    <div id="root" data-composition-id="main" data-start="0" data-duration="37" data-width="1080" data-height="1920" data-fps="60">
      <div id="bg"></div>
{chr(10).join(vids)}
{chr(10).join(sc)}
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="37" data-width="1080" data-height="1920" data-track-index="2" data-track-kind="captions" style="z-index:30"></div>
      <div id="flash" data-layout-ignore></div>
{chr(10).join(out)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      // Zoom masuk ringkas pada setiap klip
{zoom}
      // Kilatan putih pada setiap potongan
      tl.set("#flash", {{ opacity: 0 }}, 0);
{flash}
      tl.set("#flash", {{ opacity: 0 }}, 36.99);
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open("/home/user/hf/skipping/index.html","w").write(html)
print(len(out),"sfx,",len(lanes),"lanes")
