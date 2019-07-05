import pygame
from pygame.sprite import Sprite

"""
settings:需要用子弹颜色、大小、速度
screen:屏幕
tank:需要用坦克方向   上下左右0123？

子弹为矩形
"""
class Bullet(Sprite):
    def __init__(self, ai_settings, screen, tank_dir, tank_tect):
        super().__init__()
        self.screen = screen
        self.ai_setting = ai_settings

        self.color = ai_settings.bullet_color
        self.direction = tank_dir
        self.speed = ai_settings.bullet_speed
        self.tank_ract = tank_tect

        self.rect = pygame.Rect(0, 0, self.ai_setting.bullet_width, self.ai_setting.bullet_height)
        if self.direction == 0:
            self.rect = pygame.Rect(0, 0, self.ai_setting.bullet_width, self.ai_setting.bullet_height)
            self.rect.centerx = self.tank_ract.centerx
            self.rect.top = self.tank_ract.top
        elif self.direction == 1:
            self.rect = pygame.Rect(0, 0, self.ai_setting.bullet_width, self.ai_setting.bullet_height)
            self.rect.centerx = self.tank_ract.centerx
            self.rect.bottom = self.tank_ract.bottom
        elif self.direction == 2:
            self.rect = pygame.Rect(0, 0, self.ai_setting.bullet_height, self.ai_setting.bullet_width)
            self.rect.centery = self.tank_ract.centery
            self.rect.left = self.tank_ract.left
        elif self.direction == 3:
            self.rect = pygame.Rect(0, 0, self.ai_setting.bullet_height, self.ai_setting.bullet_width)
            self.rect.centery = self.tank_ract.centery
            self.rect.right = self.tank_ract.right

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)


    def update(self):
        if (self.direction == 0) and (map.if_crash(self.x, self.y - self.speed)):
            self.y -= self.speed
        elif (self.direction == 1) and (map.if_crash(self.x, self.y + self.speed)):
            self.y += self.speed
        elif (self.direction == 2) and (map.if_crash(self.x - self.speed, self.y)):
            self.x -= self.speed
        elif (self.direction == 3) and (map.if_crash(self.x - self.speed, self.y)):
            self.x += self.speed
        self.rect.x = self.x
        self.rect.y = self.y


    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


"""
map:地图，int二维数组，0表可穿透，1表不可
"""
class Map():
    def __init__(self, map):
        self.map = map

    def if_crash(self, new_x, new_y):
        return map[new_x][new_y] == 1