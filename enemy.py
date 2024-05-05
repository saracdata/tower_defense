import pygame as pg
from pygame.math import Vector2
import math
class Enemy(pg.sprite.Sprite):
    def __init__(self, waypoints, image):
        pg.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.angle = 0
        self.original_img = image
        self.image = pg.transform.rotate(self.original_img, self.angle)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.speed = 2

    def update(self):
        self.move()
        self.rotate()

    def move(self):
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            self.kill()

        #calc distance
        dist = self.movement.length()
        if dist >= self.speed:
            self.pos += self.movement.normalize() * self.speed
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1

        self.pos += self.movement.normalize() * self.speed

    def rotate(self):
        #calc distance to next waypoint
        dist = self.target - self.pos
        #calc angle using dist
        self.angle = math.degrees(math.atan2(-dist[1], dist[0]))

        #rotate img and update rect
        self.image = pg.transform.rotate(self.original_img, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
