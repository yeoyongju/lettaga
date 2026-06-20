"""T-Drive — every signed & filed doc auto-saved to each entity's drive."""
from studio import *
from PIL import Image, ImageDraw

DUR=3.8; FPS=12.5
N=int(DUR*FPS)

EXIST=[("Constitution.pdf","2.1 MB"),
       ("Register Book.pdf","1.4 MB")]
INCOMING=[("Signed Resolution.pdf","from T-Sign",GREEN,0.18),
          ("AR Certificate.pdf","from e-Filing",BLUE,0.46)]

def frame(t):
    img,d=base_window("lettaga · T-Drive", full=True)
    text(d,(34,62),"Apex Ventures · T-Drive", font(12.5,True), INK, anchor="lm")
    # capacity + search
    rrect(d,[430,54,540,76],11,fill=(244,247,251))
    ic_search(d,446,65,6,SOFT,2)
    text(d,(458,65),"Search", font(8.5,False), SOFT, anchor="lm")
    rrect(d,[548,54,602,76],11,fill=LBLUE)
    text(d,(575,65),"100 GB", font(8.5,True), BLUE, anchor="mm")

    # ===== folder column =====
    fx0,fy0,fx1=34,84,168
    folders=[("Documents", True), ("Privacy", False), ("Transactions", False)]
    made=sum(1 for _,_,_,tt in INCOMING if t>=tt+0.30)
    counts=[4+made, 2, 6]
    for i,(nm,sel) in enumerate(folders):
        y=fy0+i*46
        rrect(d,[fx0,y,fx1,y+38],9,fill=LBLUE if sel else (250,251,253),
              outline=(206,224,250) if sel else LINE,width=1)
        ic_folder(d,fx0+18,y+19,7,BLUE if sel else SOFT)
        text(d,(fx0+32,y+14),nm, font(9.5,True), INK if sel else SOFT, anchor="lm")
        # count badge
        cb=str(counts[i])
        bump = pulse(t, [0.48,0,0][i] if i==0 else 0, 0.2) if i==0 else 0
        rrect(d,[fx1-26,y+8,fx1-8,y+24],8,fill=BLUE if sel else (224,230,240))
        text(d,(fx1-17,y+16),cb, font(8,True), WHITE if sel else SOFT, anchor="mm")
    # storage gauge under folders
    gy=fy0+3*46+18
    text(d,(fx0,gy),"Storage", font(8,True), SOFT, anchor="lm")
    text(d,(fx1,gy),"33 / 100 GB", font(7.5,False), SOFT, anchor="rm")
    rrect(d,[fx0,gy+10,fx1,gy+18],4,fill=(232,238,246))
    rrect(d,[fx0,gy+10,fx0+(fx1-fx0)*0.33,gy+18],4,fill=BLUE)
    text(d,(fx0,gy+34),"Per-entity drive", font(8,True), INK, anchor="lm")
    text(d,(fx0,gy+50),"Documents · Privacy · Transactions", font(7.5,False), SOFT, anchor="lm")

    # ===== file list =====
    lx0,ly0,lx1,ly1=182,84,602,376
    rrect(d,[lx0,ly0,lx1,ly1],10,fill=(250,251,254),outline=LINE,width=1)
    text(d,(lx0+16,ly0+18),"Documents", font(10,True), INK, anchor="lm")
    text(d,(lx1-16,ly0+18),"drag & drop · auto-saved", font(8,False), SOFT, anchor="rm")
    hline(d,lx0+12,lx1-12,ly0+30,LINE)

    # build current list: existing + incoming(after they land)
    rows=list(EXIST)
    landed=[]
    for nm,src,col,tt in INCOMING:
        if t>=tt+0.30: landed.append((nm,src,col))
    allrows = landed + rows  # newest on top
    ry=ly0+40; rh=50
    for i,row in enumerate(allrows):
        y=ry+i*rh
        nm=row[0]; isnew=len(row)==3
        a = ease_out(seg(t,0,0.1))
        rrect(d,[lx0+12,y,lx1-12,y+rh-8],8,fill=WHITE,outline=LINE,width=1)
        ic_doc(d,lx0+30,y+(rh-8)/2,9,fill=(row[2] if isnew else SOFT),line=WHITE)
        text(d,(lx0+50,y+11),nm, font(10,True), INK, anchor="lm")
        sub = row[1] if isnew else "—"
        text(d,(lx0+50,y+24),(row[1] if isnew else EXIST[i-len(landed)][1]), font(8,False), SOFT, anchor="lm")
        if isnew:
            pill(d,[lx1-150,y+8,lx1-58,y+rh-18],"auto-saved",font(7.5,True),TILE_G,GREEN)
            ic_check_circle(d,lx1-44,y+(rh-8)/2,6,WHITE,GREEN)

    # flying doc chips from top-right into list
    for nm,src,col,tt in INCOMING:
        fly=seg(t,tt,0.28)
        if 0<fly<1:
            p=ease_io(fly)
            sx,sy=lx1-40, ly0-2
            ex,ey=lx0+30, ry+ (rh-8)/2
            cx=lerp(sx,ex,p); cy=lerp(sy,ey,p)
            rrect(d,[cx-66,cy-12,cx+66,cy+12],7,fill=WHITE,outline=col,width=1)
            ic_doc(d,cx-52,cy,7,fill=col,line=WHITE)
            text(d,(cx-40,cy),src, font(8,True), col, anchor="lm")

    return img

def build():
    return [frame(((i/FPS)%DUR)/DUR) for i in range(N)]

if __name__=="__main__":
    fr=build(); save_gif(fr,"t-drive.gif",fps=FPS,colors=128)
    print("done",os.path.getsize("t-drive.gif"))
