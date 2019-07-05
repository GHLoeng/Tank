import random
import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group
from bullet import Bullet
from const import *


class Tank(Sprite):
    def __init__(self, screen, tank_path):
        super().__init__()
        self.screen = screen

        self.tank_ful_image = pygame.image.load(tank_path)
        self.image_num = 2
        self.tank_images = [
            self.tank_ful_image.subsurface(pygame.Rect((i * Object_width, 0), (Object_width, Object_width)))
            for i in range(self.image_num)]
        self.tank_image_num = 0
        self.tank_image = self.tank_images[self.tank_image_num]
        self.rect = pygame.Rect(0, 0, Object_width, Object_width)

        self.speed = Tank_speed
        self.x_move = 0
        self.y_move = 0

        self.old_direction = Direction.Stop
        self.new_direction = Direction.Stop
        self.moving = False

        self.hp = 1

        self.bullet_limit = 1
        self.bullets = Group()

    def change_image_direction(self):
        if ((self.old_direction == Direction.Up and self.new_direction == Direction.Down) or
            (self.old_direction == Direction.Down and self.new_direction == Direction.Up) or
            (self.old_direction == Direction.Left and self.new_direction == Direction.Right) or
            (self.old_direction == Direction.Right and self.new_direction == Direction.Left)):
            for i in range(self.image_num):
                self.tank_images[i] = pygame.transform.rotate(self.tank_images[i], 180)

        elif ((self.old_direction == Direction.Up and self.new_direction == Direction.Left) or
              (self.old_direction == Direction.Down and self.new_direction == Direction.Right) or
              (self.old_direction == Direction.Left and self.new_direction == Direction.Down) or
              (self.old_direction == Direction.Right and self.new_direction == Direction.Up)):
            for i in range(self.image_num):
                self.tank_images[i] = pygame.transform.rotate(self.tank_images[i], 90)

        elif ((self.old_direction == Direction.Up and self.new_direction == Direction.Right) or
              (self.old_direction == Direction.Down and self.new_direction == Direction.Left) or
              (self.old_direction == Direction.Left and self.new_direction == Direction.Up) or
              (self.old_direction == Direction.Right and self.new_direction == Direction.Down)):
            for i in range(self.image_num):
                self.tank_images[i] = pygame.transform.rotate(self.tank_images[i], 270)

        self.old_direction = self.new_direction

        self.x_move = 0
        self.y_move = 0

    def check_edge(self):
        if self.rect.y < 0 or \
                self.rect.y + Object_width > Battlefield_width or \
                self.rect.x < 0 or \
                self.rect.x + Object_width > Battlefield_width:
            return False
        return True

    def hit(self):
        self.bullets.empty()
        self.hp -= 1

    def update_tank(self):
        if self.moving:
            if self.new_direction == Direction.Up:
                self.y_move -= self.speed
            elif self.new_direction == Direction.Down:
                self.y_move += self.speed
            elif self.new_direction == Direction.Left:
                self.x_move -= self.speed
            elif self.new_direction == Direction.Right:
                self.x_move += self.speed

            self.rect.x += self.x_move
            self.rect.y += self.y_move

    def update(self):
        self.bullets.update()
        self.update_tank()

    def cancel_update(self):
        self.rect.x -= self.x_move
        self.rect.y -= self.y_move

        self.x_move = 0
        self.y_move = 0

    def draw_bullets(self):
        for bullet in self.bullets:
            bullet.draw()

    def draw_tank(self):
        if self.moving:
            self.tank_image_num += 1
            if self.tank_image_num % self.image_num == 0:
                self.tank_image_num = 0
        self.tank_image = self.tank_images[self.tank_image_num]
        self.screen.blit(self.tank_image, self.rect)


class Player(Tank):
    def __init__(self, screen, player_path):
        super().__init__(screen, player_path)
        self.ful_image = pygame.image.load(Protect_path)
        self.protect_images = [
            self.ful_image.subsurface(pygame.Rect((i * Object_width, 0), (Object_width, Object_width)))
            for i in range(2)]
        self.protect_image_num = 0
        self.protect_image = self.protect_images[self.protect_image_num]
        self.is_protect = True
        self.protect_time = Protect_time

        self.rect.x = Revive_x1
        self.rect.y = Revive_y1

        self.old_direction = Direction.Up
        self.new_direction = Direction.Up

        self.p = 0
        self.level = 1

    def fire(self, music):
        music.play_shoot()

        if self.level >= 3:
            self.bullet_limit = 3

        if len(self.bullets) < self.bullet_limit:
            new_one = Bullet(self.screen, self.rect, self.old_direction)
            if self.level >= 2:
                new_one.speed += Bullet_speed
            if self.level >= 4:
                new_one.power = True
            self.bullets.add(new_one)

    def draw(self):
        self.draw_bullets()

        self.draw_tank()

        if self.is_protect:
            self.protect_image_num += 1
            if self.protect_image_num % 8 == 0:
                self.protect_image_num = 0
            self.protect_time -= 1
            if self.protect_time == 0:
                self.is_protect = False
            self.protect_image = self.protect_images[int(self.protect_image_num / 4)]
            self.screen.blit(self.protect_image, self.rect)


class Player1(Player):
    def __init__(self, screen):
        super().__init__(screen, Player1_path)
        self.p = 1

        self.rect.x = Revive_x1
        self.rect.y = Revive_y1


class Player2(Player):
    def __init__(self, screen):
        super().__init__(screen, Player2_path)
        self.p = 2

        self.rect.x = Revive_x2
        self.rect.y = Revive_y2


class Enemy(Tank):
    def __init__(self, screen, position, enemy_path, is_bonus):
        super().__init__(screen, enemy_path)
        self.twinkle_ful_image = pygame.image.load(Twinkle_path)
        self.twinkle_images = [
            self.twinkle_ful_image.subsurface(pygame.Rect((i * Object_width, 0), (Object_width, Object_width)))
            for i in range(7)]
        self.twinkle_image_num = 0
        self.twinkle_image = self.twinkle_images[self.twinkle_image_num]
        self.is_twinkle = True
        self.twinkle_time = Twinkle_time

        if position == 1:
            self.rect.x = 0
        elif position == 2:
            self.rect.centerx = Battlefield_width / 2
        elif position == 3:
            self.rect.x = Battlefield_width - Object_width
        self.rect.y = 0

        self.old_direction = Direction.Down
        self.new_direction = Direction.Down

        self.step = 0

        self.is_bonus = is_bonus

        self.stop_time = 0

    def fire(self, music):
        if self.moving and len(self.bullets) < self.bullet_limit and self.step % Enemy_fire_frequency == 1:
            self.bullets.add(Bullet(self.screen, self.rect, self.old_direction))
            music.play_shoot()
        self.step += 1

    def change_direction(self):
        direction = random.randint(1, 4)
        if direction == 1:
            self.new_direction = Direction.Up
        elif direction == 2:
            self.new_direction = Direction.Down
        elif direction == 3:
            self.new_direction = Direction.Left
        elif direction == 4:
            self.new_direction = Direction.Right

    def track_player(self, player_x, player_y):
        if self.step % Enemy_change_direction_frequency == 0:
            if random.randint(0, 1) == 1:
                if player_x > self.rect.x:
                    self.new_direction = Direction.Right
                else:
                    self.new_direction = Direction.Left
            else:
                if player_y > self.rect.y:
                    self.new_direction = Direction.Down
                else:
                    self.new_direction = Direction.Up

        self.step += 1

    def draw(self):
        self.draw_bullets()

        if self.is_twinkle:
            self.twinkle_image_num += 1
            if self.twinkle_image_num % 28 == 0:
                self.twinkle_image_num = 0
            self.twinkle_time -= 1
            if self.twinkle_time == 0:
                self.is_twinkle = False
                self.moving = True
            self.twinkle_image = self.twinkle_images[int(self.twinkle_image_num / 4)]
            self.screen.blit(self.twinkle_image, self.rect)
        else:
            if self.stop_time > 0:
                self.moving = False
                self.stop_time -= 1
            else:
                self.moving = True
            self.draw_tank()


class Enemy1(Enemy):
    def __init__(self, screen, position, is_bonus):
        super().__init__(screen, position, Enemy1_path, is_bonus)
        self.type = 1
        self.score = 100

        self.tank_images = [
            self.tank_ful_image.subsurface(pygame.Rect((i * Object_width, 0), (Object_width, Object_width)))
            for i in range(3)]
        if self.is_bonus:
            self.tank_images.pop(0)
        else:
            self.tank_images.pop(2)
        self.tank_image = self.tank_images[self.tank_image_num]

        for i in range(self.image_num):
            self.tank_images[i] = pygame.transform.rotate(self.tank_images[i], 180)


class Enemy2(Enemy):
    def __init__(self, screen, position, is_bonus):
        super().__init__(screen, position, Enemy2_path, is_bonus)
        self.type = 2
        self.speed = Tank_speed * 2
        self.score = 200

        self.tank_images = [
            self.tank_ful_image.subsurface(pygame.Rect((i * Object_width, 0), (Object_width, Object_width)))
            for i in range(3)]
        if self.is_bonus:
            self.tank_images.pop(0)
        else:
            self.tank_images.pop(2)
        self.tank_image = self.tank_images[self.tank_image_num]

        for i in range(self.image_num):
            self.tank_images[i] = pygame.transform.rotate(self.tank_images[i], 180)


class Enemy3(Enemy):
    def __init__(self, screen, position, is_bonus):
        super().__init__(screen, position, Enemy3_path, is_bonus)
        self.type = 3
        self.score = 300

        self.tank_images = [
            self.tank_ful_image.subsurface(pygame.Rect((i * Object_width, 0), (Object_width, Object_width)))
            for i in range(3)]
        if self.is_bonus:
            self.tank_images.pop(0)
        else:
            self.tank_images.pop(2)
        self.tank_image = self.tank_images[self.tank_image_num]

        for i in range(self.image_num):
            self.tank_images[i] = pygame.transform.rotate(self.tank_images[i], 180)

    def fire(self, music):
        if self.moving and len(self.bullets) < self.bullet_limit and self.step % Enemy_fire_frequency == 1:
            new_one = Bullet(self.screen, self.rect, self.old_direction)
            new_one.speed += Bullet_speed
            self.bullets.add(new_one)
            music.play_shoot()
        self.step += 1


class Enemy4(Enemy):
    def __init__(self, screen, position):
        super().__init__(screen, position, Enemy4_path, False)
        self.type = 4
        self.score = 400
        self.hp = 3

        self.tank_images = [
            self.tank_ful_image.subsurface(pygame.Rect((i * Object_width, 0), (Object_width, Object_width)))
            for i in range(7)]
        self.yellow_tank = self.tank_images[:2]
        self.green_tank = self.tank_images[2:4]
        self.grey_tank = self.tank_images[4:6]

        self.tank_images = self.yellow_tank
        for i in range(self.image_num):
            self.tank_images[i] = pygame.transform.rotate(self.tank_images[i], 180)

    def __new_direction(self):
        if self.old_direction == Direction.Down:
            for i in range(self.image_num):
                self.tank_images[i] = pygame.transform.rotate(self.tank_images[i], 180)
        elif self.old_direction == Direction.Left:
            for i in range(self.image_num):
                self.tank_images[i] = pygame.transform.rotate(self.tank_images[i], 90)
        elif self.old_direction == Direction.Right:
            for i in range(self.image_num):
                self.tank_images[i] = pygame.transform.rotate(self.tank_images[i], 270)

        self.tank_image = self.tank_images[self.tank_image_num]

    def kill(self):
        if self.hp == 3:
            self.tank_images = self.green_tank
            self.__new_direction()
        elif self.hp == 2:
            self.tank_images = self.grey_tank
            self.__new_direction()

        self.hp -= 1

    def update(self):
        self.bullets.update()
        self.update_tank()


class TankFactory:
    def __init__(self, screen, enemy_number, is_2p):
        self.screen = screen

        self.player_number = 2 if is_2p else 1
        self.player1_hp = Player_hp
        self.player2_hp = Player_hp
        self.new_one = None
        self.players = Group()
        self.players.add(Player1(self.screen))
        if is_2p:
            self.players.add(Player2(self.screen))

        self.enemy_number = enemy_number
        self.enemies = Group()

        self.enemies.add(Enemy1(self.screen, 1, False))
        self.enemies.add(Enemy1(self.screen, 2, False))
        self.enemies.add(Enemy1(self.screen, 3, False))
        self.enemy_number -= 3
        self.left_number = enemy_number
        self.count = 0

        self.tot_tank_type1 = [0, 0, 0, 0]
        self.tot_tank_type2 = [0, 0, 0, 0]
        
    def create_player(self, p):
        if p == 1 and self.player1_hp > 0:
            self.new_one = Player1(self.screen)
            self.player1_hp -= 1
        elif p == 2 and self.player2_hp > 0:
            self.new_one = Player2(self.screen)
            self.player2_hp -= 1

        if (self.player1_hp > 0 or self.player2_hp > 0) and \
                not pygame.sprite.spritecollide(self.new_one, self.enemies, False) and \
                not pygame.sprite.spritecollide(self.new_one, self.players, False):
            self.players.add(self.new_one)

    def __create_enemy(self):
        self.tank_type = random.randint(0, 10)
        self.position = random.randint(1, 3)

        if int(self.tank_type / 3) == 0:
            self.new_one = Enemy1(self.screen, self.position, (self.tank_type % 3 == 2))
        elif int(self.tank_type / 3) == 1:
            self.new_one = Enemy2(self.screen, self.position, (self.tank_type % 3 == 2))
        elif int(self.tank_type / 3) == 2:
            self.new_one = Enemy3(self.screen, self.position, (self.tank_type % 3 == 2))
        else:
            self.new_one = Enemy4(self.screen, self.position)

        if not pygame.sprite.spritecollide(self.new_one, self.enemies, False) and \
                not pygame.sprite.spritecollide(self.new_one, self.players, False):
            self.enemies.add(self.new_one)
            self.enemy_number -= 1

    def create(self):
        if self.enemy_number > 0:
            if random.randint(0, 1) == 1:
                self.count += 1
                if self.count % Enemy_create_frequency == 0:
                    self.__create_enemy()
                    self.count = 0
            elif self.left_number - self.enemy_number < 3:
                self.__create_enemy()
