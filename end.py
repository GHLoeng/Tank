import pygame
import sys
from pygame.sprite import Sprite
from const import *
class End(Sprite):
    def __init__(self,screen,tank_factory):
        super().__init__()
        self.screen = screen
        self.tank_factory = tank_factory
        self.full_image = pygame.image.load(Full_path)
        self.font = pygame.font.SysFont(None, 36)
        self.font_GameOver = pygame.font.SysFont(None, 50)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.clock = pygame.time.Clock()
        self.brick1_image = self.full_image.subsurface(pygame.Rect((4 * 32 + 8, 3 * 32 + 16), (8, 8)))

    def draw(self,score):
        while True:
            self.screen.fill(Bg_color)
            self.prefstr("Game over", [150, 30], self.red, True)
            self.prefstr("Final Score : ", [50, 80], self.white, False)
            self.prefnum(score, [300, 80], self.white)
            self.prefstr("Press space to restart", [100, 250], self.white, False)
            self.prefstr("Press q to quit", [100, 300], self.white, False)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: return
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

    def draw2p(self,scoreP1,scoreP2):
        while True:
            self.screen.fill(Bg_color)
            self.prefstr("Game over", [150, 30], self.red, True)
            self.prefstr("Player1", [50, 130], self.white, False)
            self.prefstr("Player2", [250, 130], self.white, False)
            self.prefstr("Final Score : ", [50, 80], self.white, False)
            self.prefnum(scoreP1, [50, 180], self.white)
            self.prefnum(scoreP2, [250, 180], self.white)
            self.prefstr("Press space to restart", [100, 250], self.white, False)
            self.prefstr("Press q to quit", [100, 300], self.white, False)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: return
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

    def prefstr(self,text,pos,color,ifOver):
        if ifOver:  self.text_image = self.font_GameOver.render(text, True, color, Bg_color)
        else:  self.text_image = self.font.render(text, True, color, Bg_color)
        self.screen.blit(self.text_image, pos)

    def prefnum(self,num,pos,color):
        self.text = "{:,}".format(num)
        self.text_image = self.font.render(self.text, True, color, Bg_color)
        self.screen.blit(self.text_image, pos)
