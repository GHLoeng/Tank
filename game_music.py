import pygame
from const import *


class GameMusic:
    def __init__(self):
        self.add_life = pygame.mixer.Sound(Add_life)
        self.add_score = pygame.mixer.Sound(Add_score)
        self.game_over = pygame.mixer.Sound(Game_over)
        self.game_pause = pygame.mixer.Sound(Game_pause)
        self.game_start = pygame.mixer.Sound(Game_start)
        self.get_props = pygame.mixer.Sound(Get_props)
        self.hit_border = pygame.mixer.Sound(Hit_border)
        self.hit_brick = pygame.mixer.Sound(Hit_brick)
        self.hit_kill = pygame.mixer.Sound(Hit_kill)
        self.hit_special = pygame.mixer.Sound(Hit_special)
        self.hit_steel = pygame.mixer.Sound(Hit_steel)
        self.inc_score = pygame.mixer.Sound(Inc_score)
        self.shoot = pygame.mixer.Sound(Shoot)
        self.speed_normal = pygame.mixer.Sound(Speed_normal)
        self.speed_up = pygame.mixer.Sound(Speed_up)

    def play_add_life(self):
        self.add_life.play()

    def play_add_score(self):  # ?
        self.add_score.play()

    def play_game_over(self):
        pygame.mixer.music.load(Game_over)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

    def play_game_pause(self):  # ?
        self.game_pause.play()

    def play_game_start(self):
        self.game_start.play()

    def play_get_props(self):
        self.get_props.play()

    def play_hit_border(self):
        self.hit_border.play()

    def play_hit_brick(self):
        self.hit_brick.play()

    def play_hit_kill(self):
        self.hit_kill.play()

    def play_hit_special(self):
        self.hit_special.play()

    def play_hit_steel(self):
        self.hit_steel.play()

    def play_inc_score(self):  # ?
        self.inc_score.play()

    def play_shoot(self):
        self.shoot.play()

    def play_speed_normal(self):  # ?
        self.speed_normal.play()

    def play_speed_up(self):  # ?
        self.speed_up.play()
