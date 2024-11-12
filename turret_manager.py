import pygame
from turret import Turret
import constants as const
from pygame.math import Vector2


class TurretManager:
    def __init__(self, world, turret_group, gold_balance, enemy_group):
        self.world = world
        self.turret_group = turret_group
        self.gold_balance = gold_balance
        self.enemy_group = enemy_group


    def create_turret(self, mouse_pos, turret_sheet):
        mouse_tile_x = mouse_pos[0] // const.Tile_size
        mouse_tile_y = mouse_pos[1] // const.Tile_size
        mouse_tile_num = (mouse_tile_y * const.Cols) + mouse_tile_x

        new_turret = Turret(turret_sheet, mouse_tile_x, mouse_tile_y, Vector2(mouse_pos[0], mouse_pos[1]))

        # Check if tile is grass and if the player can afford the turret
        if self.world.tile_map[mouse_tile_num] == 10 and self.can_afford(new_turret.cost):
            # Check if there's already a turret on the tile
            if self.is_tile_free(mouse_tile_x, mouse_tile_y):
                self.turret_group.add(new_turret)
                self.deduct_gold(new_turret.cost)

    def is_tile_free(self, x, y):
        for turret in self.turret_group:
            if (x, y) == (turret.tile_x, turret.tile_y):
                return False
        return True

    def can_afford(self, cost):
        return self.gold_balance >= cost

    def deduct_gold(self, cost):
        if self.can_afford(cost):
            self.gold_balance -= cost
        return

    def select_turret(self, mouse_pos):
        mouse_tile_x = mouse_pos[0] // const.Tile_size
        mouse_tile_y = mouse_pos[1] // const.Tile_size
        for turret in self.turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                turret.select()
                return turret
        return None

    def clear_selection(self):
        for turret in self.turret_group:
            turret.deselect()

    def update(self, game_started):
        if game_started:
            for turret in self.turret_group:
                turret.update(game_started, self.enemy_group)

    def draw(self, surface):
        for turret in self.turret_group:
            turret.draw(surface)

    def handle_turret_placement(self, mouse_pos, placing_turrets, turret_sheet):
        if placing_turrets:
            self.create_turret(mouse_pos, turret_sheet)
        else:
            return self.select_turret(mouse_pos)

    def update(self, game_started):
        for turret in self.turret_group:
            turret.update(game_started, self.enemy_group)
            for enemy in self.enemy_group:
                if turret.in_range(enemy):
                    turret.attack(enemy)
                    print(f"Enemy HP: {enemy.hp}")
