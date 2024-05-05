import pygame
import constants as const
from enemy import Enemy

pygame.init()
screen = pygame.display.set_mode((const.SCREEN_WIDTH,const.SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defense")
clock = pygame.time.Clock()

#load imgs
enemy_image = pygame.image.load("graphics/snail1.png").convert_alpha()

waypoints = [
    (100,100),
    (400,200),
    (400,100),
    (200,300),
]

#create groups
enemy_group = pygame.sprite.Group()

enemyName = Enemy(waypoints, enemy_image)
enemy_group.add(enemyName)

#game loop
run = True
while run:
    clock.tick(const.FPS)

    screen.fill("grey100")

    #draw enemy path
    pygame.draw.lines(screen, "grey0", False, waypoints)
    #update groups
    enemy_group.update()

    #draw groups
    enemy_group.draw(screen)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update display
    pygame.display.flip()

pygame.quit()