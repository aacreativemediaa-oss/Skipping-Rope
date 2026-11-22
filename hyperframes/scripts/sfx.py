import numpy as np, wave, subprocess, re, sys
SR=48000
rng=np.random.default_rng(7)
def t(d): return np.arange(int(SR*d))/SR
def env(n,a,d_rel):
    x=np.linspace(0,1,n); e=np.minimum(1,x/max(a,1e-4)); return e*np.exp(-x*d_rel)
def lp(x,a):  # one-pole lowpass, a in 0..1 per-sample (array or scalar)
    y=np.zeros_like(x); s=0.0; a=np.broadcast_to(a,x.shape)
    for i in range(len(x)): s+= a[i]*(x[i]-s); y[i]=s
    return y
def hp(x,a): return x-lp(x,a)
def save(name,x,target):
    x=x/np.max(np.abs(x)+1e-9)*0.9
    st=np.stack([x,x],1)
    def wr(path,arr):
        w=wave.open(path,'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(arr,-1,1)*32767).astype(np.int16).tobytes()); w.close()
    # measure loudness with padding to >=1s via ffmpeg ebur128 (momentary max)
    pad=np.zeros((SR,2)); tmp='/tmp/_sfx.wav'; wr(tmp,np.concatenate([st,pad]))
    out=subprocess.run(['ffmpeg','-nostats','-i',tmp,'-af','ebur128=peak=none','-f','null','-'],capture_output=True,text=True).stderr
    M=[float(m) for m in re.findall(r'M:\s*(-?[\d.]+)',out)]
    mmax=max(M); g=10**((target-mmax)/20)
    wr(f'/home/user/hf/skipping/assets/sfx/{name}.wav',st*g)
    print(name, 'momentary max', round(mmax,1),'-> gain',round(20*np.log10(g),1),'dB')
TARGET=-36.0  # momentary-max LUFS, kept under a nominal VO level (-30)
# whoosh: bandpassed noise with sweeping cutoff, swell
d=0.55; n=int(SR*d); x=rng.standard_normal(n); sw=np.sin(np.linspace(0,np.pi,n))
a=0.02+0.25*sw**2; w=lp(x,a); w=hp(w,0.01); save('whoosh',w*sw**1.5,TARGET)
# pop: pitch drop sine + click
d=0.12; tt=t(d); f=900*np.exp(-tt*30)+250; ph=2*np.pi*np.cumsum(f)/SR
p=np.sin(ph)*env(len(tt),0.003,40); save('pop',p,TARGET)
# ding: bell partials
d=1.4; tt=t(d); b=sum(a*np.sin(2*np.pi*f*tt)*np.exp(-tt*k) for f,a,k in [(1320,1,3.2),(2640,0.5,4.5),(3960,0.25,6),(1760*1.5,0.15,8)])
b*=np.minimum(1,tt/0.002); save('ding',b,TARGET)
# impact: low sine thump + noise burst
d=0.9; tt=t(d); f=110*np.exp(-tt*6)+42; th=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*5)
nz=lp(rng.standard_normal(len(tt)),0.08)*np.exp(-tt*25)*1.5
save('impact',th+nz*0.6,TARGET+2)
# cha-ching: two metallic hits + shimmer
d=1.2; tt=t(d)
def metal(t0,base):
    tt2=np.clip(tt-t0,0,None); on=(tt>=t0)
    s=sum(np.sin(2*np.pi*base*r*tt2)*np.exp(-tt2*k) for r,k in [(1,6),(2.76,8),(5.4,10),(8.9,14)])
    return s*on
c=metal(0,1800)*0.7+metal(0.11,2400)
sh=hp(rng.standard_normal(len(tt)),0.5)*np.exp(-np.clip(tt-0.11,0,None)*5)*(tt>0.11)*0.4
save('chaching',c+sh,TARGET)
# riser: noise + rising tone over 1.3s, ends abruptly
d=1.3; tt=t(d); k=tt/d; f=180+1400*k**2; tone=np.sin(2*np.pi*np.cumsum(f)/SR)*0.5
nz=lp(rng.standard_normal(len(tt)),0.03+0.5*k**2)
r=(tone+nz)*k**2; r[-200:]*=np.linspace(1,0,200); save('riser',r,TARGET)
# zap: fast descending saw sweep with vibrato
d=0.3; tt=t(d); f=2600*np.exp(-tt*14)+120+60*np.sin(2*np.pi*55*tt); ph=np.cumsum(f)/SR
z=(2*(ph%1)-1)*env(len(tt),0.002,10); z=lp(z,0.35); save('zap',z,TARGET)
