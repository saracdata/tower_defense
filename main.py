import pygame
import json
import constants as const
from world import World
from turret import Turret
from button import Button
from pygame.math import Vector2
from design import GameLevel, EnemyType, TurretType, MapSource, ExtraEffectType
from level_renderer import LevelRender
from level_state_global import *
import copy
from game_level_config_load import load_level_config
from enemy_manager import EnemyManager
import logging

logging.basicConfig(level=logging.DEBUG)

pygame.init()

#create game window
screen = pygame.display.set_mode((const.SCREEN_WIDTH + const.SIDE_PANEL, const.SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defense")

#create clock
clock = pygame.time.Clock()

#game variables
placing_turrets = False
selected_turret = None

enemy_images = {
    EnemyType.RED: pygame.image.load("graphics/player_stand.png").convert_alpha(),
    EnemyType.GREEN: pygame.image.load("graphics/Fly1.png").convert_alpha(),
    EnemyType.BLUE: pygame.image.load("graphics/snail1.png").convert_alpha(),

}

turret_sheet = pygame.image.load('assets/images/turrets/turret_1.png').convert_alpha()
cursor_turret = pygame.image.load('assets/images/turrets/cursor_turret.png').convert_alpha()
buy_turret_image = pygame.image.load('assets/images/buttons/buy_turret.png').convert_alpha()
cancel_image = pygame.image.load('assets/images/buttons/cancel.png').convert_alpha()
start_button_image = pygame.image.load('assets/images/buttons/begin.png').convert_alpha()
restart_button_image = pygame.image.load('assets/images/buttons/restart.png').convert_alpha()

#create buttons
turret_button = Button(const.SCREEN_WIDTH + 30, 120, buy_turret_image, True)
cancel_button = Button(const.SCREEN_WIDTH + 50, 180, cancel_image, True)
start_button = Button(const.SCREEN_WIDTH + 30, 0, start_button_image, True)
restart_button = Button(const.SCREEN_WIDTH + 30, 0, restart_button_image, True)


level_name = "level_1"

test_level = load_level_config(level_name)

current_level = copy.deepcopy(test_level)

level_render = LevelRender()

set_starting_gold(current_level)

world_data = current_level.map.load_map_data()

map_image = current_level.map.load_graphics_image()

#create world
world = World(world_data, map_image)
world.process_data()

print(world.waypoints)

def create_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // const.Tile_size
    mouse_tile_y = mouse_pos[1] // const.Tile_size
    #calculate the sequential number of the tile
    mouse_tile_num = (mouse_tile_y * const.Cols) + mouse_tile_x

    new_turret = Turret(turret_sheet, mouse_tile_x, mouse_tile_y, Vector2(mouse_pos[0], mouse_pos[1]))

    #check if that tile is grass
    if world.tile_map[mouse_tile_num] == 10 and can_afford(new_turret.cost):
        #check that there isn't already a turret there
        space_is_free = True
        for turret in turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                space_is_free = False
        #if it is a free space then create turret
        if space_is_free == True:
            turret_group.add(new_turret)
            deduct_gold(new_turret.cost, current_level)

def select_turret(mouse_pos): #not a pure function, because it depends on turret_group
    mouse_tile_x = mouse_pos[0] // const.Tile_size
    mouse_tile_y = mouse_pos[1] // const.Tile_size
    for turret in turret_group:
        if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            return turret

def clear_selection():
    for turret in turret_group:
        turret.selected = False


#create groups
enemy_group = pygame.sprite.Group()
turret_group = pygame.sprite.Group()

game_started = False
restart_button_visible = False

enemy_manager = EnemyManager(current_level, enemy_images, world.waypoints)

#game loop
run = True
while run:
    clock.tick(const.FPS)

    #############################
    # UPDATING SECTION
    #############################
    #update groups
    if game_started:
        enemy_manager.update_enemies()

    turret_group.update(game_started, enemy_manager.enemy_group)


    #highlight selected turret
    if selected_turret:
        selected_turret.selected = True


    for turret in turret_group:
        for enemy in enemy_manager.enemy_group:
            if turret.in_range(enemy):
                turret.attack(enemy)
                print(f"Enemy HP: {enemy.hp}")

    # DRAWING SECTION
    #############################
    screen.fill("grey100")

    # draw level
    world.draw(screen)


    level_render.render_level(current_level, screen)

    if not game_started:
        if start_button.draw(screen):
            game_started = True
            restart_button_visible = True

    if restart_button_visible:
        if restart_button.draw(screen):
            enemy_manager.restart()

    #draw groups
    if game_started:
        enemy_manager.draw_enemies(screen)

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
            if mouse_pos[0] < const.SCREEN_WIDTH and mouse_pos[1] < const.SCREEN_HEIGHT:
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