import math
import random
import sys
import time

import pygame as pg
from pygame.sprite import AbstractGroup

WIDTH = 1600  # ゲームウィンドウの幅
HEIGHT = 900  # ゲームウィンドウの高さ

def check_bound(obj: pg.Rect) -> tuple[bool, bool]:
    
    yoko, tate = True, True
    if obj.left < 0 or WIDTH < obj.right:  # 横方向のはみ出し判定
        yoko = False
    if obj.top < 0 or HEIGHT < obj.bottom:  # 縦方向のはみ出し判定
        tate = False
    return yoko, tate



class Maou(pg.sprite.Sprite):
    """ 
    魔王
    """
    def __init__(self):
        self.image = pg.transform.rotozoom(pg.image.load("ex05/fig/maou1.png"), 0, 0.5)
        self.rect = self.image.get_rect()
        self.rect.center = (1500, 450)

    def update(self, bg_obj):
        bg_obj.blit(self.image, self.rect)


class Zako(pg.sprite.Sprite):
    """
    ザコ
    """
    def __init__(self):
        self.image = pg.transform.rotozoom(pg.image.load("ex05/fig/zako1.png"), 0, 0.5)
        self.rect = self.image.get_rect()
        self.rect.center = (100, 450)

    def update(self, bg_obj):
        bg_obj.blit(self.image, self.rect)        


class Beam(pg.sprite.Sprite):
    """
        魔王が出すビームに関するクラス
    """
    def __init__(self, maou: Maou):
        super().__init__()
        self.image = pg.transform.rotozoom(pg.image.load("ex05/fig/beam.png"),0,0.5)
        self.rect = self.image.get_rect()
        self.rect.left = maou.rect.left  
        self.rect.centery = maou.rect.centery 
        self.vx, self.vy = -10, 0

    def update(self): 
        self.rect.move_ip(self.vx, self.vy)
        if check_bound(self.rect) != (True, True):
            self.kill()


def main():
    pg.display.set_caption("アンチヒーロー")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.transform.rotozoom(pg.image.load("ex05/fig/back.png"), 0, 5)
    maou = Maou()
    zako = Zako()
    beams = pg.sprite.Group()
    tmr = 0
    clock = pg.time.Clock()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                beams.add(Beam(maou))
        
        screen.blit(bg_img, (0, 0))
        maou.update(screen)
        zako.update(screen)
        beams.update() 
        beams.draw(screen)
        pg.display.update()
        tmr += 1
        clock.tick(50)
        
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
