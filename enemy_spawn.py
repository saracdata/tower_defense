import pygame
import logging
from enemy import Enemy

class EnemySpawner:
    def __init__(self, game_level, enemy_images, waypoints, enemy_manager):
        self.game_level = game_level
        self.enemy_images = enemy_images
        self.waypoints = waypoints
        self.spawn_delay = 1000  # Time in milliseconds between spawns
        self.last_spawn_time = pygame.time.get_ticks()  # Track the last spawn time
        self.enemy_queue = self._create_enemy_queue()  # Queue of enemies to spawn
        self.enemy_manager = enemy_manager  # Group to store all spawned enemies
        self.spawn_points = game_level.map.spawn_points
        self.angle_offset = game_level.map.angle_offset

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
            if not self.enemy_queue:
                logging.warning("Enemy queue is empty. No enemies to spawn.")
                return
            try:
                enemy_type = self.enemy_queue.pop(0)
                enemy_image = self.enemy_images[enemy_type]
                spawn_point = self.spawn_points[0]
                new_enemy = Enemy(self.waypoints, enemy_image, spawn_point, self.angle_offset)
                self.enemy_manager.add_enemy(new_enemy)
                self.last_spawn_time = current_time
                logging.debug(f"Enemy spawned, remaining queue length: {len(self.enemy_queue)}")
            except Exception as e:
                logging.error(f"Error while spawning enemy: {e}")

    def restart(self):
        """Clear and reset enemy spawning for a new round."""
        self.enemy_queue = self._create_enemy_queue()
        self.last_spawn_time = pygame.time.get_ticks()
        logging.info("Enemy spawner restarted.")
