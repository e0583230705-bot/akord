import numpy as np, subprocess, wave, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
U='/root/.claude/uploads/24d64b93-7524-557a-8518-cb2326d2717f/'
OUT='/tmp/claude-0/-home-user-akord/24d64b93-7524-557a-8518-cb2326d2717f/scratchpad/video/'
W,H,FPS=1080,1920,30
FB='/tmp/claude-0/-home-user-akord/24d64b93-7524-557a-8518-cb2326d2717f/scratchpad/fonts/frl.ttf'
def load(n,crop=None):
    im=Image.open(U+n).convert('RGB')
    return im.crop(crop) if crop else im
dad=load('d0afc983-image.jpg',(0,510,1080,1950))
p_class=load('d50c394a-image.jpg'); p_chalk=load('f8aeeea0-image.jpg')
p_bus=load('568d5f54-image.jpg'); p_glass=load('29037d97-image.jpg'); p_sit=load('0095f5bf-image.jpg')

def warm(im,amt=0.06):
    a=np.asarray(im).astype(np.float32); a[...,0]*=1+amt; a[...,2]*=1-amt
    return Image.fromarray(np.clip(a,0,255).astype(np.uint8))
dad=warm(dad,0.05)

def bg_of(im):  # blurred fill background
    s=max(W/im.width,H/im.height); b=im.resize((int(im.width*s)+2,int(im.height*s)+2))
    b=b.crop(((b.width-W)//2,(b.height-H)//2,(b.width-W)//2+W,(b.height-H)//2+H))
    b=b.filter(ImageFilter.GaussianBlur(40))
    return Image.fromarray((np.asarray(b)*0.45).astype(np.uint8))

def fit_card(im,maxw,maxh):
    s=min(maxw/im.width,maxh/im.height); return im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)

def text_layer(lines,y,size=72,alpha=1.0):
    L=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(L)
    f=ImageFont.truetype(FB,size); f.set_variation_by_name('Bold')
    for i,t in enumerate(lines):
        bb=d.textbbox((0,0),t,font=f,direction='rtl'); w=bb[2]-bb[0]
        x=(W-w)//2; yy=y+i*int(size*1.35)
        sh=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(sh).text((x+3,yy+4),t,font=f,fill=(0,0,0,200),direction='rtl')
        L=Image.alpha_composite(L,sh.filter(ImageFilter.GaussianBlur(6)))
        d=ImageDraw.Draw(L); d.text((x,yy),t,font=f,fill=(255,244,225,255),direction='rtl')
    if alpha<1:
        a=np.asarray(L).copy(); a[...,3]=(a[...,3]*alpha).astype(np.uint8); L=Image.fromarray(a)
    return L

def ease(t): return t*t*(3-2*t)

# scene: photo card with slow zoom (Ken Burns) on blurred bg
def photo_scene(im,secs,lines,ty=1500,zoom=(1.0,1.08),pan=(0,0),full=False):
    bg=bg_of(im); n=int(secs*FPS)
    if full:
        base=im
        s0=max(W/base.width,H/base.height)
    else:
        base=fit_card(im,W-80,1300)
        py0=180 if base.height>1000 else 380
        ty=py0+base.height+90
    frames=[]
    tl=text_layer(lines,ty,84) if lines else None
    for i in range(n):
        t=i/(n-1); z=zoom[0]+(zoom[1]-zoom[0])*ease(t)
        if full:
            s=s0*z; r=base.resize((int(base.width*s),int(base.height*s)),Image.BILINEAR)
            ox=(r.width-W)//2+int(pan[0]*t); oy=(r.height-H)//2+int(pan[1]*t)
            fr=r.crop((ox,oy,ox+W,oy+H))
        else:
            fr=bg.copy()
            r=base.resize((int(base.width*z),int(base.height*z)),Image.BILINEAR)
            cw,ch=base.width,base.height
            ox=(r.width-cw)//2+int(pan[0]*t); oy=(r.height-ch)//2+int(pan[1]*t)
            card=r.crop((ox,oy,ox+cw,oy+ch))
            px=(W-cw)//2; py=py0
            fr.paste(Image.new('RGB',(cw+20,ch+20),(250,244,232)),(px-10,py-10)); fr.paste(card,(px,py))
        fr=fr.convert('RGBA')
        if tl:
            ta=min(1,max(0,(t-0.12)/0.2))
            if ta>0:
                a=np.asarray(tl).copy(); a[...,3]=(a[...,3]*ta).astype(np.uint8)
                fr=Image.alpha_composite(fr,Image.fromarray(a))
        frames.append(fr.convert('RGB'))
    return frames

def title_scene(lines,secs,size=88,heart=False):
    n=int(secs*FPS); base=Image.new('RGB',(W,H),(14,10,8)); fr=[]
    tl=text_layer(lines,H//2-int(size*1.35*len(lines)/2),size)
    for i in range(n):
        t=i/(n-1); a=min(1,t/0.3)*min(1,(1-t)/0.25)
        x=np.asarray(tl).copy(); x[...,3]=(x[...,3]*max(0,a)).astype(np.uint8)
        fr.append(Image.alpha_composite(base.convert('RGBA'),Image.fromarray(x)).convert('RGB'))
    return fr

def draw_heart(d,cx,cy,s,col):
    pts=[]
    for k in range(200):
        a=2*math.pi*k/200
        x=16*math.sin(a)**3; y=13*math.cos(a)-5*math.cos(2*a)-2*math.cos(3*a)-math.cos(4*a)
        pts.append((cx+x*s,cy-y*s))
    d.polygon(pts,fill=col)

def together_scene(secs,lines):
    # father and daughter side by side: two framed photos that slide toward each other
    n=int(secs*FPS); bg=bg_of(p_class)
    a=fit_card(dad,500,1000); b=fit_card(p_bus,500,1000)
    h=min(a.height,b.height); a=a.resize((int(a.width*h/a.height),h)); b=b.resize((int(b.width*h/b.height),h))
    tl=text_layer(lines,260+h+24+220,90); fr=[]
    def framed(p):
        f=Image.new('RGB',(p.width+24,p.height+24),(250,244,232)); f.paste(p,(12,12)); return f
    A,B=framed(a),framed(b); gap=30
    for i in range(n):
        t=i/(n-1); e=ease(min(1,t/0.45))
        cx=W//2; y=260
        xa=int(-A.width+(cx-gap//2-A.width+A.width)*e) if False else int((cx-gap//2-A.width)*e + (-A.width)*(1-e))
        xb=int((cx+gap//2)*e + W*(1-e))
        f=bg.copy().convert('RGBA'); f.paste(A,(xa,y)); f.paste(B,(xb,y))
        if t>0.45:
            ha=min(1,(t-0.45)/0.2); s=4.5+0.4*math.sin(t*14)
            hl=Image.new('RGBA',(W,H),(0,0,0,0)); draw_heart(ImageDraw.Draw(hl),W//2,y+h+24+90,s,(220,40,60,int(235*ha)))
            f=Image.alpha_composite(f,hl)
        if t>0.5:
            ta=min(1,(t-0.5)/0.2); x=np.asarray(tl).copy(); x[...,3]=(x[...,3]*ta).astype(np.uint8)
            f=Image.alpha_composite(f,Image.fromarray(x))
        fr.append(f.convert('RGB'))
    return fr

scenes=[
 lambda: title_scene(['יש קשר','שאין לו מילים'],4.0),
 lambda: photo_scene(dad,6.0,['אבא'],ty=1560,zoom=(1.0,1.10)),
 lambda: photo_scene(p_class,5.5,['והבת שלו','בדרך לכיתה א׳'],ty=1380,zoom=(1.0,1.12)),
 lambda: photo_scene(p_chalk,5.0,['הוא מאמין בה','בכל צעד'],ty=1380,zoom=(1.12,1.0)),
 lambda: photo_scene(p_bus,5.5,['היא יודעת','שהוא תמיד שם'],ty=1560,zoom=(1.0,1.08)),
 lambda: photo_scene(p_glass,5.0,['כל חיוך שלה','הוא האור שלו'],ty=1380,zoom=(1.0,1.12)),
 lambda: photo_scene(p_sit,5.0,['גדלה כל כך מהר...'],ty=1380,zoom=(1.12,1.0)),
 lambda: together_scene(7.0,['אבא ובת','לב אחד']),
 lambda: title_scene(['אוהב אותך','תמיד'],4.5,96),
]
secs=[4.0,6.0,5.5,5.0,5.5,5.0,5.0,7.0,4.5]
XF=int(0.8*FPS)
dur=(sum(int(x*FPS) for x in secs)-XF*(len(secs)-1))/FPS
print('dur',dur)
# soft piano music
sr=44100; N=int(sr*(dur+0.5)); mus=np.zeros(N)
def note(f,t0,d,v):
    i0=int(t0*sr); n=int(d*sr); tt=np.arange(n)/sr
    w=(np.sin(2*np.pi*f*tt)+0.35*np.sin(4*np.pi*f*tt)+0.12*np.sin(6*np.pi*f*tt))*np.exp(-tt*2.2)*(1-np.exp(-tt*200))
    if i0>=N: return
    e=min(N,i0+n); mus[i0:e]+=v*w[:e-i0]
mid=lambda m:440*2**((m-69)/12)
prog=[[48,55,60,64,67],[43,50,55,59,62],[45,52,57,60,64],[41,48,53,57,60]]  # C G Am F
beat=0.5; t=0; bar=0
mel=[76,74,72,74, 74,71,67,71, 72,71,69,72, 69,67,65,67]
while t<dur-1:
    ch=prog[bar%4]
    note(mid(ch[0]-12),t,4,0.35)
    for k,m in enumerate([ch[1],ch[2],ch[3],ch[4],ch[3],ch[2],ch[3],ch[4]]):
        note(mid(m),t+k*beat,2.5,0.13)
    if bar>=2:
        for k in range(4): note(mid(mel[(bar%4)*4+k]),t+k*1.0,2.8,0.2)
    t+=8*beat; bar+=1
rev=mus.copy()
for dl,g in [(0.13,0.3),(0.29,0.22),(0.47,0.15),(0.71,0.1)]:
    k=int(dl*sr); rev[k:]+=g*mus[:-k]
rev*=np.clip(np.arange(N)/(sr*2),0,1)*np.clip((N-np.arange(N))/(sr*3.5),0,1)
rev=rev/np.abs(rev).max()*0.8
with wave.open(OUT+'music.wav','wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((rev*32767).astype(np.int16).tobytes())

p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
  '-i',OUT+'music.wav','-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k',
  '-shortest','-movflags','+faststart','/home/user/akord/video/aba-ubat.mp4'],stdin=subprocess.PIPE)
out=[]; cnt=0
def emit(f):
    global cnt
    p.stdin.write(f.tobytes())
    if cnt in (60,200,420,700,1100): f.resize((360,640)).save(OUT+f'f{cnt}.jpg')
    cnt+=1
tail=None
for mk in scenes:
    sc=mk()
    if tail is not None:
        for k in range(XF): emit(Image.blend(tail[k],sc[k],(k+1)/(XF+1)))
        body=sc[XF:]
    else: body=sc
    for f in body[:-XF]: emit(f)
    tail=body[-XF:]; del sc,body
for f in tail: emit(f)
p.stdin.close(); p.wait(); print('rc',p.returncode,cnt)
