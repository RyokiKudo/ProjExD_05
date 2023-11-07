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
    """
    プレイアブルとなる魔王のクラス
    """
    def __init__(self):
        """
        イニシャライザの定義
        """
        self.image = pg.transform.rotozoom(pg.image.load("fig/maou1.png"), 0, 0.5)  #魔王の画像を縮小して格納
        self.rect = self.image.get_rect()   #魔王の画像のrectを取得し格納
        self.rect.center = (1500, 450)  #魔王の初期位置を指定

    def update(self, key_list, bg_obj: pg.Surface):
        """
        魔王の状態を更新する
        移動の処理
        """
        move_val = 0    #移動量となる変数
        if key_list[pg.K_UP]:   #上キーが押されていた場合、移動量を-1
            move_val += -1
        if key_list[pg.K_DOWN]: #下キーが押されていた場合、移動量を+1
            move_val += 1
        self.rect.move_ip(0, move_val * 10) #移動量*10だけ移動
        if not check_bound(self.rect)[1]:   #上下の壁に接触した場合、移動をキャンセル
            self.rect.move_ip(0 ,-move_val * 10)
        bg_obj.blit(self.image, self.rect)  #魔王をblit
        
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
    敵キャラのクラス
    """
    def __init__(self, y: int, speed: int, hp: int, size: float, score: int):   #敵の出現位置、移動速度、サイズ, 倒した際の取得スコアを引数として受け取る
        """
        イニシャライザ
        """
        super().__init__()
        self.num = random.randint(1,2) #ザコ敵をランダムに出現させるために使う
        self.image = pg.transform.rotozoom(pg.image.load(f"ex05/fig/zako{self.num}.png"), 0, size)  #敵の画像のrectを取得し格納
        self.rect = self.image.get_rect()   #画像のrectを取得
        self.rect.center = (100, y) #敵の出現位置を決定
        self.speed = speed  #敵の移動速度を格納
        self.hp = hp    #敵の初期HPを設定
        self.score = score  #取得スコアを格納
        self.atk = 10   #攻撃力を設定

    def update(self, score: Score, hp):
        """
        敵の状態を更新する
        HP管理
        移動
        """
        if self.hp <= 0:    #残りHPが0になったら削除し、スコアを追加
            self.kill()
            score.score_up(self.score)
        else:
            self.rect.move_ip(self.speed, 0)    #横方向へ移動
            if self.rect.right >= 1200: #一定の位置へ移動したらその位置で移動を終了
                self.rect.right = 1200
                if self.atk != 0:   #攻撃力ぶんのダメージを1度だけ与える
                    hp.HP_Down(self.atk)
                    self.atk = 0


class Beam(pg.sprite.Sprite):
    """
        魔王が出すビームに関するクラス
    """
    def __init__(self, maou: Maou, num:int):
        super().__init__()
        self.image = pg.transform.rotozoom(pg.image.load(f"ex05/fig/beam{num}.png"),0,0.5)    #進化した際に画像を変更させるために指定できるようにしている
        self.rect = self.image.get_rect()
        self.rect.left = maou.rect.left  
        self.rect.centery = maou.rect.centery
        self.vx, self.vy = -20, 0       #ビームの速度

    def update(self): 
        self.rect.move_ip(self.vx, self.vy)
        if check_bound(self.rect) != (True, True):
            self.kill()    #画面端で消えるようにしている


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
    maou = Maou()   #魔王インスタンス
    score = Score()
    level = Level()
    hp = HP()
    beams = pg.sprite.Group()
    enemys = pg.sprite.Group()  #敵グループ
    beamlevel = 1
    tmr = 0
    clock = pg.time.Clock()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:    #シフトキーでビームが出るようにしている
                beams.add(Beam(maou,beamlevel))
        for enemy in pg.sprite.groupcollide(enemys, beams, False, True if beamlevel == 1 else False).keys():    #敵とビームの衝突判定
            enemy.hp -= 1   #衝突した敵のHPを-1
            if level.level <3: #上限は3レベル
                if score.score > 100:
                    score.score -= 100
                    level.level_up(1)  # 1レベルアップ
                    hp.HP += 100
                    if level.level == 3:
                        maou.change_img(2, screen)
                        beamlevel = 2    #魔王が進化したら、ビームも進化する
        if hp.HP == 0:
            time.sleep(1)
            break
        screen.blit(bg_img, (0, 0))
        beams.update() 
        beams.draw(screen)
        key_lst = pg.key.get_pressed()
        if tmr % 50 == 0:   #1秒ごとに雑魚敵を出現
            enemys.add(Enemy(random.randint(100, 800), random.randint(5, 15), 1, 0.5, 10))  #ランダムで出現
        if tmr % 100 == 0:  #2秒ごとに強敵を出現
            enemys.add(Enemy(random.randint(100, 800), random.randint(5, 15), 10, 1, 100))  #ランダムで出現
        maou.update(key_lst, screen)    #魔王の状態を更新
        enemys.update(score, hp)    #敵の状態を更新
        enemys.draw(screen) #敵の描画
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
