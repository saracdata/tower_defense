import pygame
import constants as const
from enemy import Enemy

pygame.init()
screen = pygame.display.set_mode((const.SCREEN_WIDTH,const.SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defense")
clock = pygame.time.Clock()

#load imgs
enemy_image = pygame.image.load("graphics/snail1.png").convert_alpha()

#create groups
enemy_group = pygame.sprite.Group()

enemyName = Enemy((200,300), enemy_image)
enemy_group.add(enemyName)

#game loop
run = True
while run:
    clock.tick(const.FPS)

    #draw groups
    enemy_group.draw(screen)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update display
    pygame.display.flip()

pygame.quit()