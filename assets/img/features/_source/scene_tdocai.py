"""T-Doc AI — AI auto-extracts [[variables]] & generates for many entities."""
from studio import *
from PIL import Image, ImageDraw

DUR=4.0; FPS=12.5
N=int(DUR*FPS)

VARS=[("[[Company_Name]]","Apex Ventures",118),
      ("[[Director]]","Tan Wei Ming",150),
      ("[[Date]]","20 Jun 2026",182)]

def frame(t):
    img,d=base_window("lettaga · T-Doc AI", full=True)
    # ===== left: template being analysed (the customer's own template) =====
    text(d,(34,62),"Your template", font(12,True), INK, anchor="lm")
    rrect(d,[136,52,250,70],9,fill=TILE_G)
    ic_check_circle(d,149,61,5,WHITE,GREEN)
    text(d,(159,61),"uploaded · DOCX", font(7.5,True), GREEN, anchor="lm")
    tx0,ty0,tx1,ty1=34,76,330,360
    rrect(d,[tx0,ty0,tx1,ty1],12,fill=WHITE,outline=LINE,width=1)
    # heading line
    text(d,((tx0+tx1)/2,ty0+18),"DIRECTORS' RESOLUTION", font(9,True), INK, anchor="mm")
    hline(d,tx0+18,tx1-18,ty0+30,LINE)
    # body filler lines
    for i,yy in enumerate(range(ty0+46,ty1-20,16)):
        w=(tx1-tx0-40) if i%3 else (tx1-tx0-90)
        d.line([(S(tx0+18),S(yy)),(S(tx0+18+w),S(yy))],fill=(228,233,242),width=S(3))
    # AI scan line sweep
    scan=seg(t,0.04,0.40)
    if 0<scan<1:
        sy=lerp(ty0+34,ty1-14,scan)
        d.rectangle([S(tx0+3),S(sy-13),S(tx1-3),S(sy+13)],fill=(243,239,253))
        d.line([(S(tx0+4),S(sy)),(S(tx1-4),S(sy))],fill=PURPLE,width=S(2))
    # the variable rows (highlight when scanned, then fill)
    for lab,val,vy in VARS:
        scanned = scan*(ty1-14-(ty0+34)) >= (vy-(ty0+34)-6) if scan>0 else False
        filled=seg(t,0.50,0.30)
        box=[tx0+18,vy-9,tx1-18,vy+9]
        if filled>0.05:
            a=ease_out(filled)
            rrect(d,box,7,fill=lerp_col((245,246,250),TILE_G,a))
            text(d,(tx0+26,vy),val, font(9,False), lerp_col(SOFT,INK,a), anchor="lm")
            ic_check_circle(d,tx1-28,vy,6,WHITE,GREEN)
        else:
            on = scan>0 and (lerp(ty0+34,ty1-14,scan) >= vy-2)
            rrect(d,box,7,fill=(238,233,255) if on else (245,243,252))
            text(d,(tx0+26,vy),lab, font(9,True), PURPLE if on else (150,140,190), anchor="lm")
    # extracted badge — count grows 0..6 as scan/fill progresses
    nfound = round(clamp(max(seg(t,0.04,0.40), seg(t,0.50,0.30)))*6)
    text(d,(34,372),f"AI extracted {nfound} variables — no manual mapping",
         font(8.5,True), PURPLE, anchor="lm")
    ic_spark(d,310,371,6,PURPLE)

    # ===== right: multi-entity generation =====
    gx0,gy0,gx1,gy1=346,76,602,360
    rrect(d,[gx0,gy0,gx1,gy1],12,fill=(250,251,254),outline=LINE,width=1)
    text(d,((gx0+gx1)/2,gy0+18),"Generate · Multi-entity", font(10,True), INK, anchor="mm")
    text(d,((gx0+gx1)/2,gy0+34),"same document set, every entity", font(8,False), SOFT, anchor="mm")
    # doc cards generating
    total=8
    made=int(seg(t,0.55,0.36)*total+0.001)
    made=max(0,min(total,made))
    bx=gx0+22; by=gy0+50; cw=46; ch=58; gapx=12; gapy=14
    for i in range(total):
        col=i%4; row=i//4
        x=bx+col*(cw+gapx); y=by+row*(ch+gapy)
        if i<made:
            a=ease_out(seg(t,0.55+i*0.035,0.12))
            yoff=(1-a)*-16
            rrect(d,[x,y+yoff,x+cw,y+ch+yoff],7,fill=WHITE,outline=(214,222,236),width=1)
            for k,ly in enumerate([0.30,0.46,0.62]):
                d.line([(S(x+8),S(y+yoff+ch*ly)),(S(x+cw-8 if k else x+cw-18),S(y+yoff+ch*ly))],fill=(223,229,240),width=S(2))
            ic_check_circle(d,x+cw-12,y+yoff+ch-12,6,WHITE,GREEN)
        else:
            rrect(d,[x,y,x+cw,y+ch],7,fill=(238,241,247),outline=(224,229,239),width=1)
    # generate button / result
    btnY=gy1-40
    if made<total:
        rrect(d,[gx0+22,btnY,gx1-22,btnY+26],8,fill=BLUE)
        text(d,((gx0+gx1)/2,btnY+13),f"Generate {total} documents", font(9.5,True), WHITE, anchor="mm")
    else:
        rrect(d,[gx0+22,btnY,gx1-22,btnY+26],8,fill=TILE_G)
        ic_check_circle(d,gx0+44,btnY+13,7,WHITE,GREEN)
        text(d,((gx0+gx1)/2+8,btnY+13),f"{total} documents ready", font(9.5,True), GREEN, anchor="mm")

    return img

def build():
    return [frame(((i/FPS)%DUR)/DUR) for i in range(N)]

if __name__=="__main__":
    fr=build(); save_gif(fr,"t-doc-ai.gif",fps=FPS,colors=128)
    print("done",os.path.getsize("t-doc-ai.gif"))
