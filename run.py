from game import Game


if __name__ == "__main__":
    tank_game = Game()
    while True:
        tank_game.Start_menu()
        tank_game.initialize()
        tank_game.start()
