import pygame

pygame.mixer.init()

channel = pygame.mixer.Channel(2)
sound = pygame.mixer.Sound('shoot.ogg')
while 1:
    if channel.get_busy() == False:
        #sound.play()
        channel.play(sound)