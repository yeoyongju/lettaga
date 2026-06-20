"""Annual Return (Malaysia) — prepared automatically from synced Register data,
validated in SSM's MBRS (XBRL) format, ready to lodge. Country-specific: MY."""
from studio import *
from PIL import Image, ImageDraw

DUR=4.0; FPS=12.5
N=int(DUR*FPS)

STEPS=[("Recollect from Register","Directors, shareholders & address — from synced data",0.12),
       ("Filing Info & Certification","Section G certified by the secretary",0.34),
       ("XBRL Validation (MBRS)","Checked against SSM's MBRS taxonomy",0.52),
       ("Generate XBRL & Confirm","Draft finalised — status turns Collected",0.72)]

def frame(t):
    img,d=base_window("lettaga · Annual Return", full=True)
    cx0=side_rail(img,d,active=2,bottom=H-24)

    # header
    text(d,(cx0+10,66),"Annual Return", font(15,True), INK, anchor="lm")
    text(d,(cx0+10,87),"AR4 · Malaysia · SSM (MBRS)", font(9.5,False), SOFT, anchor="lm")
    rrect(d,[470,56,600,77],10,fill=LBLUE)
    text(d,(535,66),"SSM · MBRS", font(9,True), BLUE_D, anchor="mm")

    # info bar
    ib0,ib1=cx0+4,604; iy=100
    rrect(d,[ib0,iy,ib1,iy+38],10,fill=(250,251,253),outline=LINE,width=1)
    cells=[("Entity","Apex Holdings SDN. BHD."),("Reg no","202401017631"),
           ("AR due","30 Sep 2026"),("AGM due","31 Aug 2026")]
    cw=(ib1-ib0)/4
    for i,(k,v) in enumerate(cells):
        x=ib0+12+i*cw
        text(d,(x,iy+13),k.upper(), font(7,True), FAINT, anchor="lm")
        col = AMBER if k=="AR due" else INK
        text(d,(x,iy+27),v, font(8.5,True), col, anchor="lm")
        if i: vline(d,ib0+i*cw,iy+8,iy+30,LINE)

    # main editor card
    mx0,my0,mx1,my1=cx0+4,150,604,372
    rrect(d,[mx0,my0,mx1,my1],11,fill=WHITE,outline=LINE,width=1)
    text(d,(mx0+16,my0+18),"AR4 · Annual Return", font(10.5,True), INK, anchor="lm")
    collected = t>0.84
    stt = "COLLECTED" if collected else "DRAFT · v1"
    sbg = TILE_G if collected else (240,243,248); sfg = GREEN if collected else SOFT
    tw=text_w(d,stt,font(8,True))
    rrect(d,[mx1-tw-26,my0+8,mx1-12,my0+26],9,fill=sbg)
    text(d,(mx1-tw-18,my0+17),stt,font(8,True),sfg,anchor="lm")
    hline(d,mx0+12,mx1-12,my0+34,LINE)

    ang=t*1440
    sy0=my0+44; srh=37
    for i,(title,sub,tt) in enumerate(STEPS):
        y=sy0+i*srh
        done=t>=tt+0.14
        active = (tt<=t<tt+0.14)
        # icon
        ix=mx0+26
        if (i==2 and not done and t>=tt):   # validation spins
            ic_spinner(d,ix,y+10,7,ang,BLUE,2.2)
        elif done:
            ic_check_circle(d,ix,y+10,7,WHITE,GREEN)
        else:
            d.ellipse([S(ix-7),S(y+3),S(ix+7),S(y+17)],outline=(214,221,232),width=S(1.6))
            text(d,(ix,y+10),str(i+1),font(8,True),FAINT,anchor="mm")
        a = ease_out(seg(t,tt,0.16)) if t>=tt else 0.25
        text(d,(mx0+44,y+6),title, font(9.5,True), lerp_col(FAINT,INK,a), anchor="lm")
        text(d,(mx0+44,y+20),sub, font(8,False), lerp_col((230,234,240),SOFT,a), anchor="lm")
        if i==2 and done:
            text(d,(mx1-16,y+10),"passed", font(8,True), GREEN, anchor="rm")
        if i<len(STEPS)-1: hline(d,mx0+44,mx1-16,y+srh-6,(245,247,251))

    # footer: ready to lodge
    fr=seg(t,0.86,0.12)
    if fr>0:
        a=ease_out(fr); fy=my1-24
        hline(d,mx0+12,mx1-12,fy-9,LINE)
        ic_check_circle(d,mx0+24,fy,6,WHITE,lerp_col(WHITE,GREEN,a))
        text(d,(mx0+36,fy),"Ready to lodge with SSM", font(9,True), lerp_col(WHITE,INK,a), anchor="lm")
        rrect(d,[mx1-118,fy-11,mx1-14,fy+11],8,fill=lerp_col(WHITE,BLUE,a))
        text(d,(mx1-66,fy),"Lodge to SSM", font(8.5,True), lerp_col(WHITE,WHITE,a) if a>.5 else SOFT, anchor="mm")

    return img

def build():
    return [frame(((i/FPS)%DUR)/DUR) for i in range(N)]

if __name__=="__main__":
    fr=build(); save_gif(fr,"ar.gif",fps=FPS,colors=128)
    print("done",os.path.getsize("ar.gif"))
