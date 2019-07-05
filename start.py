import pygame
import sys
from pygame.sprite import Sprite
from const import *
class Start(Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.is_2p = False
        self.white = (255,255,255)
        self.clock = pygame.time.Clock()
        self.full_image = pygame.image.load(Full_path)
        self.font = pygame.font.SysFont(None, 36)
        self.brick1_image = self.full_image.subsurface(pygame.Rect((4*32+8, 3*32+16), (8, 8)))
        self.brick2_image = self.full_image.subsurface(pygame.Rect((4*32+8, 3*32+24), (8, 8)))
        self.tank_image = self.full_image.subsurface(pygame.Rect((1*32, 5*32), (32, 32)))
        self.tank_image = pygame.transform.rotate(self.tank_image,-90)



    def draw(self):
        self.screen.fill(Bg_color)

        for y in range(len(title)):
            line = title[y]
            for x in range(len(line)):
                if line[x] == 'X':
                    self.screen.blit((self.brick1_image, self.brick2_image)[x % 2], [(x+6)*8, (y+9)*8])

        # 显示一个黄坦克和玩家1、2的文字
        self.pref("1 PLAYER", [204, 271], self.white)
        self.pref("2 PLAYERS", [204, 309], self.white)
        self.pos = [164,264+int(self.is_2p)*42]
        self.screen.blit(self.tank_image,self.pos)
        nose = pygame.Surface([32,32])
        while True:
            self.clock.tick(40)
            self.screen.blit(nose, self.pos)
            self.pos = [164, 264 + int(self.is_2p) * 42]
            self.screen.blit(self.tank_image, self.pos)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.is_2p = True
                    elif event.key == pygame.K_UP:
                        self.is_2p = False
                    elif event.key == pygame.K_ESCAPE:
                        sys.exit()
                    elif event.key == pygame.K_SPACE:
                        return self.is_2p
            pygame.display.update()

    def pref(self,text,pos,color):
        self.text_image = self.font.render(text, True, color, Bg_color)
        self.screen.blit(self.text_image, pos)

'''开头'''
title  = (
        'XXXXXX....XXX....XXXXXX..XXXXXX.XX......XXXXXXX.',
        'XX...XX..XX.XX.....XX......XX...XX......XX......',
        'XX...XX.XX...XX....XX......XX...XX......XX......',
        'XXXXXX..XXXXXXX....XX......XX...XX......XXXXXX..',
        'XX...XX.XX...XX....XX......XX...XX......XX......',
        'XX...XX.XX...XX....XX......XX...XX......XX......',
        'XXXXXX..XX...XX....XX......XX...XXXXXXX.XXXXXXX.',
        '................................................',
        '................................................',
        '................................................',
        '............XXXX...XXXXXX..XXXXXX.XX..XX........',
        '...........XX..XX....XX......XX...XX..XX........',
        '..........XX.........XX......XX...XX..XX........',
        '..........XX.........XX......XX....XXXX.........',
        '..........XX.........XX......XX.....XX..........',
        '...........XX..XX....XX......XX.....XX..........',
        '............XXXX...XXXXXX....XX.....XX..........')
