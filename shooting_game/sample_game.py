#coding: utf-8

import pygame
from pygame.locals import *
import sys
import numpy as np

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 600
SCREEN_RECT = Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
SHADOW_OFFSET = (10,10)
SHADOW_COLOR = pygame.Color(0,0,0,100)
FLICKER_COLOR = pygame.Color(255,0,0,240)

IMAGE_DIR = "img/"
PLAYER_IMAGE = "jobcrown.png"
ENEMY_IMAGES = (
    "adidas.png",
    "amazon.png",
    "apple.png",
    "burgerking.png",
    "cocacola.png",
    "ebay.png",
    "facebook.png",
    "google.png",
    "hp.png",
    "huawei.png",
    "ibm.png",
    "lego.png",
    "line.png",
    "mcdonalds.png",
    "nasa.png",
    "nike.png",
    "sony.png",
    "starbucks.png",
    "twitter.png",
)
SHOT_IMAGES = (
    "p_shot1.png",
    "p_shot2.png",
    "e_shot1.png",
    "e_shot2.png",
)
COLLAPSE_IMAGE = "explosion.png"
BACKGROUND_IMAGE = "background.png"

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_RECT.size)
    pygame.display.set_caption("がんばれジョブクラウン")
    font = pygame.font.Font(None,60)
    message = "PRESS ENTER KEY"
    gameover_message = "GAME OVER"
    game_state = False

    # スプライトグループを作成して登録
    all_sprite = pygame.sprite.RenderUpdates()
    enemys = pygame.sprite.Group()  # 敵グループ
    player_shots = pygame.sprite.Group()   # プレイヤの弾グループ
    enemy_shots = pygame.sprite.Group()   # 敵の弾グループ
    background = pygame.sprite.Group()   # 背景グループ
    Player.containers = all_sprite
    PlayerShot.containers = all_sprite, player_shots
    Enemy.containers = all_sprite, enemys
    EnemyShot.containers = all_sprite, enemy_shots

    # 画像の読込み
    player_image = make_logo(IMAGE_DIR+PLAYER_IMAGE)
    enemy_images = [make_logo(IMAGE_DIR+img) for img in ENEMY_IMAGES]
    shot_images = [load_image(IMAGE_DIR+img) for img in SHOT_IMAGES]

    # スプライトの画像を登録
    Background.image = load_image(IMAGE_DIR+BACKGROUND_IMAGE)
    back_rect = Background.image.get_rect()
    PlayerShot.image = shot_images[1]
    EnemyShot.image = shot_images[2]

    BkgSprite1 = Background(0,-Background.image.get_size()[1])
    BkgSprite2 = Background(0,0)
    background.add(BkgSprite1)
    background.add(BkgSprite2)

    clock = pygame.time.Clock()
    while True:
        # ゲーム開始時、ゲームオーバー時の画面
        while not game_state:
            text_width, text_height = font.size(message)
            text = font.render(message, True, (255,255,255))
            BkgSprite2.draw(screen)
            screen.blit(text,(int((WINDOW_WIDTH-text_width)/2),int((WINDOW_HEIGHT-text_height)/2)))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_RETURN:
                    game_state = True
                    player = Player(player_image)
                    for i in range(0, 10):
                        x = 20 + (i % 10) * 40
                        y = 20 + (i - 25) * (i - 25) / 3
                        Enemy((enemy_images[np.random.randint(len(enemy_images))]),(x,y))

        # 敵を全部倒したらおかわり
        if len(enemys.sprites()) <= 0:
            for i in range(0, 10):
                x = 20 + (i % 10) * 40
                y = 20 + (i - 25) * (i - 25) / 3
                Enemy((enemy_images[np.random.randint(len(enemy_images))]),(x,y))

        # ゲームオーバー時
        if not player.alive():
            message = gameover_message
            [sprite.kill() for sprite in enemys.sprites()]
            [sprite.kill() for sprite in enemy_shots.sprites()]
            [sprite.kill() for sprite in player_shots.sprites()]
            game_state = False

        clock.tick(60)
        all_sprite.update()

        # 衝突判定
        collision_detection(player, enemys, player_shots, enemy_shots)

        background.update()
        BkgSprite1.draw(screen)
        BkgSprite2.draw(screen)
        all_sprite.draw(screen)
        pygame.display.update()

        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

def collision_detection(player, enemys, player_shots, enemy_shots):
    """衝突判定"""
    # 敵と弾の衝突判定
    enemy_collided = pygame.sprite.groupcollide(enemys, player_shots, False, True)
    enemy_collided.update(pygame.sprite.groupcollide(enemys, enemy_shots, False, True))
    for enemy in list(enemy_collided.keys()):
        if not enemy.damaged:
            enemy.damage()
  
    # プレイヤーと弾の衝突判定
    beam_collided = pygame.sprite.spritecollide(player, enemy_shots, True)
    if beam_collided and not player.damaged:
        player.damage()

    # 弾同士の衝突判定
    shot_collided = pygame.sprite.groupcollide(enemy_shots, player_shots, True, True)


class Company(pygame.sprite.Sprite):
    """ プレイヤーと敵の親クラス """
    def __init__(self, logo):
        super().__init__(self.containers)
        self.logo = logo
        self.image = self.logo[0]["surface"]
        self.rect = self.logo[0]["rect"]
        self.life = 0
        self.speed = 0
        self.collapse_flame = 30
        self.damage_flame = 20
        self.damaged = False

    def damage(self):
        self.life -= 1
        self.damaged = True

    def collapse(self):
        self.image = load_image(IMAGE_DIR+COLLAPSE_IMAGE)
        self.speed = 0
        self.collapse_flame -= 1
        if self.collapse_flame <= 0:
            self.kill()

    def update(self):
        if self.damaged:
            self.damage_flame -= 1
            self.image = self.logo[self.damage_flame%2]["surface"]
            if self.damage_flame <= 0:
                self.image = self.logo[0]["surface"]
                self.damaged = False

        if self.life <= 0:
            self.collapse()

class Player(Company):
    """自機"""
    def __init__(self,logo):
        super().__init__(logo)
        self.life = 3
        self.speed = 5  # 移動速度
        self.reload_time = 15  # リロード時間

        self.rect.bottom = SCREEN_RECT.bottom  # プレイヤーが画面の一番下
        self.reload_timer = 0

    def update(self):
        super().update()
        # 押されているキーをチェック
        pressed_keys = pygame.key.get_pressed()
        # 押されているキーに応じてプレイヤーを移動
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        elif pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        elif pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.speed)
        elif pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.speed)
        self.rect.clamp_ip(SCREEN_RECT)
        # 弾の発射
        if pressed_keys[K_SPACE]:
            # リロード時間が0になるまで再発射できない
            if self.reload_timer > 0:
                # リロード中
                self.reload_timer -= 1
            else:
                # 発射！！！
                PlayerShot(self.rect.midtop)  # 作成すると同時にallに追加される
                PlayerShot(self.rect.midtop,deg=10)  # 作成すると同時にallに追加される
                PlayerShot(self.rect.midtop,deg=-10)  # 作成すると同時にallに追加される
                self.reload_timer = self.reload_time

class Enemy(Company):
    """敵"""
    def __init__(self,logo,pos):
        super().__init__(logo)
        self.life = 5
        self.speed = 2
        self.prob_beam = 0.0105  # 弾を発射する確率
        self.forward_frame = np.random.randint(10,50)   # 出現してから直進するフレーム数

        self.rect.midtop = ((np.random.randint(80,SCREEN_RECT.width-80),0))
    def update(self):
        super().update()

        if not self.damaged:
            if self.forward_frame > 0:
                self.forward_frame -= 1
                self.rect.move_ip(0,np.random.randint(4))
            else:
                if np.random.randint(0,10) >= 8:
                    self.rect.move_ip(np.random.randint(-6,8), np.random.randint(-4,4))
                # 弾を発射
                if np.random.random() < self.prob_beam:
                    EnemyShot(self.rect.midbottom)
                    EnemyShot(self.rect.midbottom,deg=20)
                    EnemyShot(self.rect.midbottom,deg=-20)

        if self.rect.top < 0 or self.rect.bottom > SCREEN_RECT.height or self.rect.right < 0 or self.rect.left > SCREEN_RECT.width:
            self.kill()

class Shot(pygame.sprite.Sprite):
    """ 弾の親クラス """
    def __init__(self, deg):
        # imageとcontainersはmain()でセット
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.speed = 0
        self.direction = 0
        self.deg = deg

    def update(self):
        self.rect.move_ip(
            self.direction*self.speed*np.sin(np.radians(self.deg)),
            self.direction*self.speed*np.cos(np.radians(self.deg))
        )  # 上へ移動

        if self.rect.top < 0 or self.rect.bottom > SCREEN_RECT.height:  # 上端または下端に達したら除去
            self.kill()

class PlayerShot(Shot):
    """ プレイヤーの弾 """
    def __init__(self, pos, deg=0):
        super().__init__(deg)
        self.rect.midbottom = pos # Shotの出現位置
        self.speed = 6
        self.direction = -1

class EnemyShot(Shot):
    """ 敵の弾 """
    def __init__(self, pos, deg=0):
        super().__init__(deg)
        self.rect.midtop = pos # Shotの出現位置
        self.speed = 5
        self.direction = 1

class Background(pygame.sprite.Sprite):
    x = 0
    y = 0
    scroll_speed = 1
    def __init__(self, x=0,y=0):
        super(Background,self).__init__()
        self.x=x
        self.y=y
        
        self.rect = self.image.get_rect()

    def scroll(self,speed):
        self.y+=(speed)
        if self.y>self.image.get_size()[1]:
            self.y=-self.image.get_size()[1]

    def update(self):
        self.scroll(self.scroll_speed)
    
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

def load_image(filename, colorkey=None):
    """画像をロードして画像と矩形を返す"""
    try:
        image = pygame.image.load(filename)
    except pygame.error as message:
        print("Cannot load image:", filename)
        raise SystemExit(message)
    image = image.convert_alpha()
    return image

def set_alpha(surface, color, offset=(0,0), back=False):
    """ 
        surfaceに対してアルファチャンネル指定の塗りつぶし領域を重ねます
        offsetでオフセット指定、back=Trueで背面に配置
    """
    alpha = surface.copy()
    fill(alpha, color)

    image_rect = surface.get_rect()
    alpha_rect = alpha.get_rect()
    alpha_rect.center = image_rect.center
    alpha_rect.move_ip(offset)

    union_rect = image_rect.union(alpha_rect)
    new_surface = pygame.Surface(union_rect.size, pygame.SRCALPHA)

    args=[(surface,(0,0)),(alpha,offset)]
    if back: args.reverse()
    list(new_surface.blit(arg[0],arg[1]) for arg in args)
    # list(map(new_surface.blit,args))
    # if back:
        # new_surface.blit(alpha, offset)
        # new_surface.blit(surface, (0,0))
    # else:
        # new_surface.blit(surface, (0,0))
        # new_surface.blit(alpha, offset)

    return {"surface":new_surface, "rect":image_rect}

def fill(surface, color):
    """ surfaceを塗りつぶす """
    w,h = surface.get_size()
    r,g,b,a = color
    for x in range(w):
        for y in range(h):
            new_alpha = surface.get_at((x,y))[3] and a
            surface.set_at((x,y), pygame.Color(r,g,b,new_alpha))

def make_logo(filename):
    image = load_image(filename)
    flicker_image = set_alpha(image.copy(),FLICKER_COLOR)["surface"]
    logo_images = []
    logo_images.append(set_alpha(image,SHADOW_COLOR,SHADOW_OFFSET,True))
    logo_images.append(set_alpha(flicker_image,SHADOW_COLOR,SHADOW_OFFSET,True))
    return logo_images

if __name__ == "__main__":
    main()