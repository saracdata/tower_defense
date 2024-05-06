import pygame as pg

class World():
    def __init__(self, data, map_image):
        self.level_data = data
        self.image = map_image

    def process_data(self):
        for layer in self.level_data["layers"]:
            if layer["name"] == "waypoints":
                print(layer)
    def draw(self, surface):
        surface.blit(self.image, (0,0))