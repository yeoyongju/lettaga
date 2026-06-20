"""Lettaga feature GIF studio — offline Pillow renderer.
Renders at 2x supersample then downsamples to 640x400 for crisp edges.
Brand tokens from Vue3 BLUE_THEME / mockup.html.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os

# ---- canvas ----
SS = 2
W, H = 640, 400
CW, CH = W*SS, H*SS

# ---- brand tokens ----
BLUE   = (27,132,255)      # #1B84FF
BLUE_D = (30,79,196)       # #1e4fc4
LBLUE  = (237,245,253)     # #EDF5FD
TILE_B = (234,242,255)     # #eaf2ff
GREEN  = (51,178,74)       # #33b24a
GREEN2 = (21,192,111)      # #15c06f
TILE_G = (231,247,238)
AMBER  = (207,138,44)      # #cf8a2c
TILE_A = (255,244,230)
RED    = (242,48,79)       # #f2304f
INK    = (58,71,82)        # #3A4752
SOFT   = (118,139,158)     # #768B9E
FAINT  = (154,166,189)
LINE   = (227,233,242)
LINE2  = (210,219,231)
BG     = (238,245,249)     # #eef5f9
CARD   = (255,255,255)
PURPLE = (123,92,255)      # AI accent #7b5cff
WHITE  = (255,255,255)

FONT_DIR = "/usr/share/fonts/truetype/liberation"
_RE = os.path.join(FONT_DIR, "LiberationSans-Regular.ttf")
_BD = os.path.join(FONT_DIR, "LiberationSans-Bold.ttf")
_fc = {}
def font(size, bold=False):
    key=(size,bold)
    if key not in _fc:
        _fc[key]=ImageFont.truetype(_BD if bold else _RE, int(round(size*SS)))
    return _fc[key]

# ---- easing ----
def clamp(x,a=0.0,b=1.0): return a if x<a else (b if x>b else x)
def lerp(a,b,t): return a+(b-a)*t
def lerp2(p,q,t): return (lerp(p[0],q[0],t), lerp(p[1],q[1],t))
def ease_out(t): t=clamp(t); return 1-(1-t)**3
def ease_in(t): t=clamp(t); return t*t*t
def ease_io(t):
    t=clamp(t)
    return 4*t*t*t if t<0.5 else 1-(-2*t+2)**3/2
def seg(t,start,dur):
    """local 0..1 progress for a segment starting at `start` lasting `dur`."""
    if dur<=0: return 1.0 if t>=start else 0.0
    return clamp((t-start)/dur)
def pulse(t,start,dur):
    """0->1->0 over the window."""
    p=seg(t,start,dur)
    return math.sin(p*math.pi)
def lerp_col(c1,c2,t):
    t=clamp(t)
    return tuple(int(round(lerp(c1[i],c2[i],t))) for i in range(3))

# ---- drawing helpers (coords in 2x space) ----
def S(v): return int(round(v*SS))

def rrect(d, box, r, fill=None, outline=None, width=1):
    x0,y0,x1,y1=[S(v) for v in box]
    d.rounded_rectangle([x0,y0,x1,y1], radius=S(r), fill=fill, outline=outline, width=S(width) if outline else 0)

def soft_shadow(img, box, r, blur=14, alpha=42, dy=8, color=(20,40,80)):
    """draw a soft drop shadow of a rounded rect onto img (RGB)."""
    x0,y0,x1,y1=[S(v) for v in box]
    pad=S(blur*2)
    lw=(x1-x0)+pad*2; lh=(y1-y0)+pad*2
    layer=Image.new("RGBA",(lw,lh),(0,0,0,0))
    ld=ImageDraw.Draw(layer)
    ld.rounded_rectangle([pad,pad,pad+(x1-x0),pad+(y1-y0)], radius=S(r), fill=color+(alpha,))
    layer=layer.filter(ImageFilter.GaussianBlur(S(blur)))
    img.paste(Image.alpha_composite(Image.new("RGBA",layer.size,(0,0,0,0)),layer),
              (x0-pad, y0-pad+S(dy)), layer)

def text(d, xy, s, f, fill, anchor="la"):
    d.text((S(xy[0]),S(xy[1])), s, font=f, fill=fill, anchor=anchor)

def text_w(d, s, f):
    return d.textlength(s, font=f)/SS

def pill(d, box, label, f, bg, fg, r=None):
    x0,y0,x1,y1=box
    if r is None: r=(y1-y0)/2
    rrect(d,box,r,fill=bg)
    d.text((S((x0+x1)/2),S((y0+y1)/2)), label, font=f, fill=fg, anchor="mm")

def vline(d,x,y0,y1,fill,w=1):
    d.line([S(x),S(y0),S(x),S(y1)], fill=fill, width=S(w))
def hline(d,x0,x1,y,fill,w=1):
    d.line([S(x0),S(y),S(x1),S(y)], fill=fill, width=S(w))

# ---- vector icons (centered in box [cx,cy], size px) drawn at 2x ----
def _pts(seq,cx,cy,s):
    return [(S(cx+px*s), S(cy+py*s)) for px,py in seq]
pts=_pts  # public alias (import * skips underscore names)

def ic_check(d,cx,cy,s,fill,w=2.2):
    p=_pts([(-0.34,0.02),(-0.10,0.26),(0.36,-0.28)],cx,cy,s)
    d.line(p,fill=fill,width=S(w),joint="curve")

def ic_check_circle(d,cx,cy,s,fg=WHITE,bg=GREEN):
    d.ellipse([S(cx-s),S(cy-s),S(cx+s),S(cy+s)],fill=bg)
    ic_check(d,cx,cy,s*0.95,fg,w=s*0.20)

def ic_arrow_down(d,cx,cy,s,fill,w=2.4):
    d.line([(S(cx),S(cy-s)),(S(cx),S(cy+s))],fill=fill,width=S(w))
    d.line(_pts([(-0.5,0.45),(0,1.0)],cx,cy,s),fill=fill,width=S(w),joint="curve")
    d.line(_pts([(0.5,0.45),(0,1.0)],cx,cy,s),fill=fill,width=S(w),joint="curve")

def ic_doc(d,cx,cy,s,fill=WHITE,line=None,fold=True):
    x0,y0,x1,y1=cx-s*0.62,cy-s*0.8,cx+s*0.62,cy+s*0.8
    fx=s*0.34
    body=[(x0,y0),(x1-fx,y0),(x1,y0+fx),(x1,y1),(x0,y1)]
    d.polygon([(S(a),S(b)) for a,b in body],fill=fill)
    if fold:
        d.polygon(_pts([(0.28,-0.8),(0.62,-0.46),(0.28,-0.46)],cx,cy,s),fill=line or LINE2)
    if line:
        for i,yy in enumerate([-0.30,-0.05,0.20,0.45]):
            d.line([(S(cx-s*0.40),S(cy+s*yy)),(S(cx+s*(0.40 if i else 0.10)),S(cy+s*yy))],fill=line,width=S(s*0.12))

def ic_pen(d,cx,cy,s,fill=BLUE):
    # diagonal pen nib
    body=_pts([(-0.55,0.55),(0.30,-0.30),(0.55,-0.05),(-0.30,0.80),(-0.62,0.86)],cx,cy,s)
    d.polygon(body,fill=fill)
    d.polygon(_pts([(-0.30,0.80),(-0.62,0.86),(-0.50,0.55)],cx,cy,s),fill=INK)

def ic_cloud(d,cx,cy,s,fill=BLUE):
    d.ellipse([S(cx-s*0.9),S(cy-s*0.1),S(cx-s*0.1),S(cy+s*0.6)],fill=fill)
    d.ellipse([S(cx-s*0.4),S(cy-s*0.55),S(cx+s*0.5),S(cy+s*0.55)],fill=fill)
    d.ellipse([S(cx+s*0.1),S(cy-s*0.15),S(cx+s*0.9),S(cy+s*0.6)],fill=fill)
    d.rectangle([S(cx-s*0.8),S(cy+s*0.2),S(cx+s*0.8),S(cy+s*0.6)],fill=fill)

def ic_folder(d,cx,cy,s,fill=BLUE):
    x0,y0,x1,y1=cx-s*0.8,cy-s*0.5,cx+s*0.8,cy+s*0.6
    d.polygon(_pts([(-0.8,-0.5),(-0.2,-0.5),(-0.02,-0.28),(0.8,-0.28),(0.8,-0.5)],cx,cy,s),fill=fill)
    rrect(d,[x0,cy-s*0.32,x1,y1],s*0.16,fill=fill)

def ic_lock(d,cx,cy,s,fill=WHITE):
    rrect(d,[cx-s*0.55,cy-s*0.1,cx+s*0.55,cy+s*0.7],s*0.14,fill=fill)
    d.arc([S(cx-s*0.38),S(cy-s*0.62),S(cx+s*0.38),S(cy+s*0.18)],180,360,fill=fill,width=S(s*0.16))

def ic_spark(d,cx,cy,s,fill=PURPLE):
    for ang in (0,90):
        a=math.radians(ang)
        dx,dy=math.cos(a),math.sin(a)
        d.polygon([(S(cx+dx*s),S(cy+dy*s)),(S(cx+dy*s*0.28),S(cy-dx*s*0.28)),
                   (S(cx-dx*s),S(cy-dy*s)),(S(cx-dy*s*0.28),S(cy+dx*s*0.28))],fill=fill)

def ic_link(d,cx,cy,s,fill=BLUE,w=2.0):
    d.arc([S(cx-s*1.05),S(cy-s*0.55),S(cx-s*0.05),S(cy+s*0.55)],300,120,fill=fill,width=S(w))
    d.arc([S(cx+s*0.05),S(cy-s*0.55),S(cx+s*1.05),S(cy+s*0.55)],120,300,fill=fill,width=S(w))
    d.line([(S(cx-s*0.35),S(cy)),(S(cx+s*0.35),S(cy))],fill=fill,width=S(w))

def ic_refresh(d,cx,cy,s,fill=GREEN,w=2.0):
    d.arc([S(cx-s),S(cy-s),S(cx+s),S(cy+s)],300,210,fill=fill,width=S(w))
    d.polygon(pts([(0.5,-1.02),(1.02,-0.86),(0.62,-0.46)],cx,cy,s),fill=fill)
    d.arc([S(cx-s),S(cy-s),S(cx+s),S(cy+s)],120,30,fill=fill,width=S(w))
    d.polygon(pts([(-0.5,1.02),(-1.02,0.86),(-0.62,0.46)],cx,cy,s),fill=fill)

def ic_warn(d,cx,cy,s,fill=AMBER,glyph=WHITE):
    d.polygon(pts([(0,-0.95),(0.92,0.72),(-0.92,0.72)],cx,cy,s),fill=fill)
    d.line([(S(cx),S(cy-s*0.30)),(S(cx),S(cy+s*0.22))],fill=glyph,width=S(s*0.20))
    d.ellipse([S(cx-s*0.11),S(cy+s*0.36),S(cx+s*0.11),S(cy+s*0.58)],fill=glyph)

def ic_book(d,cx,cy,s,fill=GREEN):
    rrect(d,[cx-s*0.7,cy-s*0.78,cx+s*0.7,cy+s*0.82],s*0.12,fill=fill)
    d.line([(S(cx),S(cy-s*0.6)),(S(cx),S(cy+s*0.64))],fill=WHITE,width=S(s*0.14))

def ic_spinner(d,cx,cy,s,ang,fill=BLUE,w=2.4):
    a0=ang%360
    d.arc([S(cx-s),S(cy-s),S(cx+s),S(cy+s)],a0,a0+270,fill=fill,width=S(w))

def ic_building(d,cx,cy,s,fill=WHITE):
    rrect(d,[cx-s*0.7,cy-s*0.85,cx+s*0.7,cy+s*0.9],s*0.12,fill=fill)
    return

def ic_grid(d,cx,cy,s,fill=WHITE):
    for ox in (-0.5,0.5):
        for oy in (-0.5,0.5):
            rrect(d,[cx+ox*s-s*0.34,cy+oy*s-s*0.34,cx+ox*s+s*0.34,cy+oy*s+s*0.34],s*0.12,fill=fill)

def ic_bars(d,cx,cy,s,fill=WHITE):
    for i,h in enumerate((0.5,0.9,0.7)):
        x=cx+(i-1)*s*0.55
        rrect(d,[x-s*0.16,cy+s*0.8-s*1.6*h,x+s*0.16,cy+s*0.8],s*0.06,fill=fill)

def ic_clip(d,cx,cy,s,fill=WHITE):
    rrect(d,[cx-s*0.6,cy-s*0.8,cx+s*0.6,cy+s*0.85],s*0.14,fill=fill)
    rrect(d,[cx-s*0.28,cy-s*0.95,cx+s*0.28,cy-s*0.62],s*0.08,fill=fill)

def side_rail(img,d, active=1, items=None, bottom=None):
    """slim Lettaga-style icon rail on the left inside the window. returns content x0."""
    rx0,rx1=24,66; ry0,ry1=52,(bottom if bottom else H-60)
    rrect(d,[rx0,ry0,rx1,ry1],14,fill=(247,250,253))
    icons=[ic_grid, ic_building, ic_clip, ic_pen, ic_bars]
    ys=[ry0+34+i*44 for i in range(5)]
    for i,(fn,yy) in enumerate(zip(icons,ys)):
        act=(i==active)
        if act:
            rrect(d,[rx0+8,yy-15,rx1-8,yy+15],9,fill=BLUE)
        fn(d,(rx0+rx1)/2,yy,7,WHITE if act else (170,182,200))
    return 78

def ic_search(d,cx,cy,s,fill=SOFT,w=2):
    d.ellipse([S(cx-s*0.7),S(cy-s*0.7),S(cx+s*0.2),S(cy+s*0.2)],outline=fill,width=S(w))
    d.line([(S(cx+s*0.1),S(cy+s*0.1)),(S(cx+s*0.7),S(cy+s*0.7))],fill=fill,width=S(w))

def ic_phone(d,x0,y0,x1,y1,body=INK,screen=WHITE):
    rrect(d,[x0,y0,x1,y1],(x1-x0)*0.16,fill=body)
    rrect(d,[x0+3,y0+7,x1-3,y1-7],(x1-x0)*0.10,fill=screen)

# ---- window chrome ----
def base_window(title="lettaga", sub=None, full=False):
    """returns RGBA base image with app window + titlebar.
    full=True extends the card to near the bottom edge (no caption strip)."""
    img=Image.new("RGB",(CW,CH),BG)
    d=ImageDraw.Draw(img)
    cb = H-16 if full else H-58
    # outer app card
    soft_shadow(img,[16,14,W-16,cb],18,blur=16,alpha=34,dy=10)
    rrect(d,[16,14,W-16,cb],18,fill=CARD)
    # titlebar
    rrect(d,[16,14,W-16,46],18,fill=(248,250,253))
    d.rectangle([S(16),S(36),S(W-16),S(46)],fill=(248,250,253))
    for i,c in enumerate([(255,95,86),(255,189,46),(39,201,63)]):
        d.ellipse([S(34+i*16),S(27),S(34+i*16+8),S(35)],fill=c)
    # brand wordmark
    text(d,(W/2,30),title,font(11,True),(150,162,180),anchor="mm")
    hline(d,16,W-16,46,LINE)
    return img,d

def caption_bar(d, head, sub=None, accent=BLUE):
    """bottom caption strip below the window."""
    y=H-44
    d.rectangle([S(0),S(y),S(W),S(H)],fill=BG)
    # accent dot
    cx=30
    d.ellipse([S(cx-5),S(y+15),S(cx+5),S(y+25)],fill=accent)
    text(d,(cx+16,y+8),head,font(14.5,True),INK,anchor="lm")
    if sub:
        text(d,(cx+16,y+27),sub,font(10.5,False),SOFT,anchor="lm")

# ---- GIF assembly ----
import numpy as np
def save_gif(frames_rgb, path, fps=12.5, colors=128):
    """Downsample to 640x400, map all frames to ONE shared palette, then store only
    the pixels that change each frame (rest = transparent). Big size win for UI motion."""
    small=[f.resize((W,H), Image.LANCZOS) for f in frames_rgb]
    n=len(small)
    # build a single global palette from a sample of frames
    sample=small[::max(1,n//12)] or small
    strip=Image.new("RGB",(W, H*len(sample)))
    for i,im in enumerate(sample): strip.paste(im,(0,H*i))
    pal_img=strip.quantize(colors=colors, method=Image.FASTOCTREE, dither=Image.NONE)
    # map every frame to that palette
    idx=[np.asarray(im.quantize(palette=pal_img, dither=Image.NONE), dtype=np.uint8) for im in small]
    TRANSP=colors  # reserved transparent index (just past used colors)
    out=[]
    first=Image.fromarray(idx[0],mode="P"); first.putpalette(pal_img.getpalette())
    out.append(first)
    prev=idx[0]
    for k in range(1,n):
        cur=idx[k].copy()
        same=(cur==prev)
        cur[same]=TRANSP
        im=Image.fromarray(cur,mode="P"); im.putpalette(pal_img.getpalette())
        im.info["transparency"]=TRANSP
        out.append(im)
        prev=idx[k]
    dur=int(round(1000.0/fps))
    out[0].save(path, save_all=True, append_images=out[1:], duration=dur, loop=0,
                disposal=1, optimize=False, transparency=TRANSP)
    return path
