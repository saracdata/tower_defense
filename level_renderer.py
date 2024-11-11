from pygame import font as pg_font, Surface
from design import GameLevel
from level_state import LevelState

class LevelRender:
    # def __init__(self, level):
    #     self.current_level = level
    def render_level(self, game_level: GameLevel, level_state: LevelState, screen: Surface):
        self.__render_level_text(game_level, screen)
        self.__render_level_gold(level_state, screen)

    def __render_level_text(self, game_level: GameLevel, screen: Surface):

        # font game object
        white = (255, 255, 255)
        font = pg_font.Font(None, 36)
        text_surface = font.render(game_level.level_label, True, white)
        text_rect = text_surface.get_rect(topleft=(10, 10))
        screen.blit(text_surface, text_rect)

    def __render_level_gold(self, level_state: LevelState, screen: Surface):

        gold = (255, 215, 0)
        font = pg_font.Font(None, 36)
        text_surface = font.render(str(level_state.current_gold_balance), True, gold)
        text_rect = text_surface.get_rect(topright=(450, 10))
        screen.blit(text_surface, text_rect)
