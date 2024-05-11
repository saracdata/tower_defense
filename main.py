import pygame
import json
import constants
import constants as const
from enemy import Enemy
from world import World
from turret import Turret
from button import Button

pygame.init()

#create game window
screen = pygame.display.set_mode((const.SCREEN_WIDTH + const.SIDE_PANEL,const.SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defense")

#create clock
clock = pygame.time.Clock()

#game variables
placing_turrets = False

#load imgs
enemy_image = pygame.image.load("graphics/snail1.png").convert_alpha()
#load images
#map
map_image = pygame.image.load('graphicsNew/testMap.png')
#inividual turret image for mouse cursor

cursor_turret = pygame.image.load('assets/images/turrets/cursor_turret.png').convert_alpha()

#buttons
buy_turret_image = pygame.image.load('assets/images/buttons/buy_turret.png').convert_alpha()
cancel_image = pygame.image.load('assets/images/buttons/cancel.png').convert_alpha()

#load json data for level
with open('graphicsNew/testMap.tmj') as file:
    world_data = json.load(file)

def create_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // const.Tile_size
    mouse_tile_y = mouse_pos[1] // const.Tile_size
    #calculate the sequential number of the tile
    mouse_tile_num = (mouse_tile_y * const.Cols) + mouse_tile_x
    #check if that tile is grass
    if world.tile_map[mouse_tile_num] == 10:
        #check that there isn't already a turret there
        space_is_free = True
        for turret in turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                space_is_free = False
        #if it is a free space then create turret
        if space_is_free == True:
            new_turret = Turret(cursor_turret, mouse_tile_x, mouse_tile_y)
            turret_group.add(new_turret)


#create world
world = World(world_data, map_image)
world.process_data()

print(world.waypoints)
#create groups
enemy_group = pygame.sprite.Group()
turret_group = pygame.sprite.Group()

#enemies
enemyName = Enemy(world.waypoints, enemy_image)
enemy_group.add(enemyName)

#create buttons
turret_button = Button(const.SCREEN_WIDTH + 30, 120, buy_turret_image, True)
cancel_button = Button(const.SCREEN_WIDTH + 50, 180, cancel_image, True)

#game loop
run = True
while run:
    clock.tick(const.FPS)

    #############################
    # UPDATING SECTION
    #############################
    #update groups
    enemy_group.update()

    #############################
    # DRAWING SECTION
    #############################

    screen.fill("grey100")

    #draw level
    world.draw(screen)

    #draw groups
    enemy_group.draw(screen)
    turret_group.draw(screen)

    #draw buttons
    #button for placing turrets
    if turret_button.draw(screen):
        placing_turrets = True
    #if placing turrets then show the cancel button as well
    if placing_turrets == True:
        #show cursor turret
        cursor_rect = cursor_turret.get_rect()
        cursor_pos = pygame.mouse.get_pos()
        cursor_rect.center = cursor_pos
        #print(cursor_rect.center, cursor_rect)
        if cursor_pos[0] <= const.SCREEN_WIDTH:
            screen.blit(cursor_turret, cursor_rect)
        if cancel_button.draw(screen):
            placing_turrets = False

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #mouse click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1:
            mouse_pos = pygame.mouse.get_pos()
            #check if mouse is on the game area
            if mouse_pos[0] < constants.SCREEN_WIDTH and mouse_pos[1] < constants.SCREEN_HEIGHT:
                if placing_turrets == True:
                    create_turret(mouse_pos)

    #update display
    pygame.display.flip()

pygame.quit()