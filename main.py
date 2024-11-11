import pygame
import json
import constants
import constants as const
from enemy import Enemy
from world import World
from turret import Turret
from button import Button
from pygame.math import Vector2

pygame.init()

#create game window
screen = pygame.display.set_mode((const.SCREEN_WIDTH + const.SIDE_PANEL, const.SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defense")

#create clock
clock = pygame.time.Clock()

#game variables
placing_turrets = False
selected_turret = None

#load imgs
enemy_image = pygame.image.load("graphics/player_stand.png").convert_alpha()
#load images
#map
map_image = pygame.image.load('graphicsNew/testMap.png')
#turret spreadsheet
turret_sheet = pygame.image.load('assets/images/turrets/turret_1.png').convert_alpha()
#inividual turret image for mouse cursor
cursor_turret = pygame.image.load('assets/images/turrets/cursor_turret.png').convert_alpha()
#buttons
buy_turret_image = pygame.image.load('assets/images/buttons/buy_turret.png').convert_alpha()
cancel_image = pygame.image.load('assets/images/buttons/cancel.png').convert_alpha()

#start game button
start_button_image = pygame.image.load('assets/images/buttons/begin.png').convert_alpha()
#restart game button
restart_button_image = pygame.image.load('assets/images/buttons/restart.png').convert_alpha()

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
            new_turret = Turret(turret_sheet, mouse_tile_x, mouse_tile_y, Vector2(mouse_pos[0], mouse_pos[1]))
            turret_group.add(new_turret)
def select_turret(mouse_pos): #not a pure function, because it depends on turret_group
    mouse_tile_x = mouse_pos[0] // const.Tile_size
    mouse_tile_y = mouse_pos[1] // const.Tile_size
    for turret in turret_group:
        if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            return turret

def clear_selection():
    for turret in turret_group:
        turret.selected = False

#create world
world = World(world_data, map_image)
world.process_data()

print(world.waypoints)
#create groups
enemy_group = pygame.sprite.Group()
turret_group = pygame.sprite.Group()

#enemies
enemyName = Enemy(world.waypoints, enemy_image, (100, 100, 50, 10, 100))
enemy_group.add(enemyName)

#create buttons
turret_button = Button(const.SCREEN_WIDTH + 30, 120, buy_turret_image, True)
cancel_button = Button(const.SCREEN_WIDTH + 50, 180, cancel_image, True)
start_button = Button(const.SCREEN_WIDTH + 30, 0, start_button_image, True)
restart_button = Button(const.SCREEN_WIDTH + 30, 0, restart_button_image, True)



game_started = False
restart_button_visible = False

def restart_round(): #void function, declare inside function, it is local variable - laxel scope of the function
    #enemy_group - none local, is declared outside of the function, it does stay modified
    enemy_group.empty()
    new_enemy = Enemy(world.waypoints, enemy_image, (100, 100, 50, 10, 100))
    enemy_group.add(new_enemy)


#enemy_group = restart_round(enemy_groupfunction(world.waypoints,enemy_image))

#todo: shooting animation



#game loop
run = True
while run:
    clock.tick(const.FPS)

    #############################
    # UPDATING SECTION
    #############################
    #update groups
    if game_started:
        enemy_group.update()
    turret_group.update(game_started, enemy_group)


    #highlight selected turret
    if selected_turret:
        selected_turret.selected = True


    for turret in turret_group:
        for enemy in enemy_group:
            if turret.in_range(enemy):
                turret.attack(enemy)
                print(f"Enemy HP: {enemy.hp}")

    # DRAWING SECTION
    #############################

    screen.fill("grey100")

    #draw level
    world.draw(screen)

    if not game_started:
        if start_button.draw(screen):
            game_started = True
            restart_button_visible = True

    if restart_button_visible:
        if restart_button.draw(screen):
            restart_round()

    #draw groups
    if game_started:
        enemy_group.draw(screen)
        for enemy in enemy_group:
            enemy.draw_health(screen)

    for turret in turret_group:
        turret.draw(screen)

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
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            #check if mouse is on the game area
            if mouse_pos[0] < constants.SCREEN_WIDTH and mouse_pos[1] < constants.SCREEN_HEIGHT:
                #Clear selection
                selected_turret = None
                clear_selection()
                if placing_turrets == True:
                    create_turret(mouse_pos)
                else:
                    selected_turret = select_turret(mouse_pos)

    #update display
    pygame.display.flip()

pygame.quit()