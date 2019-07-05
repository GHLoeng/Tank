import pygame
import function

class Game:
    """完成基础功能后可继续在这个类中增加主菜单、过场效果、结束效果"""

    def __init__(self):
        """游戏一开始时调用"""
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.ai_settings = ...
        pygame.display.set_caption("Tank")


    def initialize(self):
        """每开始一轮时调动"""                  #TankFactory用来生成所有坦克
        self.tank_factory = TankFactory(self.ai_settings.player_num,  #一关中玩家生命数
                                        self.ai_settings.enemy_num,...)  #一关中敌人数量

        self.player = Group()         #玩家 精灵组？如果不用精灵组则TankFactory返回一个player对象
        self.tankFactory.new_player(self.player, ...)   #生成玩家    n条命生成n辆？

        self.enemy = Group()           #敌人   精灵组
        self.tankFactory.new_enemy(self.enemy, ...)  #生成初始敌人

        self.player_base = ...        #玩家基地
        self.enemy_base = ...        #敌人基地

        self.wall = ...                #加载墙   精灵组
        self.map = ...                 #加载地图
        self.clock = pygame.time.Clock()


    def start(self):
        """开始一轮游戏"""
        while True:
            if check_events(self.player) == False:   #按键检测
                ...  暂停时的操作
            """检测碰撞（坦克和墙、坦克和子弹、子弹和墙）"""
            """检查玩家生命数"""
            """新建敌人"""

            update_screen(...)
            draw_screen(...)
            clock.tick(self.ai_settings.frequency)  #clock.tick(60) #画面刷新频率