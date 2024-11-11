import json
from design import GameLevel, EnemyType, TurretType, MapSource, ExtraEffectType


# Function to load level configuration from a JSON file
def load_level_config(level_name):
    with open('levels_config.json', 'r') as file:
        config = json.load(file)

    level_data = config.get(level_name)
    if level_data:
        # Mapping string values to actual class types (EnemyType, TurretType, etc.)
        enemies = {getattr(EnemyType, key): value for key, value in level_data["enemies"].items()}
        turrets = [getattr(TurretType, turret) for turret in level_data["turrets"]]
        extra_effects = [getattr(ExtraEffectType, effect) for effect in level_data["extra_effects"]]

        map_source = MapSource(level_data["map_source"], level_data["spawn_points"])

        # Create the GameLevel instance
        game_level = GameLevel(
            level_data["level_label"],
            level_data["gold_balance"],
            enemies,
            turrets,
            map_source,
            extra_effects
        )

        return game_level
    else:
        raise ValueError(f"Level '{level_name}' not found in the configuration.")