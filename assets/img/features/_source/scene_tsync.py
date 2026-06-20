"""T-Sync — real-time, automatic registry sync (country-common, ACRA & SSM).
Faithful to the Lettaga Entity screen: side rail + Entity Synchronisation +
Change History panel. No caption bar (text lives in the page beside it)."""
from studio import *
from PIL import Image, ImageDraw

DUR=4.0; FPS=12.5
N=int(DUR*FPS)

# country-common: badge shows both authorities, entity list mixes jurisdictions
BADGE="ACRA · SSM"
# entities: (name, suffix, reglabel, regno, status)
ENTITIES=[("Apex Holdings","PTE. LTD.","UEN","202401762K","sel"),
          ("Seri Mutiara","SDN. BHD.","Reg no","202301008842","updated"),
          ("Delta Marine","PTE. LTD.","UEN","201930828H","review")]
# change rows: (field, detail, kind, flag) — jurisdiction-neutral values
CHANGES=[("Registered address","Unit 10-2 → Unit 18-1","auto",None),
         ("Director appointed","+ Tan Wei Ming","auto",None),
         ("Issued shares","100,000 → 150,000","review",None)]

def frame(t):
    img,d=base_window("lettaga · Entity", full=True)
    cx0=side_rail(img,d,active=1,bottom=H-24)

    # ===== header =====
    text(d,(cx0+10,66),"Entity", font(15,True), INK, anchor="lm")
    text(d,(cx0+10,87),"Entity Synchronisation", font(9.5,False), SOFT, anchor="lm")
    pr=0.5+0.5*math.sin(t*2*math.pi*2); lx=cx0+150
    d.ellipse([S(lx-4-2*pr),S(87-4-2*pr),S(lx+4+2*pr),S(87+4+2*pr)],fill=(214,240,224))
    d.ellipse([S(lx-3),S(87-3),S(lx+3),S(87+3)],fill=GREEN)
    text(d,(lx+10,87),"Real-time", font(8.5,True), GREEN, anchor="lm")
    # registry badge + auto-sync chip
    rrect(d,[452,56,600,77],10,fill=LBLUE)
    text(d,(526,66),BADGE, font(9,True), BLUE_D, anchor="mm")
    syncing=t<0.66
    if syncing:
        ic_refresh(d,470,93,5.5,BLUE,1.6); text(d,(482,93),"Auto-sync · live", font(8,True), BLUE, anchor="lm")
    else:
        ic_check_circle(d,470,93,5.5,WHITE,GREEN); text(d,(482,93),"Synced just now", font(8,True), GREEN, anchor="lm")

    # ===== left: entity list =====
    lx0,lx1=cx0+4,372
    text(d,(lx0+4,118),"ENTITIES", font(7.5,True), FAINT, anchor="lm")
    ang=t*1440
    ey0=130; erh=52
    for i,(nm,suf,rlab,reg,st) in enumerate(ENTITIES):
        y=ey0+i*erh
        sel=(st=="sel")
        r_i=0.18+i*0.12; done=t>=r_i
        rrect(d,[lx0,y,lx1,y+erh-8],9,fill=LBLUE if sel else (250,251,253),
              outline=(206,224,250) if sel else LINE,width=1)
        if sel: d.rectangle([S(lx0),S(y+6),S(lx0+3),S(y+erh-14)],fill=BLUE)
        text(d,(lx0+14,y+13),nm+"  "+suf, font(10,True), INK, anchor="lm")
        text(d,(lx0+14,y+27),rlab+" "+reg, font(8,False), SOFT, anchor="lm")
        sxx=lx1-16
        if not done:
            ic_spinner(d,sxx-2,y+(erh-8)/2,6,ang,BLUE,2.0)
        elif sel:
            a=ease_out(seg(t,r_i,0.12))
            pill(d,[lx1-78,y+9,lx1-8,y+erh-19],"3 changes",font(7.5,True),
                 lerp_col((250,251,253),TILE_B,a),lerp_col((250,251,253),BLUE_D,a))
        elif st=="updated":
            ic_check_circle(d,sxx-2,y+(erh-8)/2,6,WHITE,GREEN)
        else:
            d.ellipse([S(sxx-6),S(y+(erh-8)/2-4),S(sxx+2),S(y+(erh-8)/2+4)],fill=AMBER)

    # left footer: continuous auto-sync summary
    lf=seg(t,0.60,0.18)
    if lf>0:
        a=ease_out(lf); fy=312
        hline(d,lx0,lx1,fy-14,LINE)
        d.ellipse([S(lx0+4),S(fy-4),S(lx0+12),S(fy+4)],fill=lerp_col(WHITE,GREEN,a))
        text(d,(lx0+20,fy),"Auto-sync running continuously", font(8.5,True), lerp_col(WHITE,INK,a), anchor="lm")
        text(d,(lx0+4,fy+18),"12 of 12 entities up to date", font(8,False), lerp_col(WHITE,SOFT,a), anchor="lm")

    # ===== right: Change History panel =====
    px0,py0,px1,py1=384,108,604,372
    rrect(d,[px0,py0,px1,py1],11,fill=WHITE,outline=LINE,width=1)
    text(d,(px0+14,py0+15),"Change History", font(10.5,True), INK, anchor="lm")
    ver = "FullSync #154" if t>0.30 else "FullSync #153"
    vbg = TILE_G if t>0.30 else (240,243,248); vfg = GREEN if t>0.30 else SOFT
    tw=text_w(d,ver,font(8,True))
    rrect(d,[px1-tw-26,py0+6,px1-8,py0+24],9,fill=vbg)
    text(d,(px1-tw-16,py0+15),ver,font(8,True),vfg,anchor="lm")
    text(d,(px0+14,py0+31),"into Register Book · from the registry", font(8,False), SOFT, anchor="lm")
    hline(d,px0+12,px1-12,py0+40,LINE)

    chy=py0+56; chh=56
    for k,(field,detail,kind,flag) in enumerate(CHANGES):
        y=chy+k*chh
        r_k=0.30+k*0.16
        ap=seg(t,r_k,0.14)
        if ap<=0: continue
        a=ease_out(ap)
        dotc = GREEN if kind=="auto" else AMBER
        text(d,(px0+16,y+9),field, font(9.5,True), lerp_col(WHITE,INK,a), anchor="lm")
        if flag=="company":
            fw=text_w(d,field,font(9.5,True)); cw=text_w(d,"company-filed",font(7,True))
            rrect(d,[px0+16+fw+8, y+2, px0+16+fw+18+cw, y+16],7,fill=lerp_col(WHITE,TILE_A,a))
            text(d,(px0+16+fw+13,y+9),"company-filed",font(7,True),lerp_col(WHITE,AMBER,a),anchor="lm")
        if kind=="auto":
            ic_check_circle(d,px1-20,y+9,6.5*a+0.01,WHITE,lerp_col(WHITE,GREEN,a))
        else:
            if a>0.4: ic_warn(d,px1-20,y+9,7,lerp_col(WHITE,AMBER,a))
        text(d,(px0+16,y+24),detail, font(8.5,False), lerp_col(WHITE,SOFT,a), anchor="lm")
        if k<len(CHANGES)-1: hline(d,px0+16,px1-14,y+chh-7,(245,247,251))

    # legend: what the two states mean
    lg=seg(t,0.66,0.16)
    if lg>0:
        a=ease_out(lg); lyy=py1-30
        hline(d,px0+12,px1-12,lyy-6,LINE)
        ic_check_circle(d,px0+18,lyy,5.5,WHITE,lerp_col(WHITE,GREEN,a))
        text(d,(px0+30,lyy),"auto-recorded to Register Book", font(7.5,True), lerp_col(WHITE,INK,a), anchor="lm")
        ic_warn(d,px0+19,lyy+15,6,lerp_col(WHITE,AMBER,a))
        text(d,(px0+30,lyy+15),"review, then record manually", font(7.5,True), lerp_col(WHITE,INK,a), anchor="lm")

    return img

def build():
    return [frame(((i/FPS)%DUR)/DUR) for i in range(N)]

if __name__=="__main__":
    fr=build(); save_gif(fr,"t-sync.gif",fps=FPS,colors=128)
    print("done",os.path.getsize("t-sync.gif"))
