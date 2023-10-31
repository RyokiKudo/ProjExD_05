import math
import random
import sys
import time

import pygame as pg

WIDTH = 1600  # ゲームウィンドウの幅
HEIGHT = 900  # ゲームウィンドウの高さ

def check_bound(obj: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内か画面外かを判定し，真理値タプルを返す
    引数 obj：オブジェクト（爆弾，こうかとん，ビーム）SurfaceのRect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if obj.left < 0 or WIDTH < obj.right:  # 横方向のはみ出し判定
        yoko = False
    if obj.top < 0 or HEIGHT < obj.bottom:  # 縦方向のはみ出し判定
        tate = False
    return yoko, tate

class Maou(pg.sprite.Sprite):
    def __init__(self):
        
        self.image = pg.transform.rotozoom(pg.image.load(f"fig/maou1.png"), 0, 0)
        
    def update(self, bg_obj):
        bg_obj.blit(self.image, (1500,450))

class Zako(pg.sprite.Sprite):
    def __init__(self):
        
        self.image = pg.transform.rotozoom(pg.image.load(f"fig/zako1.png"), 0, 0)
        
    def update(self, bg_obj):
        bg_obj.blit(self.image, (100,450))
        

def main():
    pg.display.set_caption("アンチヒーロー")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/back.png")
    screen.blit(bg_img, (0, 0))
    
    maou = Maou()
    zako = Zako()
    
    tmr = 0
    clock = pg.time.Clock()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
        maou.update(screen)
        zako.update(screen)
        pg.display.update()
        tmr += 1
        clock.tick(50)
        
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
