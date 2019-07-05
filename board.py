import pygame
from pygame.sprite import Sprite
from const import *
class Board(Sprite):
    def __init__(self, screen, tank_factory, is_2p, game_level):
        super().__init__()
        self.screen = screen
        self.tank_factory = tank_factory
        self.is_2p = is_2p
        self.full_image = pygame.image.load(Full_path)
        self.enemy_image = self.full_image.subsurface(pygame.Rect((4*32+16, 3*32+16), (16, 16)))
        self.IP_image = self.full_image.subsurface(pygame.Rect((5*32, 3*32+16), (32, 32)))
        self.IIP_image = self.full_image.subsurface(pygame.Rect((6*32, 3*32+16), (32, 32)))
        self.flag_image = self.full_image.subsurface(pygame.Rect((6*32, 1*32), (32, 32)))
        self.text_color = (0,0,0)
        self.tbg_color = (128,128,128)
        self.font = pygame.font.SysFont(None, 32)
        self.game_level = game_level

    def draw(self):
        pygame.draw.rect(self.screen,(128,128,128),(Battlefield_width,0,Screen_width-Battlefield_width,Screen_height))
        for idx in range(self.tank_factory.left_number): #剩余坦克数
            self.screen.blit(self.enemy_image,[((27+idx%2)*16), ((idx//2)*16)])
        #玩家1P生命
        self.screen.blit(self.IP_image,[432, 206])
        IP_HP = "{:,}".format(self.tank_factory.player1_hp)
        self.IP_HP_image = self.font.render(IP_HP,True,self.text_color,self.tbg_color)
        self.screen.blit(self.IP_HP_image,[432+16,206+16])
        #玩家2P生命
        if self.is_2p:
            self.screen.blit(self.IIP_image, [432, 206+48])
            IIP_HP = "{:,}".format(self.tank_factory.player2_hp)
            self.IIP_HP_image = self.font.render(IIP_HP, True, self.text_color, self.tbg_color)
            self.screen.blit(self.IIP_HP_image, [432+16, 206+64])

        #关卡
        self.screen.blit(self.flag_image,[432, 206+96])
        map = "{:,}".format(self.game_level)
        self.map_image = self.font.render(map, True, self.text_color, self.tbg_color)
        self.screen.blit(self.map_image, [432+32, 206+96])