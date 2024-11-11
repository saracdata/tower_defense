import pygame
from enemy import Enemy
from enemy_spawn import EnemySpawner

class EnemyManager:
    def __init__(self, game_level, enemy_images, waypoints):
        self.enemy_group = pygame.sprite.Group()  # Holds all spawned enemies
        self.enemy_spawner = EnemySpawner(game_level, enemy_images, waypoints, self)

    def add_enemy(self, enemy):
        """Adds an enemy to the enemy group."""
        self.enemy_group.add(enemy)

    def update_enemies(self):
        """Updates all enemies and spawner."""
        self.enemy_spawner.update()
        self.enemy_group.update()

    def draw_enemies(self, screen):
        """Draws all enemies on the screen."""
        self.enemy_group.draw(screen)
        for enemy in self.enemy_group:
            enemy.draw_health(screen)

    def clear_enemies(self):
        """Clears all enemies for a round restart."""
        self.enemy_group.empty()

    def restart(self):
        """Resets enemies and spawner for a new round."""
        self.clear_enemies()  # Clear current enemies
        self.enemy_spawner.restart()  # Restart spawner