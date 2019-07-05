import pygame

def check_key_down_events(event, player):
    """检查按键按下"""
    if event.key == pygame.K_RIGHT:
        player.moving_right = True
    elif event.key == pygame.K_LEFT:
        player.moving_left = True
    if event.key == pygame.K_UP:
        player.moving_up = True
    elif event.key == pygame.K_DOWN:
        player.moving_down = True

    if event.key == pygame.K_SPACE:
        player.fire()

    if event.key == pygame.K_P:   #按p暂停
        return False

    return True


def check_key_up_events(event, player):
    """检查松开按键"""
    if event.key == pygame.K_RIGHT:
        player.moving_right = False
    elif event.key == pygame.K_LEFT:
        player.moving_left = False
    if event.key == pygame.K_UP:
        player.moving_up = False
    elif event.key == pygame.K_DOWN:
        player.moving_down = False

    return True


def check_events(player):
    """按键检测"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            return check_key_down_events(event, player)
        elif event.type == pygame.KEYUP:
            return check_key_up_events(event, player)


def check_collisions(player, enemys, player_base, enemy_base, walls):
    """碰撞检测"""
    player_wall_collisions = pygame.sprite.spritecollide(player, walls, False)
    for player_list in player_wall_collisions.values():
        for player in player_list:
            player.cancel_update()

    player_enemys_collisions = pygame.sprite.spritecollide(player, enemys, True)#True碰到敌人敌人销毁
    for player_list in player_enemys_collisions.values():
        for player in player_list:
            player.hp -= 1    # 玩家生命数减一
            #重新生成一辆玩家坦克？

    player_bullet_collisions = pygame.sprite.spritecollide(player, enemys.bullets, False)
    for player_list in player_bullet_collisions.values():
        for player in player_list:
            player.hp -= 1    # 玩家生命数减一
            #重新生成一辆玩家坦克？

    enemys_wall_collisions = pygame.sprite.groupcollide(enemys, walls, True, False)
    for enemys_list in enemys_wall_collisions.values():
        for enemys in enemys_list:
            enemys.cancel_update()
            #敌人重新选择一个方向

    enemys_bullet_collisions = pygame.sprite.groupcollide(player, player.bullets, True, False)
    for enemys_list in enemys_bullet_collisions.values():
        for enemys in enemys_list:
            #删除一个敌人

    #敌人子弹和玩家基地
    enemys_base_collisions = pygame.sprite.spritecollide(enemys.bullets, player_base, False)
    for bullet_list in enemys_base_collisions.values():
        for bullet in bullet_list:
            #每一颗子弹基地生命值减一

    #玩家子弹和敌人基地
    player_base_collisions = pygame.sprite.spritecollide(player.bullets, enemy_base, False)
    for bullet_list in player_base_collisions.values():
        for bullet in bullet_list:
            # 每一颗子弹基地生命值减一

def update_screen(...):
    screen.fill((0, 0, 0)) ...

    player.update_tank(...)
    player.update_bullets(...)

    enemys.update(...)


def draw_screen(...):
    player.draw_player(...)
    player.draw_bullets(...)

    enemys.draw(...)

    pygame.display.update()