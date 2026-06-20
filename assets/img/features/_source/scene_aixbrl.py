"""AI XBRL (Singapore) — AI maps financial statements to ACRA's XBRL taxonomy,
produces a Simplified XBRL FS, validates it, ready to file with ACRA.
Marketplace add-on. Country-specific: SG."""
from studio import *
from PIL import Image, ImageDraw

DUR=4.0; FPS=12.5
N=int(DUR*FPS)

FS=[("Revenue","2,400,000",0.18),
    ("Cost of sales","(1,310,000)",0.26),
    ("Profit before tax","410,000",0.34),
    ("Total assets","3,150,000",0.42),
    ("Total equity","1,980,000",0.50)]
MAP=[("Revenue","Revenue",0.30),
     ("Total assets","Assets",0.46),
     ("Total equity","Equity",0.62)]

def frame(t):
    img,d=base_window("lettaga · AI XBRL", full=True)
    cx0=side_rail(img,d,active=4,bottom=H-24)

    # header
    text(d,(cx0+10,66),"AI XBRL", font(15,True), INK, anchor="lm")
    text(d,(cx0+10,87),"AI financial-statement tagging · Singapore", font(9.5,False), SOFT, anchor="lm")
    rrect(d,[452,56,540,77],10,fill=LBLUE); text(d,(496,66),"ACRA", font(9,True), BLUE_D, anchor="mm")
    rrect(d,[546,56,600,77],10,fill=(243,239,253)); text(d,(573,66),"AI", font(9,True), PURPLE, anchor="mm")

    # ===== left: financial statements (source) =====
    lx0,lx1=cx0+4,356
    rrect(d,[lx0,100,lx1,372],11,fill=WHITE,outline=LINE,width=1)
    text(d,(lx0+14,118),"Financial statements", font(10,True), INK, anchor="lm")
    text(d,(lx1-14,118),"FY2025", font(8,False), SOFT, anchor="rm")
    hline(d,lx0+12,lx1-12,130,LINE)
    # AI scan sweep
    scan=seg(t,0.10,0.46)
    if 0<scan<1:
        sy=lerp(140,348,scan); d.rectangle([S(lx0+4),S(sy-12),S(lx1-4),S(sy+12)],fill=(243,239,253))
        d.line([(S(lx0+4),S(sy)),(S(lx1-4),S(sy))],fill=PURPLE,width=S(2))
    ry=146; rh=44
    for i,(nm,val,tt) in enumerate(FS):
        y=ry+i*rh
        rrect(d,[lx0+12,y,lx1-12,y+rh-10],8,fill=(250,251,253),outline=LINE,width=1)
        text(d,(lx0+24,y+(rh-10)/2),nm, font(9.5,False), INK, anchor="lm")
        text(d,(lx1-46,y+(rh-10)/2),val, font(9.5,True), INK, anchor="rm")
        tagged = t>=tt
        if tagged:
            ic_check_circle(d,lx1-28,y+(rh-10)/2,6,WHITE,GREEN)

    # ===== right: AI XBRL tagging =====
    rx0,rx1=368,604
    rrect(d,[rx0,100,rx1,372],11,fill=(250,251,254),outline=LINE,width=1)
    text(d,(rx0+14,118),"AI XBRL", font(10,True), INK, anchor="lm")
    text(d,(rx1-14,118),"ACRA taxonomy", font(8,False), SOFT, anchor="rm")
    hline(d,rx0+12,rx1-12,130,LINE)
    ic_spark(d,rx0+22,150,6,PURPLE)
    text(d,(rx0+34,150),"Mapping financials → XBRL concepts", font(8.5,True), PURPLE, anchor="lm")
    # progress bar + counter
    prog=ease_io(seg(t,0.16,0.55)); tagged=int(prog*142)
    rrect(d,[rx0+14,166,rx1-14,176],5,fill=(234,230,248))
    rrect(d,[rx0+14,166,rx0+14+(rx1-rx0-28)*prog,176],5,fill=PURPLE)
    text(d,(rx0+14,190),f"{tagged} / 142 concepts auto-tagged", font(8.5,True), INK, anchor="lm")
    # sample mappings
    my=208; mrh=34
    for k,(src,dst,tt) in enumerate(MAP):
        y=my+k*mrh
        ap=seg(t,tt,0.14)
        if ap<=0: continue
        a=ease_out(ap)
        text(d,(rx0+16,y+9),src, font(9,False), lerp_col((250,251,254),SOFT,a), anchor="lm")
        # arrow
        ax=rx0+120
        d.line([(S(ax),S(y+9)),(S(ax+16),S(y+9))],fill=lerp_col((250,251,254),(180,170,210),a),width=S(1.6))
        d.polygon(pts([(-0.5,-0.5),(0,0),(-0.5,0.5)],ax+16,y+9,4),fill=lerp_col((250,251,254),(180,170,210),a))
        rrect(d,[ax+22,y+1,rx1-30,y+17],6,fill=lerp_col((250,251,254),(243,239,253),a))
        text(d,(ax+30,y+9),dst, font(8.5,True), lerp_col((250,251,254),PURPLE,a), anchor="lm")
        ic_check_circle(d,rx1-22,y+9,5.5,WHITE,lerp_col((250,251,254),GREEN,a))

    # footer: simplified xbrl + validation + file button
    done=t>=0.78
    fy=326
    hline(d,rx0+12,rx1-12,fy-12,LINE)
    if done:
        a=ease_out(seg(t,0.78,0.12))
        ic_check_circle(d,rx0+22,fy,6,WHITE,lerp_col((250,251,254),GREEN,a))
        text(d,(rx0+34,fy),"Simplified XBRL · validation passed", font(8.5,True), lerp_col((250,251,254),INK,a), anchor="lm")
        rrect(d,[rx0+14,fy+16,rx1-14,fy+38],8,fill=lerp_col((250,251,254),BLUE,a))
        text(d,((rx0+rx1)/2,fy+27),"File with ACRA", font(9.5,True), lerp_col((250,251,254),WHITE,a) if a>.5 else SOFT, anchor="mm")
    else:
        text(d,(rx0+22,fy),"Generating Simplified XBRL…", font(8.5,True), SOFT, anchor="lm")

    return img

def build():
    return [frame(((i/FPS)%DUR)/DUR) for i in range(N)]

if __name__=="__main__":
    fr=build(); save_gif(fr,"ai-xbrl.gif",fps=FPS,colors=128)
    print("done",os.path.getsize("ai-xbrl.gif"))
