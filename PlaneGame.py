# -*- coding:utf-8 -*-
import pygame
from plane_sprites import *

SCREEN_RECT = pygame.Rect(0, 0, 480, 852)
WIDTH = 480
HEIGHT = 852
BAR_LENGTH = 100
BAR_HEIGHT = 10
FRAME_PER_SEC = 60
ENEMY_GAP = 1000
CREATE_ENEMY_EVENT = pygame.USEREVENT
FIRE_EVENT = pygame.USEREVENT + 1
img_dir = path.join(path.dirname(__file__),'images_v2')
sound_folder = path.join(path.dirname(__file__),'sounds')
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
font_name = pygame.font.match_font('Times New Roman')
enemy_bullets = pygame.sprite.Group()
global GAME_STATUS
GAME_STATUS = 1
global END_TIME
END_TIME = 0.0

class Enemy(GameSprite):

    def __init__(self):
        super(Enemy, self).__init__("./images_v2/enemy1.png")
        self.rect.x = random.randint(0, SCREEN_RECT.width - self.rect.width)
        self.rect.bottom = 0
        self.speed = random.uniform(1, 3)
        self.speedx = random.uniform(-1, 1)


    def update(self):
        self.rect.y += self.speed
        self.rect.x += self.speedx
        if (self.rect.y > SCREEN_RECT.height | self.rect.right <= SCREEN_RECT.right | self.rect.left >= SCREEN_RECT.left):
            self.kill()

    def fire(self):
        # 每隔0.5s发射一次子弹，一次3发
            bl1 = Enemy_Bullet(3)
            bl1.rect.bottom = self.rect.y + 20
            bl1.rect.centerx = self.rect.centerx - 0
            enemy_bullets.add(bl1)


class Enemy_Bullet(GameSprite):

    def __init__(self,speed):
        super(Enemy_Bullet, self).__init__("./images_v2/bullet2.png", speed)

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom > SCREEN_RECT.bottom:
            self.kill()


class PlaneGame(object):
    """KlK飞机主游戏"""

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        self.clock = pygame.time.Clock()
        self.score = 0
        self.__create_sprites()
        # 设置定时器事件
        pygame.time.set_timer(CREATE_ENEMY_EVENT, ENEMY_GAP)
        pygame.time.set_timer(FIRE_EVENT, 500)

    def main_menu(self):
        global GAME_STATUS
        GAME_STATUS = 1
        #加载游戏初始界面背景音乐
        menu_song = pygame.mixer.music.load(path.join(sound_folder,"bgMusic_1.mp3"))
        #循环播放
        pygame.mixer.music.play(-1)
        #加载游戏初始界面背景图片
        title = pygame.image.load(path.join(img_dir,"background_2.png")).convert()
        title = pygame.transform.scale(title,(WIDTH, HEIGHT),self.screen)
        self.screen.blit(title,(0,0))
        pygame.display.update()
        #检测玩家操作事件
        while True:
            ev = pygame.event.poll()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN:
                    # pygame.mixer.music.stop()
                    break
            elif ev.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            else:
                self.draw_text("KILL la KILL",40,WIDTH/2, HEIGHT/4,YELLOW)
                self.draw_text("Press [ENTER] To Begin",30,WIDTH/2, HEIGHT/2,RED)
                self.draw_text("Controls:[up] [down] [left] [right]", 30, WIDTH/2, 2*HEIGHT/3,RED)
                self.draw_text("Auto Fire", 30, WIDTH/2, 3*HEIGHT/4,RED)
                pygame.display.update()
        #加载准备声音
        ready = pygame.mixer.Sound(path.join(sound_folder,'getready_2.mp3'))
        ready.play()
        #加载准备开始界面背景颜色和文本
        self.screen.fill(BLACK)
        # self.draw_text(self.screen, "GET READY!", 40, WIDTH/2, HEIGHT/3)
        pygame.display.update()

    # def wait_menu(self):

    #设置文本属性函数
    def draw_text(self,text,size,x,y,color):
        #定义文本参数
        font = pygame.font.Font(font_name,size)
        text_surface = font.render(text,True,color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface,text_rect)


    def __create_sprites(self):

        # 创建背景精灵
        bg1 = BackGround()
        bg2 = BackGround()
        self.back_group = pygame.sprite.Group(bg1, bg2)
        self.enemy_group = pygame.sprite.Group()
        self.enemy = Enemy()
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)
        self.explosion = pygame.sprite.Group()


    def start_game(self):
        bg2 = pygame.mixer.music.load(path.join(sound_folder,"bgMusic_2.mp3"))
        pygame.mixer.music.play(-1)
        while True:
            # 1.设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            # ready = pygame.mixer.Sound(path.join(sound_folder,'bulletFlyMusic.mp3'))
            # ready.play()
            # pygame.mixer.music.pause()
            # 2.事件监听
            self.__event_handler()
            # pygame.mixer.music.unpause()
            # 3.碰撞检测
            self.__check_collide()
            # 4.更新/绘制精灵组
            self.__update_sprites()
            # 5.更新显示
            pygame.display.update()
            if GAME_STATUS==0:
                active = False
                ticks = pygame.time.get_ticks()
                if ticks>END_TIME+1000*2:
                    active = True
                if active:
                    pygame.mixer.music.stop()
                    self.main_menu()
                    self.draw_text("You died!", 30, WIDTH/2, 3*HEIGHT/4,RED)
            # self.draw_text(self.screen,str(self.score),18,WIDTH/2,10)
            # self.draw_shield_bar(5,5,self.hero.shield)

    def __event_handler(self):

        for event in pygame.event.get():
            # 判断是否退出游戏
            if event.type == pygame.QUIT:
                PlaneGame.__quit_game()
            elif event.type == CREATE_ENEMY_EVENT:
                enemy_i = Enemy()
                enemy_i.fire()
                self.enemy_group.add(enemy_i)
            elif event.type == FIRE_EVENT:
                self.hero.fire()

    def __check_collide(self):
        # 子弹与敌机碰撞检测
        # pygame.sprite.groupcollide(self.enemy_group, self.hero.bullets, True, False)
        hits = pygame.sprite.groupcollide(self.enemy_group, self.hero.bullets, True,False)
        for hit in hits:
            self.score += 50
            ready = pygame.mixer.Sound(path.join(sound_folder,'explode.wav'))
            ready.play()
            # random.choice(expl_sounds).play()
            expl = Explosion(hit.rect.center,'enemy')
            self.explosion.add(expl)
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        if len(enemies) > 0:
            self.hero.kill()
            global GAME_STATUS
            GAME_STATUS= 0
            global END_TIME
            END_TIME = pygame.time.get_ticks()
            for ene_i in enemies:
                expl = Explosion(ene_i.rect.center,'hero')
                self.explosion.add(expl)
        enemy_bullets_num = pygame.sprite.spritecollide(self.hero, enemy_bullets, True)
        if len(enemy_bullets_num) > 0:
            self.hero.kill()
            global GAME_STATUS
            GAME_STATUS= 0
            global END_TIME
            END_TIME = pygame.time.get_ticks()
            for ene_i in enemy_bullets_num:
                expl = Explosion(ene_i.rect.center,'hero')
                self.explosion.add(expl)

    def __update_sprites(self):
        self.back_group.update()
        self.back_group.draw(self.screen)
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        enemy_bullets.update()
        enemy_bullets.draw(self.screen)
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        if GAME_STATUS == 1:
            self.hero.bullets.update()
            self.hero.bullets.draw(self.screen)
        self.explosion.update()
        self.explosion.draw(self.screen)
        self.draw_text('Score:'  + str(self.score), 20, WIDTH*4/5, 1*HEIGHT/15,RED)

    @staticmethod
    def __quit_game():
        pygame.quit()
        exit()

if __name__ == '__main__':

    game = PlaneGame()
    game.main_menu()
    game.start_game()
