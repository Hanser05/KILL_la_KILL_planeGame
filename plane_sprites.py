# -*- coding: utf-8 -*-
import pygame
import random
from os import path
SCREEN_RECT = pygame.Rect(0, 0, 480, 852)
img_dir = path.join(path.dirname(__file__),'images_v2')
sound_folder = path.join(path.dirname(__file__),'sounds')
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
#加载爆炸图片
pygame.display.set_mode(SCREEN_RECT.size)
explosion_anim = {}
explosion_anim['hero'] = []
explosion_anim['enemy'] = []
for i in range(1,5):
    #敌机爆炸
    filename = 'enemy1_down{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir,filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['enemy'].append(img)
    #大爆炸
    #img_lg = pygame.transform.scale(img,(75,75))
    #explosion_anim['lg'].append(img_lg)
    #小爆炸
    #img_sm = pygame.transform.scale(img,(32,32))
    #explosion_anim['sm'].append(img_sm)
    #玩家爆炸
    filename = 'hero_blowup_n{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir,filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['hero'].append(img)

class GameSprite(pygame.sprite.Sprite):

    def __init__(self, image_name, speed=1):
        super(GameSprite, self).__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        self.rect.y += self.speed


class BackGround(GameSprite):

    is_alt = 0

    def __init__(self):
        super(BackGround, self).__init__("./images_v2/background_all.png")
        self.rect.y = -(BackGround.is_alt * self.rect.height)
        BackGround.is_alt += 1

    def update(self):
        super(BackGround, self).update()
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Hero(GameSprite):

    # center_h = SCREEN_RECT.centerx
    # bottom_h = SCREEN_RECT.bottom - 120
    def __init__(self):
        super(Hero, self).__init__("./images_v2/hero1.png", 0)
        self.rect.centerx = SCREEN_RECT.centerx
        # self.center_h = self.rect.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120
        # self.bottom_h = self.rect.bottom
        # self.speed = 0 这一步不需要
        self.bullets = pygame.sprite.Group()
        self.shield = 100

    def update(self):
        # 根据上下左右方向键控制英雄移动 水平移动，不能移动出屏幕
        keys_pressed = pygame.key.get_pressed()
        if (keys_pressed[pygame.K_RIGHT] & (self.rect.right <= SCREEN_RECT.right)):
            self.rect.x += 3
        elif (keys_pressed[pygame.K_LEFT] & (self.rect.x >= 0)):
            self.rect.x -= 3
        elif (keys_pressed[pygame.K_UP] & (self.rect.y >= 0)):
            self.rect.y -= 3
        elif (keys_pressed[pygame.K_DOWN] & (self.rect.y <= SCREEN_RECT.bottom-self.rect.height)):
            self.rect.y += 3

    def fire(self):
        # 每隔0.5s发射一次子弹，一次3发
            ready = pygame.mixer.Sound(path.join(sound_folder,'bulletFlyMusic.mp3'))
            ready.play()
            bl1 = Bullet(-2)
            bl1.rect.bottom = self.rect.y - 20
            bl1.rect.centerx = self.rect.centerx - 20
            bl11 = Bullet(-2)
            bl11.rect.bottom = self.rect.y - 40
            bl11.rect.centerx = self.rect.centerx - 20

            bl2 = Bullet(-2)
            bl2.rect.bottom = self.rect.y - 25
            bl2.rect.centerx = self.rect.centerx
            bl22 = Bullet(-2)
            bl22.rect.bottom = self.rect.y - 45
            bl22.rect.centerx = self.rect.centerx

            bl3 = Bullet(-2)
            bl3.rect.bottom = self.rect.y - 20
            bl3.rect.centerx = self.rect.centerx + 20
            bl33 = Bullet(-2)
            bl33.rect.bottom = self.rect.y - 40
            bl33.rect.centerx = self.rect.centerx + 20

            self.bullets.add(bl1, bl2, bl3, bl11, bl22, bl33)
            # pygame.mixer.music.load(path.join(sound_folder,"bulletFlyMusic.mp3"))
            pass


class Bullet(GameSprite):

    def __init__(self,speed):
        super(Bullet, self).__init__("./images_v2/bullet1.png", speed)

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < SCREEN_RECT.y:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    '''创建爆炸类'''
    def __init__(self,center,size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


# if __name__ == "__main__":
#     pygame.init()
#     # 创建游戏窗口
#     screen = pygame.display.set_mode((480, 852))
#
#
#     hero_image = "./images_v2/hero1.png"
#     enemy_image = "./images_v2/enemy1.png"
#
#     background = pygame.image.load("./images_v2/background_3.png")
#     screen.blit(background, (0, 0))
#     hero = GameSprite(hero_image, 10)
#     enemy_1 = GameSprite(enemy_image, 10)
#
#     this_game = pygame.sprite.Group(hero, enemy_1)
#
#     clock = pygame.time.Clock()
#
#     # 游戏循环
#     while True:
#
#         clock.tick(60)
#
#         # 捕获事件
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 exit()
#
#         # 精灵组调用update yu draw
#         this_game.update()
#         screen.blit(background, (0, 0))
#         this_game.draw(screen)
#         pygame.display.update()
#
#
#
#
#     pygame.quit()