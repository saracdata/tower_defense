import pygame
import json
from enum import Enum
from typing import Dict, List, Tuple


class EnemyType(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


class TurretType(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


class MapType(Enum):
    DESERT = ("desert_main_map.tmj", "desert_graphics_map.png")
    FOREST = ("levels/level.tmj", "levels/level.png")
    GRASS = ("graphicsNew/testMap.tmj", "graphicsNew/testMap.png")

    def __init__(self, data_file: str, graphics_file: str):
        self.data_file = data_file
        self.graphics_file = graphics_file

    @property
    def files(self) -> Tuple[str, str]:
        """Return the tuple of filenames associated with the map type."""
        return self.data_file, self.graphics_file


class MapSource:
    def __init__(self, map_type: MapType, spawn_points: List[tuple], angle_offset: int):
        self.map_type = map_type
        self.data_file, self.graphics_file = map_type.files
        self.spawn_points = spawn_points
        self.angle_offset = angle_offset

    def load_map_data(self):
        """Load JSON data from the data file."""
        try:
            with open(self.data_file, 'r') as file:
                world_data = json.load(file)
            return world_data
        except FileNotFoundError:
            print(f"Error: {self.data_file} not found.")
            return None

    def load_graphics_image(self):
        """Load the map graphics file as a Pygame image."""
        try:
            map_image = pygame.image.load(self.graphics_file)
            return map_image
        except FileNotFoundError:
            print(f"Error: {self.graphics_file} not found.")
            return None


# class ExtraEffectType(Enum):
#     EARTHQUAKE(100) = 1 #create a separate class ExtraEffect for these 3 separate types
#     TSUNAMI(200) = 2
#     FIRE(300) = 3
#
#     def __init__(self, duration):
#         self.duration = duration
#     def earthquake(self):
#         self.duration = 100
#
#     def tsunami(self):
#         self.duration = 200

class ExtraEffectType(Enum):
    EARTHQUAKE = 1
    TSUNAMI = 2
    FIRE = 3


class GameLevel:

    level_label: str
    gold_balance: int
    enemy_type_to_count: Dict[EnemyType, int]
    turret_type_list: List[TurretType]
    map: MapSource
    extra_effect: List[ExtraEffectType]

    def __init__(self, level_label: str, gold_balance: int, enemy_type_to_count: Dict[EnemyType, int],
                 turret_type_list: List[TurretType], map_source: MapSource, extra_effect: List[ExtraEffectType]):

        self.level_label = level_label
        self.gold_balance = gold_balance
        self.enemy_type_to_count = enemy_type_to_count
        self.turret_type_list = turret_type_list
        self.map = map_source
        self.extra_effect = extra_effect

    def set_balance(self, balance: int):
        self.gold_balance = balance



