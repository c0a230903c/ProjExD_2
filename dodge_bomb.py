import os
import random
import sys
import pygame as pg
import time


WIDTH, HEIGHT = 1600, 900
DELTA={
    pg.K_UP:(0,-5),   #こうかとんのキーを押したときの移動値
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0)
}

TORI_HOUKOU={
    (0,-5):()
}
arcs=[a for a in range(1, 11)]
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def gameover():
    """
   こうかとんが爆弾にあたった時のゲームオーバー処理、
   戻り値："Game Over"といも文字列を返す
   """
    font=pg.font.Font(None,240)
    txt=font.render("Game Over",True,(255,255,255))
    return txt


def check_bound(obj_rct:pg.Rect) -> tuple[bool,bool]:
    """
    こうかとんRect、または、爆弾Rectの画面内外判定用の関数
    引数：こうかとんRect、または、爆弾Rect
    戻り値：横方向判定結果、縦方向判定結果（True：画面内/False：画面外）
    """
    yoko,tate=True,True
    if obj_rct.left<0 or WIDTH<obj_rct.right:
        yoko=False
    if obj_rct.top<0 or HEIGHT<obj_rct.bottom:
        tate=False
    return yoko,tate


def tuiju():
    for r in range(1, 11):
       bb_img = pg.Surface((20*r, 20*r))
       pg.draw.circle(bb_img,(255,0,0),(10*r,10*r),10*r)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bd_img=pg.Surface((20,20))
    bd_img.set_colorkey((0,0,0))
    pg.draw.circle(bd_img,(255,0,0),(10,10),10)
    pienton = pg.image.load("fig/8.png")
    bd_rct=bd_img.get_rect()
    bd_rct.center=random.randint(0,WIDTH),random.randint(0,HEIGHT)
    vx,vy=+5,+5
    txt=gameover()
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img,(255,0,0),(10*r,10*r),10*r)

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bd_rct):
            screen.blit(txt,[350,350])
            bout = pg.Surface((1600,900))
            pg.draw.rect(bout,(0,0,0),(0,0,1600,900) #画面を覆う黒い四角を作成
            bout.set_alpha(200)
            screen.blit(bout, [0,0])  #ゲームオーバー時に画面が暗くなる
            screen.blit(pienton, [300,400])
            screen.blit(pienton, [1270,400])
            pg.display.update()
            time.sleep(5)
            return 
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for a,b in DELTA.items():
            if key_lst[a]:
                sum_mv[0]+=b[0]
                sum_mv[1]+=b[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct)!=(True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bd_rct.move_ip(vx,vy)
        screen.blit(bd_img, bd_rct)
        yoko,tate =check_bound(bd_rct)
        if not yoko:  
            vx*=-1
        if not tate:  
            vy*=-1
        pg.display.update()
        tmr+=1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
