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
    if obj.top < 0 or HEIGHT < obj.bottom:  # 縦方向のはみ出し 判定
        tate = False
    return yoko, tate
    

class Maou(): #操作キャラクター魔王
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
        self.score = 0
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


class Enemy(pg.sprite.Sprite):
    """
    ザコ敵が出てくるクラス
    """
    def __init__(self, y: int, speed: int, hp: int, size: float, score: int):
        super().__init__()
        self.num = random.randint(1,2) #ザコ敵をランダムに出現させるために使う
        self.image = pg.transform.rotozoom(pg.image.load(f"ex05/fig/zako{self.num}.png"), 0, size)
        self.rect = self.image.get_rect()
        self.rect.center = (100, y)
        self.speed = speed
        self.hp = hp
        self.score = score
        self.atk = 10

    def update(self, score: Score, hp):
        if self.hp <= 0:
            self.kill()
            score.score_up(self.score)
        else:
            self.rect.move_ip(self.speed, 0)
            if self.rect.right >= 1200:
                self.rect.right = 1200
                if self.atk != 0:
                    hp.HP_Down(self.atk)
                    self.atk = 0


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


class HP:
    def __init__(self):
        self.font = pg.font.Font(None, 50)
        self.color = (255,255,0)
        self.HP = 100
        self.image =  self.font.render(f"HP: {self.HP}", 0, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = 800, HEIGHT-50
        
    def HP_Down(self,down):
        self.HP -= down
        
    def update(self, screen: pg.Surface):
        self.image = self.font.render(f"HP: {self.HP}", 0, self.color)
        screen.blit(self.image, self.rect)
        
        
def main():
    pg.display.set_caption("アンチヒーロー")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.transform.rotozoom(pg.image.load("ex05/fig/back.png"), 0, 5)
    maou = Maou()
    score = Score()
    level = Level()
    hp = HP()
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
        for enemy in pg.sprite.groupcollide(enemys, beams, False, True if beamlevel == 1 else False).keys():
            enemy.hp -= 1
            if level.level <3: #上限は3レベル
                if score.score > 100:
                    score.score -= 100
                    level.level_up(1)  # 1レベルアップ
                    hp.HP += 100
                    if level.level == 3:
                        maou.change_img(2, screen)
                        beamlevel = 2
        if hp.HP == 0:
            time.sleep(1)
            break
        screen.blit(bg_img, (0, 0))
        beams.update() 
        beams.draw(screen)
        key_lst = pg.key.get_pressed()
        if tmr % 50 == 0:
            enemys.add(Enemy(random.randint(100, 800), random.randint(5, 15), 1, 0.5, 10)) #ランダムで出現
        if tmr % 100 == 0:
            enemys.add(Enemy(random.randint(100, 800), random.randint(5, 15), 10, 1, 100)) #ランダムで出現
        maou.update(key_lst, screen)
        enemys.update(score, hp)
        enemys.draw(screen)
        score.update(screen)
        level.update(screen)
        hp.update(screen)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
