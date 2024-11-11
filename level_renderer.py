import pygame
from pygame import font as pg_font, Surface
from design import GameLevel


class LevelRender:
    static_surface = None  # Class attribute to hold the static surface

    def render_level(self, game_level: GameLevel, screen: Surface):
        """Render static elements like level text once and dynamic elements like gold balance."""
        # Initialize static surface if it hasn't been created yet
        if LevelRender.static_surface is None:
            # Define the size based on text dimensions plus padding
            white = (255, 255, 255)
            font = pg_font.Font(None, 36)
            text_surface = font.render(game_level.level_label, True, white)
            text_rect = text_surface.get_rect(topleft=(10, 10))

            # Create static surface with precise size and transparency
            LevelRender.static_surface = Surface((text_rect.width + 20, text_rect.height + 20), pygame.SRCALPHA)
            LevelRender.static_surface.fill((0, 0, 0, 0))  # Fully transparent background

            # Blit text onto static_surface
            LevelRender.static_surface.blit(text_surface, text_rect)

        # Blit static surface containing level text onto the screen
        screen.blit(LevelRender.static_surface, (0, 0))

        # Render dynamic elements like gold balance
        self.render_level_gold(game_level.gold_balance, screen)

    def render_level_gold(self, gold_bal: int, screen: Surface):
        """Render the current gold balance as it changes."""
        gold_color = (255, 215, 0)
        font = pg_font.Font(None, 36)

        # Render gold balance dynamically
        text_surface = font.render(str(gold_bal), True, gold_color)
        text_rect = text_surface.get_rect(topright=(450, 10))
        screen.blit(text_surface, text_rect)