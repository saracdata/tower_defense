from enemy import Enemy

def spawn_enemies(game_level, waypoints, enemy_group,  enemy_images):
    """Spawn enemies based on the configuration in game_level."""
    for enemy_type, count in game_level.enemy_type_to_count.items():
        for _ in range(count):
            enemy_image = enemy_images[enemy_type]
            enemy = Enemy(waypoints, enemy_image, (100, 100, 50, 10, 100))  # Adjust stats as needed
            enemy_group.add(enemy)