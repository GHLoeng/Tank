import sys
import random
import pygame
from map import Explosion, Bonus, Score
from const import *


"""按键检测"""
def check_keydown_events(event, players, music):
    if event.key == pygame.K_ESCAPE:
        sys.exit()
    for player in players:
        if player.p == 2:
            if event.key == pygame.K_UP:
                player.moving = True
                player.new_direction = Direction.Up
            elif event.key == pygame.K_DOWN:
                player.moving = True
                player.new_direction = Direction.Down
            elif event.key == pygame.K_LEFT:
                player.moving = True
                player.new_direction = Direction.Left
            elif event.key == pygame.K_RIGHT:
                player.moving = True
                player.new_direction = Direction.Right

            if event.key == pygame.K_k:
                player.fire(music)

        elif player.p == 1:
            if event.key == pygame.K_w:
                player.moving = True
                player.new_direction = Direction.Up
            elif event.key == pygame.K_s:
                player.moving = True
                player.new_direction = Direction.Down
            elif event.key == pygame.K_a:
                player.moving = True
                player.new_direction = Direction.Left
            elif event.key == pygame.K_d:
                player.moving = True
                player.new_direction = Direction.Right

            if event.key == pygame.K_SPACE:
                player.fire(music)


def check_keyup_events(event, players):
    for player in players:
        if player.p == 2:
            if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                player.moving = False
        elif player.p == 1:
            if event.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]:
                player.moving = False


def check_events(tank_factory, music):
    players = tank_factory.players
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, players, music)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, players)


"""碰撞检测"""
def check_tank_collide1(tank1, tank2):
    return not pygame.sprite.collide_rect(tank1, tank2)


def check_tank_collide2(tank, tanks):
    return not pygame.sprite.spritecollide(tank, tanks, False)


def check_tank_block_collide(game_map, tank):
    return not pygame.sprite.spritecollide(tank, game_map.blocks, False) and \
           not pygame.sprite.collide_rect(tank, game_map.base)


def check_player_bonus_collide(game_map, tank_factory, music):
    players = tank_factory.players
    enemies = tank_factory.enemies

    score = 0
    for player in players:
        hit = pygame.sprite.spritecollide(player, game_map.bonus, True)
        for bonus in hit:
            if bonus.type == 0:  # 铲子
                game_map.protect = Protect_time
            elif bonus.type == 1:  # 星星
                player.level += 1
                music.play_get_props()
            elif bonus.type == 2:  # 时钟
                for enemy in enemies:
                    enemy.stop_time = Stop_time
            elif bonus.type == 3:  # 钢盔
                player.is_protect = True
                player.protect_time = Protect_time
            elif bonus.type == 4:  # 手榴弹
                for enemy in enemies:
                    enemy.hp = 0
                score += 500
            elif bonus.type == 5:  # 战车
                if player.p == 1:
                    tank_factory.player1_hp += 1
                elif player.p == 2:
                    tank_factory.player2_hp += 1
                music.play_add_life()

    return score


def check_bullet_edge(screen, game_map, bullets, music):
    for bullet in bullets:
        if bullet.check_edge():
            game_map.explosion.add(Explosion(screen, bullet.rect.centerx, bullet.rect.centery))
            bullets.remove(bullet)
            music.play_hit_border()


def check_bullet_collide(bullets1, bullets2):
    pygame.sprite.groupcollide(bullets1, bullets2, True, True)


def check_bullet_block_collide(game_map, bullets):
    hit = pygame.sprite.groupcollide(bullets, game_map.blocks, True, False)
    for bullet, blocks in hit.items():
        for block in blocks:
            if bullet.power:
                block.hp = 0
            else:
                block.hp -= 1

    hit = pygame.sprite.spritecollide(game_map.base, bullets, True)
    if hit and game_map.base.hp != 0:
        game_map.base.hp -= 1


def check_bullet_tank_collide(tank_factory):
    players = tank_factory.players
    enemies = tank_factory.enemies

    for player in players:
        for enemy in enemies:
            hit_enemy = pygame.sprite.spritecollide(enemy, player.bullets, True)
            hit_player = pygame.sprite.spritecollide(player, enemy.bullets, True)
            if hit_enemy:
                if enemy.type == 4 and enemy.hp > 1:
                    enemy.kill()
                else:
                    enemy.hit()
                    if player.p == 1:
                        tank_factory.tot_tank_type1[enemy.type - 1] += 1
                    if player.p == 2:
                        tank_factory.tot_tank_type2[enemy.type - 1] += 1
            if hit_player and not player.is_protect:
                player.hit()

    if len(players) == 2:
        pygame.sprite.spritecollide(players.sprites()[0], players.sprites()[1].bullets, True)
        pygame.sprite.spritecollide(players.sprites()[1], players.sprites()[0].bullets, True)


"""更新屏幕"""
def check_win(game_map, tank_factory):
    if game_map.base.explosion_time == 0 or \
            (tank_factory.player1_hp == 0 and tank_factory.player_number == 1) or \
            (tank_factory.player1_hp == 0 and tank_factory.player2_hp == 0 and tank_factory.player_number == 2):
        return State.Failure
    if tank_factory.left_number == 0:
        return State.Success
    return State.Ok


def update_player(screen, game_map, players, enemies, music):
    for player in players:
        player.update()
        flag = player.check_edge() and \
                check_tank_block_collide(game_map, player) and \
                check_tank_collide2(player, enemies)
        if len(players) == 2:
            flag = flag and check_tank_collide1(players.sprites()[0], players.sprites()[1])


        if flag:
            player.change_image_direction()
        else:
            player.cancel_update()
        check_bullet_edge(screen, game_map, player.bullets, music)
        for enemy in enemies:
            check_bullet_collide(player.bullets, enemy.bullets)
        check_bullet_block_collide(game_map, player.bullets)


def update_enemy(screen, game_map, players, enemies, music):
    for enemy in enemies:
        for player in players:
            enemy.track_player(player.rect.x, player.rect.y)
        enemy.update()

        flag = enemy.check_edge() and check_tank_block_collide(game_map, enemy)
        for player in players:
            flag = flag and check_tank_collide1(player, enemy)

        for tank in enemies:
            if tank is not enemy:
                check_bullet_collide(tank.bullets, enemy.bullets)
                pygame.sprite.spritecollide(tank, enemy.bullets, True)
                flag = flag and check_tank_collide1(tank, enemy)
        if flag:
            enemy.change_image_direction()
        else:
            enemy.cancel_update()
            enemy.change_direction()

        enemy.fire(music)
        check_bullet_edge(screen, game_map, enemy.bullets, music)
        check_bullet_block_collide(game_map, enemy.bullets)


def update_tank_factory(screen, game_map, tank_factory, music):
    score = 0
    players = tank_factory.players
    enemies = tank_factory.enemies

    update_player(screen, game_map, players, enemies, music)
    update_enemy(screen, game_map, players, enemies, music)

    score += check_player_bonus_collide(game_map, tank_factory, music)

    check_bullet_tank_collide(tank_factory)

    for player in players:
        if player.hp == 0:
            game_map.explosion.add(Explosion(screen, player.rect.centerx, player.rect.centery))
            music.play_hit_kill()
            tank_factory.create_player(player.p)
            tank_factory.players.remove(player)

    for enemy in tank_factory.enemies:
        if enemy.hp == 0:
            game_map.explosion.add(Explosion(screen, enemy.rect.centerx, enemy.rect.centery))
            game_map.score.add(Score(screen, enemy.score, enemy.rect.centerx, enemy.rect.centery))
            tank_factory.left_number -= 1
            score += enemy.score

            if enemy.is_bonus:
                game_map.bonus.add(Bonus(screen, random.randint(0, 5), enemy.rect.centerx, enemy.rect.centery))
                music.play_hit_special()
            else:
                music.play_hit_kill()

            tank_factory.enemies.remove(enemy)

    return score


def update_map(screen, game_map, music):
    for block in game_map.blocks:
        if block.hp == 0:
            game_map.explosion.add(Explosion(screen, block.rect.centerx, block.rect.centery))
            game_map.blocks.remove(block)
            music.play_hit_brick()
        elif block.hp < -1:
            game_map.explosion.add(Explosion(screen, block.rect.centerx, block.rect.centery))
            music.play_hit_steel()
            block.hp = -1

    if game_map.base.hp == 0:
        game_map.explosion.add(Explosion(screen, game_map.base.rect.centerx, game_map.base.rect.centery))

    for explosion in game_map.explosion:
        if explosion.explosion_time == 0:
            game_map.explosion.remove(explosion)

    for bonus in game_map.bonus:
        if bonus.bonus_last_time == 0:
            game_map.bonus.remove(bonus)

    for score in game_map.score:
        if score.score_last_time == 0 and score.explosion_time == 0:
            game_map.score.remove(score)

def update_board(board):
    board.draw()

def update_screen(screen, game_map, tank_factory, music, board):
    score = update_tank_factory(screen, game_map, tank_factory, music)
    update_map(screen, game_map, music)
    update_board(board)
    return score


def draw_screen(screen, game_map, tank_factory, board):
    screen.fill(Bg_color)

    game_map.draw_block()

    for player in tank_factory.players:
        player.draw()
    for enemy in tank_factory.enemies:
        enemy.draw()

    game_map.draw_grass()
    board.draw()
    pygame.display.update()
