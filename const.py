from enum import Enum


class State(Enum):
    Ok = 0
    Success = 1
    Failure = 2


class Direction(Enum):
    Stop = 0
    Up = 1
    Down = 2
    Left = 3
    Right = 4


"""基础设置"""
Game_name = "Tank"

Wall_num = 26
Wall_width = 16
Object_width = 32
Battlefield_width = Wall_num * Wall_width

Screen_width = Battlefield_width + 64
Screen_height = Object_width * 13
Bg_color = (0, 0, 0)
Max_level = 5 #最大关卡数

"""路径设置"""
Map_path = "./maps/map.txt"
Full_path = "./images/00.png"   #信息板在原图
Brick_path = "./images/brick.png"  # 1
Grass_path = "./images/grass.png"  # 2
Steel_path = "./images/steel.png"  # 3
Base_path = "./images/base.png"    # 4
Bonus_path = "./images/bonus.png"
Score_path = "./images/score.png"

Bullet_path = "./images/bullet.png"
Explosion_path = "./images/explosion.png"

Player1_path = "./images/player1.png"
Player2_path = "./images/player2.png"
Protect_path = "./images/protect.png"

Enemy1_path = "./images/enemy1.png"
Enemy2_path = "./images/enemy2.png"
Enemy3_path = "./images/enemy3.png"
Enemy4_path = "./images/enemy4.png"
Twinkle_path = "./images/twinkle.png"


"""音效路径"""
Add_life = "./music/add_life.ogg"
Add_score = "./music/add_score.ogg"
Game_over = "./music/game_over.ogg"
Game_pause = "./music/game_pause.ogg"
Game_start = "./music/game_start.ogg"
Get_props = "./music/get_props.ogg"
Hit_border = "./music/hit_border.ogg"
Hit_brick = "./music/hit_brick.ogg"
Hit_kill = "./music/hit_kill.ogg"
Hit_special = "./music/hit_special.ogg"
Hit_steel = "./music/hit_steel.ogg"
Inc_score = "./music/inc_score.ogg"
Shoot = "./music/shoot.ogg"
Speed_normal = "./music/speed_normal.ogg"
Speed_up = "./music/speed_up.ogg"


"""对象设置"""
Base_protect = [(Battlefield_width * 1/2 - 2 * Wall_width, Battlefield_width - Wall_width),
                (Battlefield_width * 1/2 - 2 * Wall_width, Battlefield_width - 2 * Wall_width),
                (Battlefield_width * 1/2 - 2 * Wall_width, Battlefield_width - 3 * Wall_width),
                (Battlefield_width * 1/2 - Wall_width, Battlefield_width - 3 * Wall_width),
                (Battlefield_width * 1/2, Battlefield_width - 3 * Wall_width),
                (Battlefield_width * 1/2 + Wall_width, Battlefield_width - 3 * Wall_width),
                (Battlefield_width * 1/2 + Wall_width, Battlefield_width - 2 * Wall_width),
                (Battlefield_width * 1/2 + Wall_width, Battlefield_width - Wall_width)]

Bullet_speed = 30
Explosion_time = 50

Tank_speed = 2

Player_hp = 3
Protect_time = 500
Score_last_time = 50
Revive_x1 = 8 * Wall_width
Revive_y1 = Battlefield_width - Object_width
Revive_x2 = 16 * Wall_width
Revive_y2 = Battlefield_width - Object_width

Enemy_number = 20
Enemy_create_frequency = 200
Enemy_fire_frequency = 200
Enemy_change_direction_frequency = 400
Twinkle_time = 50
Stop_time = 300
Create1_x = 0
Create1_y = 0
Create2_x = Battlefield_width - Object_width
Create2_y = Battlefield_width - Object_width
Create3_x = 12 * Wall_width
Create3_y = 0

Bonus_last_time = 500


"""频率设置"""
Clock_frequency = 55

