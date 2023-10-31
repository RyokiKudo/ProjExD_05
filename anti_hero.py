import math
import random
import sys
import time

import pygame as pg
from pygame.sprite import AbstractGroup

WIDTH = 1600  # ゲームウィンドウの幅
HEIGHT = 900  # ゲームウィンドウの高さ

#enemy_y_list = [100 + i * 200 for i in range(4)]

def check_bound(obj: pg.Rect) -> tuple[bool, bool]:
    
    yoko, tate = True, True
    if obj.left < 0 or WIDTH < obj.right:  # 横方向のはみ出し判定
        yoko = False
    if obj.top < 0 or HEIGHT < obj.bottom:  # 縦方向のはみ出し判定
        tate = False
    return yoko, tate

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
        # screen.blit(self.img, self.rect)
        
        
class Maou():
    def __init__(self):
        self.image = pg.transform.rotozoom(pg.image.load("fig/maou1.png"), 0, 0.5)
        self.rect = self.image.get_rect()
        self.rect.center = (1500, 450)

    def update(self, key_list, bg_obj: pg.Surface):
        move_val = 0
        if key_list[pg.K_UP]:
            move_val += -1
        if key_list[pg.K_DOWN]:
            move_val += 1
        self.rect.move_ip(0, move_val * 10)
        if not check_bound(self.rect)[1]:
            self.rect.move_ip(0 ,-move_val * 10)
        bg_obj.blit(self.image, self.rect)

        
class Zako(pg.sprite.Sprite):
    def __init__(self, y: int, speed: int):
        super().__init__()
        self.image = pg.transform.rotozoom(pg.image.load("fig/zako1.png"), 0, 0.5)
        self.rect = self.image.get_rect()
        self.rect.center = (100, y)
        self.speed = speed

    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.right >= 1400:
            self.rect.right = 1400

def main():
    pg.display.set_caption("アンチヒーロー")
    screen = pg.display.set_mode((WIDTH, HEIGHT))

    bg_img = pg.transform.rotozoom(pg.image.load("ex05/fig/back.png"), 0, 5)
    maou = Maou()
    beams = pg.sprite.Group()
    enemys = pg.sprite.Group()
    
    tmr = 0
    clock = pg.time.Clock()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                beams.add(Beam(maou))
        screen.blit(bg_img, (0, 0))
        beams.update() 
        beams.draw(screen)
        key_lst = pg.key.get_pressed()
        if tmr % 50 == 0:
            enemys.add(Zako(random.randint(100, 800), random.randint(5, 15)))
        maou.update(key_lst, screen)
        enemys.update()
        enemys.draw(screen)

        pg.display.update()
        tmr += 1
        clock.tick(50)
        
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
