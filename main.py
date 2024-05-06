import pygame
import constants as const
from enemy import Enemy
from world import World
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

#load images
#map
map_image = pygame.image.load('graphicsNew/testMap.png')

#create groups
enemy_group = pygame.sprite.Group()

#enemies
enemyName = Enemy(waypoints, enemy_image)
enemy_group.add(enemyName)

#world
world = World(map_image)

#game loop
run = True
while run:
    clock.tick(const.FPS)

    screen.fill("grey100")

    #draw level
    world.draw(screen)

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