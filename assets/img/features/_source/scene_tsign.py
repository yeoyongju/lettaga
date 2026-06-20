"""T-Sign — built-in e-signature, no DocuSign/Adobe. Place field -> send -> all signed."""
from studio import *
from PIL import Image, ImageDraw

DUR=4.0; FPS=12.5
N=int(DUR*FPS)

REC=[("Tan Wei Ming","Director",0.40),
     ("Lim Mei Ling","Director",0.55),
     ("Aisha Rahman","Secretary",0.70)]

def status_for(t, tt):
    # Not viewed -> Viewed -> Signed
    if t < tt: return ("Not viewed",(150,160,176),(238,240,245))
    if t < tt+0.10: return ("Viewed",BLUE,LBLUE)
    return ("Signed",GREEN,TILE_G)

def frame(t):
    img,d=base_window("lettaga · T-Sign", full=True)
    text(d,(34,62),"T-Sign · Signature request", font(12.5,True), INK, anchor="lm")
    # built-in badge
    rrect(d,[446,54,602,76],11,fill=TILE_G)
    ic_check_circle(d,462,65,6,WHITE,GREEN)
    text(d,(475,65),"Built-in e-signature · 24/7", font(8.5,True), GREEN, anchor="lm")

    # ===== left: document with signature field =====
    dx0,dy0,dx1,dy1=34,84,348,376
    rrect(d,[dx0,dy0,dx1,dy1],10,fill=WHITE,outline=LINE,width=1)
    text(d,((dx0+dx1)/2,dy0+18),"BOARD RESOLUTION", font(9,True), INK, anchor="mm")
    hline(d,dx0+16,dx1-16,dy0+30,LINE)
    for i,yy in enumerate(range(dy0+44,dy1-86,15)):
        w=(dx1-dx0-34) if i%3 else (dx1-dx0-80)
        d.line([(S(dx0+16),S(yy)),(S(dx0+16+w),S(yy))],fill=(228,233,242),width=S(3))
    # signature line near bottom
    sigY=dy1-46
    text(d,(dx0+16,sigY-14),"Signature:", font(8.5,False), SOFT, anchor="lm")
    hline(d,dx0+16,dx0+150,sigY,LINE2,1)
    # draggable field: travels from palette(top-right of doc) onto sig line
    drag=ease_io(seg(t,0.05,0.22))
    fx=lerp(dx1-70, dx0+70, drag); fy=lerp(dy0+50, sigY-10, drag)
    placed = t>=0.27
    fcol = GREEN if t>0.78 else BLUE
    rrect(d,[fx-52,fy-12,fx+52,fy+12],7,fill=LBLUE if not placed else (TILE_G if t>0.78 else LBLUE),
          outline=fcol,width=1)
    ic_pen(d,fx-40,fy,6,fcol)
    text(d,(fx-28,fy),"Signature", font(8.5,True), fcol, anchor="lm")
    if t>0.80:
        ic_check_circle(d,fx+40,fy,6,WHITE,GREEN)

    # send button under doc
    btnY=dy1-14
    sent = t>=0.32
    if not sent:
        glow=pulse(t,0.26,0.10)
        rrect(d,[dx0,btnY-2,dx1,btnY+18],8,fill=lerp_col(BLUE,BLUE_D,glow*0.5))
        text(d,((dx0+dx1)/2,btnY+8),"Send signature request", font(9.5,True), WHITE, anchor="mm")
    else:
        rrect(d,[dx0,btnY-2,dx1,btnY+18],8,fill=(244,247,251),outline=LINE,width=1)
        text(d,((dx0+dx1)/2,btnY+8),"Secure links emailed", font(9,True), SOFT, anchor="mm")

    # ===== right: recipients status =====
    rx0,ry0,rx1,ry1=362,84,602,376
    rrect(d,[rx0,ry0,rx1,ry1],10,fill=(250,251,254),outline=LINE,width=1)
    text(d,(rx0+16,ry0+18),"Recipients", font(10,True), INK, anchor="lm")
    allsigned = t>0.80
    if allsigned:
        text(d,(rx1-16,ry0+18),"3 / 3 signed", font(9,True), GREEN, anchor="rm")
    ry=ry0+40; rh=64
    for i,(nm,role,tt) in enumerate(REC):
        y=ry+i*rh
        rrect(d,[rx0+12,y,rx1-12,y+rh-10],9,fill=WHITE,outline=LINE,width=1)
        # avatar
        d.ellipse([S(rx0+24),S(y+9),S(rx0+44),S(y+29)],fill=lerp_col(LBLUE,TILE_G,seg(t,tt+0.10,0.1)))
        text(d,(rx0+34,y+19),nm[0], font(9,True), BLUE if t<tt+0.10 else GREEN, anchor="mm")
        text(d,(rx0+54,y+13),nm, font(10,True), INK, anchor="lm")
        text(d,(rx0+54,y+27),role, font(8,False), SOFT, anchor="lm")
        lab,fg,bg=status_for(t,tt)
        pill(d,[rx1-92,y+9,rx1-20,y+rh-19],lab, font(8,True), bg, fg)
        if lab=="Signed":
            ic_check_circle(d,rx1-100,y+(rh-10)/2,5.5,WHITE,GREEN)

    # saved-to-drive toast
    if t>0.86:
        a=ease_out(seg(t,0.86,0.10))
        text(d,(rx0+16,ry1-14),"Signed files saved to T-Drive", font(8.5,True), lerp_col((250,251,254),GREEN,a), anchor="lm")
        ic_cloud(d,rx1-30,ry1-13,6,lerp_col((250,251,254),GREEN,a))

    return img

def build():
    return [frame(((i/FPS)%DUR)/DUR) for i in range(N)]

if __name__=="__main__":
    fr=build(); save_gif(fr,"t-sign.gif",fps=FPS,colors=128)
    print("done",os.path.getsize("t-sign.gif"))
