import pygame as pg
from pygame.math import Vector2

class Enemy(pg.sprite.Sprite):
    def __init__(self, waypoints, image):
        pg.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.speed = 2

    def update(self):
        self.move()

    def move(self):
        self.target = Vector2(self.waypoints[self.target_waypoint])
        self.movement = self.target - self.pos

        #calc distance

        self.pos += self.movement.normalize() * self.speed
        self.rect.center = self.pos