import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group
from const import *


class Block(Sprite):
    def __init__(self, screen, wall_path, x, y):
        super().__init__()
        self.screen = screen

        self.image = pygame.image.load(wall_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        self.screen.blit(self.image, self.rect)


class Score(Block):
    def __init__(self, screen, score, x, y):
        super().__init__(screen, Score_path, x, y)
        self.score = score

        self.ful_image = pygame.image.load(Score_path)
        self.images1 = [
            self.ful_image.subsurface(pygame.Rect((i * Object_width, 0), (Object_width, Wall_width)))
            for i in range(3)]
        self.images2 = [
            self.ful_image.subsurface(pygame.Rect((i * Object_width, Wall_width), (Object_width, Wall_width)))
            for i in range(2)]

        if self.score % 200:
            self.image = self.images1[int(self.score / 200)]
        else:
            self.image = self.images2[int(self.score / 200 - 1)]
        self.score_last_time = Score_last_time
        self.explosion_time = Explosion_time

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def draw(self):
        if self.explosion_time > 0:
            self.explosion_time -= 1
        if self.explosion_time == 0 and self.score_last_time != 0:
            self.score_last_time -= 1
            self.screen.blit(self.image, self.rect)


class Bonus(Block):
    def __init__(self, screen, bonus_type, x, y):
        super().__init__(screen, Bonus_path, x, y)
        self.type = bonus_type

        self.ful_image = pygame.image.load(Bonus_path)
        self.images = [
            self.ful_image.subsurface(pygame.Rect((i * Object_width, 0), (Object_width, Object_width)))
            for i in range(6)]

        self.image = self.images[self.type]
        self.bonus_last_time = Bonus_last_time

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def draw(self):
        self.bonus_last_time -= 1
        if 300 < self.bonus_last_time < Bonus_last_time:
            self.screen.blit(self.image, self.rect)
        elif 200 < self.bonus_last_time <= 300 and int(self.bonus_last_time / 20) % 2 != 0:
            self.screen.blit(self.image, self.rect)
        elif 100 < self.bonus_last_time <= 200 and int(self.bonus_last_time / 10) % 2 != 0:
            self.screen.blit(self.image, self.rect)
        elif 0 < self.bonus_last_time <= 100 and int(self.bonus_last_time / 5) % 2 != 0:
            self.screen.blit(self.image, self.rect)


class Explosion(Block):
    def __init__(self, screen, x, y):
        super().__init__(screen, Explosion_path, x, y)

        self.ful_image = pygame.image.load(Explosion_path)
        self.explosion_images = [
            self.ful_image.subsurface(pygame.Rect((i * Object_width, 0), (Object_width, Object_width)))
            for i in range(5)]
        self.explosion_image_num = 0
        self.explosion_image = self.explosion_images[self.explosion_image_num]
        self.explosion_time = Explosion_time

        self.rect = self.explosion_image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def draw(self):
        if self.explosion_time > 0:
            self.explosion_time -= 1
            self.explosion_image_num += 1
            if self.explosion_image_num % 25 == 0:
                self.explosion_image_num = 0
            self.explosion_image = self.explosion_images[int(self.explosion_image_num / 5)]
            self.screen.blit(self.explosion_image, self.rect)


class Base(Block):
    def __init__(self, screen, x, y):
        super().__init__(screen, Base_path, x, y)
        self.hp = 1

        self.ful_image = pygame.image.load(Base_path)
        self.base_images = [self.ful_image.subsurface(pygame.Rect((i * Object_width, 0), (Object_width, Object_width)))
                            for i in range(2)]
        self.base_image = self.base_images[0]
        self.explosion_time = Explosion_time

        self.rect = self.base_image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        if self.hp == 0 and self.explosion_time > 0:
            self.explosion_time -= 1
            self.base_image = self.base_images[1]
        self.screen.blit(self.base_image, self.rect)


class Brick(Block):
    def __init__(self, screen, x, y):
        super().__init__(screen, Brick_path, x, y)
        self.hp = 1


class Grass(Block):
    def __init__(self, screen, x, y):
        super().__init__(screen, Grass_path, x, y)
        self.hp = 0


class Steel(Block):
    def __init__(self, screen, x, y):
        super().__init__(screen, Steel_path, x, y)
        self.hp = -1


class Map:
    def __init__(self, screen, game_level):
        self.screen = screen

        self.map = []
        self.blocks = Group()
        self.protect_wall = Group()
        self.temp_wall = Group()
        self.temp_wall.empty()
        self.grass = Group()
        self.base = None
        self.explosion = Group()
        self.bonus = Group()
        self.score = Group()
        self.map_level = game_level

        self.protect = 0

        self.__get_map_path()
        self.__get_map()
        self.__get_protect()

    def __get_map(self):
        with open(self.map_path) as file_object:
            self.map = file_object.readlines()

        x, y = 0, 0
        for i in range(len(self.map)):
            for j in range(len(self.map[i]) - 1):
                if self.map[i][j] == '1':
                    self.blocks.add(Brick(self.screen, x, y))
                elif self.map[i][j] == '2':
                    self.grass.add(Grass(self.screen, x, y))
                elif self.map[i][j] == '3':
                    self.blocks.add(Steel(self.screen, x, y))
                elif self.map[i][j] == '4' and self.map[i-1][j] != '4' and self.map[i][j-1] != '4':
                    self.base = Base(self.screen, x, y)
                x += Wall_width
            x = 0
            y += Wall_width

    def __get_protect(self):
        for i in range(8):
            self.protect_wall.add(Steel(self.screen, Base_protect[i][0], Base_protect[i][1]))

    def __set_protect(self):
        for block in self.blocks.sprites():
            if (block.rect.x, block.rect.y) in Base_protect:
                self.temp_wall.add(block)
                self.blocks.remove(block)
        for block in self.protect_wall:
            self.blocks.add(block)

    def __cancel_protect(self):
        for block in self.blocks.sprites():
            if (block.rect.x, block.rect.y) in Base_protect:
                self.blocks.remove(block)
        for block in self.temp_wall:
            self.blocks.add(block)
        self.temp_wall.empty()

    def draw_block(self):
        if self.protect == Protect_time and not self.temp_wall.sprites():
            self.__set_protect()
            self.protect -= 1
        elif self.protect == 0 and self.temp_wall.sprites():
            self.__cancel_protect()
        elif 0 < self.protect < Protect_time:
            self.protect -= 1

        for block in self.blocks:
            block.draw()

        for explosion in self.explosion:
            explosion.draw()

        self.base.draw()

    def draw_grass(self):
        for block in self.grass:
            block.draw()

        for bonus in self.bonus:
            bonus.draw()

        for score in self.score:
            score.draw()

    def __get_map_path(self):
        temp_list = list(Map_path)
        temp_list.insert(10, str(self.map_level))
        self.map_path = "".join(temp_list)