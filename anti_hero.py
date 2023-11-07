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
    if obj.left < 0 :  # 横方向のはみ出し判定
        yoko = False
    if obj.top < 0 or HEIGHT < obj.bottom:  # 縦方向のはみ出し判定
        tate = False
    return yoko, tate


class Maou():
    def __init__(self):
        self.image = pg.transform.rotozoom(pg.image.load("ex05/fig/maou1.png"), 0, 0.5)
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
        
    def change_img(self, num: int, screen: pg.Surface):
        """
        魔王の画像を第2形態に替える
        """
        self.image = pg.transform.rotozoom(pg.image.load(f"ex05/fig/maou{num}.png"), 0, 0.8)
        screen.blit(self.image, self.rect)

        
class Score:
    """
    倒した敵の数をスコアとして表示するクラス
    ザコ:10点
    勇者：500点
    """
    def __init__(self):
        self.font = pg.font.Font(None, 50)
        self.color = (0,255,0)
        self.score = 400
        self.image =  self.font.render(f"Score: {self.score}", 0, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = 100, HEIGHT-50

    def score_up(self, add):
        self.score += add

    def update(self, screen: pg.Surface):
        self.image = self.font.render(f"Score: {self.score}", 0, self.color)
        screen.blit(self.image, self.rect)


class Level:
    """
    スコアに応じてレベルが変化するクラス
    """
    def __init__(self):
        self.font = pg.font.Font(None, 50)
        self.color = (255,255,0)
        self.level = 1
        self.image =  self.font.render(f"Level: {self.level}", 0, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH-200, HEIGHT-50
    
    def level_up(self, up):
        self.level += up

    def update(self, screen: pg.Surface):
        self.image = self.font.render(f"Level: {self.level}", 0, self.color)
        screen.blit(self.image, self.rect)
        
        
class Zako(pg.sprite.Sprite):
    def __init__(self, y: int, speed: int):
        super().__init__()
        self.num = random.randint(1,2)
        self.image = pg.transform.rotozoom(pg.image.load(f"ex05/fig/zako{self.num}.png"), 0, 0.5)
        self.rect = self.image.get_rect()
        self.rect.center = (100, y)
        self.speed = speed

    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.right >= 1400:
            self.rect.right = 1400

class Beam(pg.sprite.Sprite):
    """
        魔王が出すビームに関するクラス
    """
    def __init__(self, maou: Maou, num:int):
        super().__init__()
        self.image = pg.transform.rotozoom(pg.image.load(f"ex05/fig/beam{num}.png"),0,0.5)
        self.rect = self.image.get_rect()
        self.rect.left = maou.rect.left  
        self.rect.centery = maou.rect.centery
        self.vx, self.vy = -20, 0

    def update(self): 
        self.rect.move_ip(self.vx, self.vy)
        if check_bound(self.rect) != (True, True):
            self.kill()

    # def beam_change_img(self, num: int, screen: pg.Surface):
    #     """
    #     ビームを第2形態に替える
    #     """
    #     self.image = pg.transform.rotozoom(pg.image.load(f"ex05/fig/beam{num}.png"), 0, 0.8)
    #     screen.blit(self.image, self.rect)
 
def main():
    pg.display.set_caption("アンチヒーロー")
    screen = pg.display.set_mode((WIDTH, HEIGHT))

    bg_img = pg.transform.rotozoom(pg.image.load("ex05/fig/back.png"), 0, 5)
    maou = Maou()
    score = Score()
    level = Level()
    beams = pg.sprite.Group()
    enemys = pg.sprite.Group()
    beamlevel = 1
    
    tmr = 0
    clock = pg.time.Clock()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0

            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                beams.add(Beam(maou,beamlevel))
      
        for zakos in pg.sprite.groupcollide(enemys, beams, True, True if beamlevel == 1 else False).keys(): #zakoをenemysに変えたら、動くかも
            #score.score_up(10)  # 10点アップ
        #for yuusya1 in pg.sprite.groupcollide(yuusya, beams, True, True).keys():
            #score.score_up(10)  # 100点アップ"
            if level.level <3: #上限は3レベル
                if score.score > 100:
                    score.score -= 100
                    level.level_up(1)  # 1レベルアップ
                    if level.level == 3:
                        maou.change_img(2, screen)
                        beamlevel = 2
        
        screen.blit(bg_img, (0, 0))
        beams.update() 
        beams.draw(screen)
        key_lst = pg.key.get_pressed()
        if tmr % 50 == 0:
            enemys.add(Zako(random.randint(100, 800), random.randint(5, 15)))
        maou.update(key_lst, screen)
        enemys.update()
        enemys.draw(screen)

        score.update(screen)
        level.update(screen)
        
        pg.display.update()
        tmr += 1
        clock.tick(50)
        
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
