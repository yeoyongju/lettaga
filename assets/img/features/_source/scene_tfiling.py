"""T-Filing — pre-filled e-Filing, one-click submit to ACRA & SSM, certificate."""
from studio import *
from PIL import Image, ImageDraw

DUR=4.0; FPS=12.5
N=int(DUR*FPS)

FORMFIELDS=[("Entity name","Apex Ventures SDN. BHD.",0.10),
            ("Registration type","Direct Incorporation",0.20),
            ("Registered address","12 Jalan Ampang, KL",0.30),
            ("Paid-up capital","RM 100,000",0.40)]
STAGES=[("Document",GREEN),("T-Sign",GREEN),("e-Filing",None),("Register",None)]

def frame(t):
    img,d=base_window("lettaga · e-Filing", full=True)
    text(d,(34,62),"e-Filing", font(13,True), INK, anchor="lm")
    # ACRA + SSM dual badge
    rrect(d,[470,54,602,76],11,fill=LBLUE)
    text(d,(536,65),"ACRA · SSM", font(9,True), BLUE_D, anchor="mm")
    # pre-filled tag
    pf=seg(t,0.0,0.45)
    text(d,(34,80),"Pre-filled from your task", font(8.5,True), GREEN, anchor="lm")
    ic_check_circle(d,168,79,5.5,WHITE,GREEN)

    # ===== form card =====
    fx0,fy0,fx1,fy1=34,92,602,276
    rrect(d,[fx0,fy0,fx1,fy1],12,fill=WHITE,outline=LINE,width=1)
    colw=(fx1-fx0-48)/2
    for i,(lab,val,tt) in enumerate(FORMFIELDS):
        col=i%2; row=i//2
        x=fx0+20+col*(colw+8); y=fy0+18+row*54
        text(d,(x,y),lab, font(8.5,True), SOFT, anchor="lm")
        rrect(d,[x,y+10,x+colw,y+34],7,fill=(250,251,253),outline=LINE,width=1)
        fill=seg(t,tt,0.12)
        if fill>0:
            shown=val[:max(1,int(len(val)*ease_out(fill)))]
            text(d,(x+10,y+22),shown, font(9,False), INK, anchor="lm")
            if fill>=1: ic_check_circle(d,x+colw-16,y+22,5.5,WHITE,GREEN)

    # declaration checkbox
    decY=fy1-22
    tick=t>0.52
    rrect(d,[fx0+20,decY-8,fx0+36,decY+8],4,fill=GREEN if tick else WHITE,outline=GREEN if tick else LINE2,width=1)
    if tick: ic_check(d,fx0+28,decY,5,WHITE,w=1.6)
    text(d,(fx0+44,decY),"I agree the information is true and correct.", font(9,False), INK, anchor="lm")

    # ===== submit button -> progress -> completed =====
    bx0,by0,bx1,by1=fx0,290,fx1,328
    phase_press=seg(t,0.58,0.06)
    phase_prog=seg(t,0.62,0.16)
    done=t>=0.80
    if not done:
        if t<0.62:
            glow=pulse(t,0.56,0.10)
            rrect(d,[bx0,by0,bx1,by1],10,fill=lerp_col(BLUE,BLUE_D,glow*0.4))
            ic_cloud(d,(bx0+bx1)/2-78,(by0+by1)/2,8,WHITE)
            text(d,((bx0+bx1)/2+6,(by0+by1)/2),"Submit to ACRA · SSM — one click", font(11,True), WHITE, anchor="mm")
        else:
            rrect(d,[bx0,by0,bx1,by1],10,fill=BLUE_D)
            # progress bar
            pw=(bx1-bx0-40)*ease_io(phase_prog)
            rrect(d,[bx0+20,(by0+by1)/2-4,bx0+20+max(6,pw),(by0+by1)/2+4],4,fill=WHITE)
            text(d,((bx0+bx1)/2,(by0+by1)/2-16),"Filing to registry…", font(8.5,True), (210,225,255), anchor="mm")
    else:
        a=ease_out(seg(t,0.80,0.12))
        rrect(d,[bx0,by0,bx1,by1],10,fill=lerp_col(BLUE_D,TILE_G,a))
        ic_check_circle(d,(bx0+bx1)/2-92,(by0+by1)/2,9,WHITE,lerp_col(BLUE_D,GREEN,a))
        text(d,((bx0+bx1)/2-72,(by0+by1)/2-1),"E-Filing Completed", font(11,True), lerp_col(WHITE,GREEN,a), anchor="lm")
        # download certificate chip
        rrect(d,[bx1-150,by0+8,bx1-14,by1-8],8,fill=lerp_col(BLUE_D,WHITE,a),outline=lerp_col(BLUE_D,GREEN,a),width=1)
        text(d,(bx1-82,(by0+by1)/2),"Download Certificate", font(8,True), lerp_col(BLUE_D,GREEN,a), anchor="mm")

    # ===== task stage bar =====
    syy=356
    text(d,(34,syy-2),"Task progress", font(8.5,True), SOFT, anchor="lm")
    sx=130; sw=(602-sx)/4
    for i,(nm,col) in enumerate(STAGES):
        cx=sx+sw*i+sw/2
        if nm=="e-Filing":
            c = GREEN if done else (BLUE if t>0.62 else (208,215,228))
        elif col==GREEN:
            c=GREEN
        else:
            c=(208,215,228)
        d.ellipse([S(cx-9),S(syy-9),S(cx+9),S(syy+9)],fill=c)
        if c==GREEN: ic_check(d,cx,syy,6,WHITE,w=1.8)
        text(d,(cx,syy+20),nm, font(7.5,True), INK if c==GREEN or c==BLUE else SOFT, anchor="mm")
        if i<3:
            d.line([(S(cx+10),S(syy)),(S(cx+sw-10),S(syy))],fill=GREEN if (STAGES[i+1][1]==GREEN or (i+1==2 and done)) else (224,230,240),width=S(2))

    return img

def build():
    return [frame(((i/FPS)%DUR)/DUR) for i in range(N)]

if __name__=="__main__":
    fr=build(); save_gif(fr,"t-filing.gif",fps=FPS,colors=128)
    print("done",os.path.getsize("t-filing.gif"))
