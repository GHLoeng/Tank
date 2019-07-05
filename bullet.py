import pygame
from pygame.sprite import Sprite
from const import *


class Bullet(Sprite):
    def __init__(self, screen, tank_rect, tank_direction):
        super().__init__()
        self.screen = screen

        self.image = pygame.image.load(Bullet_path)
        self.rect = self.image.get_rect()
        self.rect.centerx = float(tank_rect.centerx)
        self.rect.centery = float(tank_rect.centery)

        self.direction = tank_direction
        self.speed = Bullet_speed

        self.power = False

        self.__change_image_direction()

    def __change_image_direction(self):
        if self.direction == Direction.Down:
            self.image = pygame.transform.rotate(self.image, 180)
        elif self.direction == Direction.Left:
            self.image = pygame.transform.rotate(self.image, 90)
        elif self.direction == Direction.Right:
            self.image = pygame.transform.rotate(self.image, 270)

    def check_edge(self):
        if self.rect.centery < 0 or \
                self.rect.centery > Battlefield_width or \
                self.rect.centerx < 0 or \
                self.rect.centerx > Battlefield_width:
            return True
        return False

    def update(self):
        if self.direction == Direction.Up:
            self.rect.centery -= self.speed
        elif self.direction == Direction.Down:
            self.rect.centery += self.speed
        elif self.direction == Direction.Left:
            self.rect.centerx -= self.speed
        elif self.direction == Direction.Right:
            self.rect.centerx += self.speed

    def draw(self):
        self.screen.blit(self.image, self.rect)
