import pygame
from enemy import Enemy

class EnemySpawner:
    def __init__(self, game_level, enemy_images, waypoints, enemy_group):
        self.game_level = game_level
        self.enemy_images = enemy_images
        self.waypoints = waypoints
        self.spawn_delay = 1000  # Time in milliseconds between spawns
        self.last_spawn_time = pygame.time.get_ticks()  # Track the last spawn time
        self.enemy_queue = self._create_enemy_queue()  # Queue of enemies to spawn
        self.enemy_group = enemy_group  # Group to store all spawned enemies

    def _create_enemy_queue(self):
        """Prepare the enemy queue based on game_level configuration."""
        queue = []
        for enemy_type, count in self.game_level.enemy_type_to_count.items():
            for _ in range(count):
                queue.append(enemy_type)
        return queue

    def update(self):
        """Spawn enemies at intervals."""
        current_time = pygame.time.get_ticks()
        if self.enemy_queue and current_time - self.last_spawn_time >= self.spawn_delay:
            enemy_type = self.enemy_queue.pop(0)
            enemy_image = self.enemy_images[enemy_type]
            new_enemy = Enemy(self.waypoints, enemy_image, (100, 100, 50, 10, 100))
            self.enemy_group.add(new_enemy)
            self.last_spawn_time = current_time

    def restart(self):
        """Clear and reset enemy spawning for a new round."""
        self.enemy_group.empty()
        self.enemy_queue = self._create_enemy_queue()
        self.last_spawn_time = pygame.time.get_ticks()

# To be called in main.py for instantiation and updates
def spawn_enemies(game_level, enemy_images, waypoints, enemy_group):
    return EnemySpawner(game_level, enemy_images, waypoints, enemy_group)