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
        self.image = pg.transform.rotozoom(pg.image.load("ex05/fig/maou1.png"), 0, 1)
        self.rect = self.image.get_rect()
        self.rect.center = (1500,450)
        
    def update(self, bg_obj):
        bg_obj.blit(self.image, self.rect)
    

    def change_img(self, num: int, screen: pg.Surface):
        """
        こうかとん画像を切り替え，画面に転送する
        引数1 num：maou画像ファイル名の番号
        引数2 screen：画面Surface
        """
        self.image = pg.transform.rotozoom(pg.image.load(f"ex05/fig/maou{num}.png"), 0, 0.8)
        screen.blit(self.image, self.rect)


class Zako(pg.sprite.Sprite):
    def __init__(self):
        self.image = pg.transform.rotozoom(pg.image.load("ex05/fig/zako1.png"), 0, 0.5)
        self.rect = self.image.get_rect()
        self.rect.center = (100, 450)
        
    def update(self, bg_obj):
        bg_obj.blit(self.image, self.rect)


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


def main():
    pg.display.set_caption("アンチヒーロー")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.transform.rotozoom(pg.image.load("ex05/fig/back.png"), 0, 5)
    
    maou = Maou()
    zako = Zako()
    score = Score()
    level = Level()
        
    tmr = 0
    clock = pg.time.Clock()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
        #for zakos in pg.sprite.groupcollide(zako, beams, True, True).keys():
            #score.score_up(10)  # 10点アップ
        #for yuusya1 in pg.sprite.groupcollide(yuusya, beams, True, True).keys():
            #score.score_up(10)  # 100点アップ"
        if level.level <3: #上限は3レベル
            if score.score > 100:
                score.score -= 100
                level.level_up(1)  # 1レベルアップ
                if level.level == 3:
                    maou.change_img(2, screen)
                    
        screen.blit(bg_img, (0, 0))
        maou.update(screen)
        zako.update(screen)
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
