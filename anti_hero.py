import math
import random
import sys
import time

import pygame as pg

WIDTH = 1600  # ゲームウィンドウの幅
HEIGHT = 900  # ゲームウィンドウの高さ

#enemy_y_list = [100 + i * 200 for i in range(4)]

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
    bg_img = pg.transform.rotozoom(pg.image.load("fig/back.png"), 0, 5)
    
    maou = Maou()
    enemys = pg.sprite.Group()
    
    tmr = 0
    clock = pg.time.Clock()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
        key_lst = pg.key.get_pressed()
        if tmr % 50 == 0:
            enemys.add(Zako(random.randint(100, 800), random.randint(5, 15)))

        screen.blit(bg_img, (0, 0))
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
