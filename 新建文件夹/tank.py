import pygame
from pygame.sprite import Sprite
from setting import *

class Tank(Sprite):
    def __init__(self,ai_settings,screen,position):
        """初始化坦克并设置其初始位置"""
        super(Tank,self).__init__()
        self.screen = screen
        self.ai_setting = ai_settings
        #加载坦克图形并获取其外接矩形
        self.image = pygame.image.load()
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #坦克位置设定
        self.rect.centerx = position[0]
        self.rect.bottom = position[1]
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        #初始设定
        self.HP = 1
        self.bullets = []  #子弹列表
        self.tank_direction = DIR_UP
        self.tank_speed_factor = 1  #移动速度
        self.tank_bullet_limit = 1  #最大子弹数
        self.fire_level = 0 #攻击力
        self.is_god = False #是否无敌

        # 移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_dowm = False

    def update(self,map):
        """根据移动标志调整坦克位置"""
        # 更新x,y,需要地图判断能不能走
        if self.moving_up :
            self.tank_direction = DIR_UP
            if self.rect.top > 0:
                self.y -= self.tank_speed_factor

        elif self.moving_dowm :
            self.tank_direction = DIR_DOWN
            if self.rect.bottom < self.screen_rect.bottom:
                self.y += self.tank_speed_factor

        elif self.moving_left :
            self.tank_direction = DIR_LEFT
            if self.rect.left > 0:
                self.x -= self.tank_speed_factor

        elif self.moving_right :
            self.tank_direction = DIR_RIGHT
            if self.rect.right < self.screen_rect.right:
                self.x += self.tank_speed_factor

        self.rect.x = self.x
        self.rect.y = self.y


    def cancel_update(self):
        """取消坦克移动"""
        if self.tank_direction == DIR_UP:
            self.y += self.tank_speed_factor

        elif self.tank_direction == DIR_DOWN:
            self.y -= self.tank_speed_factor

        elif self.tank_direction == DIR_LEFT:
            self.x += self.tank_speed_factor

        elif self.tank_direction == DIR_RIGHT:
            self.x -= self.tank_speed_factor

        self.rect.x = self.x
        self.rect.y = self.y


    def blitme(self):
        """在指定位置绘制坦克"""
        self.screen.blit(self.image,self.rect)


class Enemy(Tank):
    def __init__(self):
        super(Enemy, self).__init__(ai_settings,screen,position)
        self.count = 0 #计算敌人步数，走一定步数后开火一次
        self.attack_frequency = self.ai_setting.attack_frequency #敌人攻击频率


    def attack(self):
        self.count = (self.count + 1) % self.attack_frequency
        if self.count == self.attack_frequency:
            self.bullets.add(Bullet(self.ai_setting, self.screen, self.tank_direction, self.rect))

"""
坦克类增加生命值以及子弹列表？
ai_setting中增加attack_frequency参数，表示敌人攻击频率


坦克基类中新增cancel_update函数，通过外面判断是否碰撞而决定是否调用这个函数
撞墙坦克列表 = pygame.sprite.groupcollide(坦克, 墙, True, False)
    for 坦克 in 撞墙坦克列表:
        取消碰撞
        （如果是玩家坦克：等待下一回输入方向）
        （如果是敌人，随机更改坦克方向）
"""