import pygame
import sys
from tank import TankFactory
from map import Map
from game_music import GameMusic
from board import Board
import game_functions as gf
from start import Start
from end import End
from const import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((Screen_width, Screen_height))
        pygame.display.set_caption(Game_name)

        self.clock = None
        self.music = None
        self.game_state = None
        self.is_2p = None
        self.score = None
        self.scoreP1 = None
        self.scoreP2 = None
        self.turnScore = None
        self.game_map = None
        self.tank_factory = None
        self.board = None
        self.game_level = 1
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.font = pygame.font.SysFont(None, 36)
        self.full_image = pygame.image.load(Full_path)
        self.tank_image = []
        self.enemy_num = [0, 0, 0, 0]
        self.enemy_score = [100, 200, 300, 400]
        tank_Ypos = 6
        while tank_Ypos <= 9:
            self.tank_image.append(self.full_image.subsurface(pygame.Rect((1*32, tank_Ypos*32), (32, 32))))
            tank_Ypos = tank_Ypos + 1

    def Start_menu(self):
        self.start_menu = Start(self.screen)
        self.game_level = 1
        self.is_2p = self.start_menu.draw()

    def prefstr(self,text,pos,color):
        self.text_image = self.font.render(text, True, color, Bg_color)
        self.screen.blit(self.text_image, pos)

    def prefnum(self,num,pos,color):
        self.text = "{:,}".format(num)
        self.text_image = self.font.render(self.text, True, color, Bg_color)
        self.screen.blit(self.text_image, pos)

    def draw_score_p1(self):
        while True:
            self.screen.fill(Bg_color)
            self.prefstr("Total Score : ", [50, 40], self.white)
            self.prefnum(self.score, [300, 40], self.red)
            self.prefstr("Score : ", [50, 80], self.white)
            self.prefnum(self.score, [300, 80], self.white)
            tank_num = 0
            while tank_num <= 3:
                self.screen.blit(self.tank_image[tank_num], [50, 120 + tank_num * 50])
                self.prefnum(self.tank_factory.tot_tank_type1[tank_num], [180, 130 + tank_num * 50], self.white)
                self.prefnum(self.tank_factory.tot_tank_type1[tank_num]*self.enemy_score[tank_num], [300, 130 + tank_num * 50], self.white)
                tank_num = tank_num + 1
            self.prefstr("Press space to continue", [100, 350], self.white)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: return

    def draw_score_p2(self):
        score1, score2, count = 0, 0, 0
        while count <= 3:
            score1 += self.tank_factory.tot_tank_type1[count] * self.enemy_score[count]
            score2 += self.tank_factory.tot_tank_type2[count] * self.enemy_score[count]
            count += 1
        self.scoreP1 += score1
        self.scoreP2 += score2
        while True:
            self.screen.fill(Bg_color)
            self.prefstr("Player 1", [200, 5], self.white)
            self.prefstr("Player 2", [300, 5], self.white)
            self.prefstr("Total Score : ", [50, 40], self.white)
            self.prefnum(self.scoreP1, [250, 40], self.red)
            self.prefnum(self.scoreP2, [350, 40], self.red)
            self.prefstr("Score : ", [50, 80], self.white)
            self.prefnum(score1, [250, 80], self.white)
            self.prefnum(score2, [350, 80], self.white)
            tank_num = 0
            while tank_num <= 3:
                self.screen.blit(self.tank_image[tank_num], [220, 120 + tank_num * 50])
                self.prefnum(self.tank_factory.tot_tank_type1[tank_num], \
                             [150, 130 + tank_num * 50], self.white)
                self.prefnum(self.tank_factory.tot_tank_type1[tank_num]*\
                             self.enemy_score[tank_num], [50, 130 + tank_num * 50], self.white)
                self.prefnum(self.tank_factory.tot_tank_type2[tank_num], \
                             [310, 130 + tank_num * 50], self.white)
                self.prefnum(self.tank_factory.tot_tank_type2[tank_num]*\
                             self.enemy_score[tank_num], [390, 130 + tank_num * 50], self.white)
                tank_num = tank_num + 1
            self.prefstr("Press space to continue", [100, 350], self.white)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: return

    def initialize(self):
        self.clock = pygame.time.Clock()
        self.music = GameMusic()
        self.game_state = State.Ok
        self.game_map = Map(self.screen, self.game_level)
        self.tank_factory = TankFactory(self.screen, Enemy_number, self.is_2p)
        self.board = Board(self.screen,self.tank_factory,self.is_2p, self.game_level)

    def start(self):
        self.music.play_game_start()
        self.score, self.scoreP1, self.scoreP2 = 0, 0, 0
        while self.game_state == State.Ok:
            self.clock.tick(Clock_frequency)

            self.tank_factory.create()

            gf.check_events(self.tank_factory, self.music)
            self.turnScore = gf.update_screen(self.screen, self.game_map, self.tank_factory, self.music, self.board)
            self.score += self.turnScore
            gf.draw_screen(self.screen, self.game_map, self.tank_factory, self.board)
            
            self.game_state = gf.check_win(self.game_map, self.tank_factory)
            if self.game_state == State.Success:
                self.game_level += 1
                if self.game_level > Max_level:
                    self.game_level = 1
                    break
                else:
                    if self.game_level >=2:
                        if self.is_2p:  self.draw_score_p2()
                        else:  self.draw_score_p1()
                    self.initialize()
                    self.game_state = State.Ok

        self.game_level = 1
        self.music.play_game_over()
        score1, score2, count = 0, 0, 0
        while count <= 3:
            score1 += self.tank_factory.tot_tank_type1[count] * self.enemy_score[count]
            score2 += self.tank_factory.tot_tank_type2[count] * self.enemy_score[count]
            count += 1
        self.scoreP1 += score1
        self.scoreP2 += score2
        self.end_menu = End(self.screen,self.tank_factory)
        if self.is_2p:  self.end_menu.draw2p(self.scoreP1, self.scoreP2)
        else:  self.end_menu.draw(self.score)
