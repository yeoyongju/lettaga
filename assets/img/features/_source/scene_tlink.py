"""T-Link — client self-service via secure deep link, no login."""
from studio import *
from PIL import Image, ImageDraw

DUR=4.0; FPS=12.5
N=int(DUR*FPS)

FIELDS=[("Applicant","Tan Wei Ming",0.34),
        ("Entity name","Apex Ventures SDN. BHD.",0.50),
        ("Reg. address","12 Jalan Ampang, KL",0.66)]
STEPS=["Applicant","Company","Director","Shares","Confirm"]

def frame(t):
    img,d=base_window("lettaga · T-Link", full=True)
    # ---------- left: application list ----------
    text(d,(34,62),"T-Link · Applications", font(13,True), INK, anchor="lm")
    # public deep-link bar
    rrect(d,[34,80,300,108],8,fill=LBLUE,outline=(206,224,250),width=1)
    ic_link(d,48,94,6,BLUE)
    text(d,(60,88),"Public deep link", font(8,True), BLUE_D, anchor="lm")
    text(d,(60,99),"lettaga.my/link/aXk92", font(8.5,False), SOFT, anchor="lm")
    # copy button highlights early
    copy=pulse(t,0.02,0.22)
    rrect(d,[238,86,294,102],7,fill=lerp_col(BLUE,GREEN,seg(t,0.16,0.1)))
    text(d,(266,94),"Copy" if t<0.18 else "Copied", font(8,True), WHITE, anchor="mm")
    text(d,(34,126),"no login required", font(8.5,True), GREEN, anchor="lm")
    ic_check_circle(d,150,123,5.5,WHITE,GREEN)

    # existing rows + new client row (appears at end)
    rows=[("Sunrise Foods","Lim · Complete",GREEN,True),
          ("Delta Marine","Wong · Complete",GREEN,True)]
    newin=seg(t,0.86,0.12)
    ly=150; rh=58
    for i,(nm,who,col,done) in enumerate(rows):
        y=ly+i*rh
        rrect(d,[34,y,360,y+rh-8],9,fill=(250,251,253),outline=LINE,width=1)
        text(d,(48,y+11),nm, font(10.5,True), INK, anchor="lm")
        text(d,(48,y+24),who, font(8.5,False), SOFT, anchor="lm")
        pill(d,[300,y+9,352,y+rh-19],"Complete",font(7.5,True),TILE_G,GREEN)
    # new row
    y=ly+2*rh
    if newin>0:
        a=ease_out(newin)
        rrect(d,[34,y,360,y+rh-8],9,fill=lerp_col(CARD,(240,250,244),a),outline=lerp_col(LINE,GREEN,a),width=1)
        text(d,(48,y+11),"Apex Ventures", font(10.5,True), lerp_col(CARD,INK,a), anchor="lm")
        text(d,(48,y+24),"Tan · just now", font(8.5,False), lerp_col(CARD,SOFT,a), anchor="lm")
        pill(d,[300,y+9,352,y+rh-19],"Complete",font(7.5,True),lerp_col(CARD,TILE_G,a),lerp_col(CARD,GREEN,a))

    # left footer
    lf=seg(t,0.62,0.16)
    if lf>0:
        a=ease_out(lf); fy=336
        hline(d,34,360,fy-14,LINE)
        ic_check_circle(d,42,fy,6,WHITE,lerp_col(CARD,GREEN,a))
        text(d,(54,fy),"All applications up to date — no chasing", font(8.5,True), lerp_col(CARD,INK,a), anchor="lm")

    # ---------- right: client phone ----------
    px0,py0,px1,py1=430,58,602,372
    # flying deep-link chip start -> phone
    if 0.18<t<0.36:
        p=ease_io(seg(t,0.18,0.16))
        cx=lerp(266,(px0+px1)/2,p); cy=lerp(94,150,p)
        rrect(d,[cx-26,cy-9,cx+26,cy+9],9,fill=BLUE)
        text(d,(cx,cy),"link",font(8,True),WHITE,anchor="mm")
    ic_phone(d,px0,py0,px1,py1,body=(38,52,74),screen=(247,250,253))
    sx0,sy0,sx1,sy1=px0+8,py0+16,px1-8,py1-16
    # phone header
    text(d,((sx0+sx1)/2,sy0+14),"Incorporation", font(10,True), INK, anchor="mm")
    text(d,((sx0+sx1)/2,sy0+28),"No account needed", font(7.5,False), GREEN, anchor="mm")
    # step bar (1..5)
    cur=min(4,int(seg(t,0.30,0.55)*5))
    sbY=sy0+44
    for i in range(5):
        cxx=sx0+18+i*((sx1-sx0-36)/4)
        done=i<=cur
        col=GREEN if i<cur else (BLUE if i==cur else (214,221,232))
        d.ellipse([S(cxx-7),S(sbY-7),S(cxx+7),S(sbY+7)],fill=col)
        if i<cur: ic_check(d,cxx,sbY,5,WHITE,w=1.6)
        else: text(d,(cxx,sbY),str(i+1),font(8,True),WHITE,anchor="mm")
        if i<4:
            nx=sx0+18+(i+1)*((sx1-sx0-36)/4)
            hline(d,cxx+8,nx-8,sbY,GREEN if i<cur else (224,230,240),2)
    # filling fields
    fy=sbY+24
    for k,(lab,val,tt) in enumerate(FIELDS):
        y=fy+k*46
        text(d,(sx0+6,y),lab, font(8,True), SOFT, anchor="lm")
        rrect(d,[sx0+6,y+10,sx1-6,y+34],7,fill=WHITE,outline=LINE,width=1)
        typ=seg(t,tt,0.12)
        if typ>0:
            shown=val[:max(1,int(len(val)*ease_out(typ)))]
            text(d,(sx0+14,y+22),shown, font(8.5,False), INK, anchor="lm")
            if typ>=1:
                ic_check_circle(d,sx1-16,y+22,6,WHITE,GREEN)
    # complete banner
    comp=seg(t,0.80,0.12)
    if comp>0:
        a=ease_out(comp)
        by=sy1-30
        rrect(d,[sx0+6,by,sx1-6,by+24],8,fill=lerp_col(WHITE,GREEN,a))
        text(d,((sx0+sx1)/2,by+12),"Submitted ✓" if False else "Submitted", font(9,True), lerp_col(WHITE,WHITE,a) if a>.5 else SOFT, anchor="mm")

    return img

def build():
    return [frame(((i/FPS)%DUR)/DUR) for i in range(N)]

if __name__=="__main__":
    fr=build(); save_gif(fr,"t-link.gif",fps=FPS,colors=128)
    print("done",os.path.getsize("t-link.gif"))
