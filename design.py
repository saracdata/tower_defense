from enum import Enum
from typing import Dict, List


class EnemyType(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


class TurretType(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


class MapSource:
    def __init__(self, filename: str):
        self.filename = filename


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
                 turret_type_list: List[TurretType], map: MapSource, extra_effect: List[ExtraEffectType]):

        self.level_label = level_label
        self.gold_balance = gold_balance
        self.enemy_type_to_count = enemy_type_to_count
        self.turret_type_list = turret_type_list
        self.map = map
        self.extra_effect = extra_effect



