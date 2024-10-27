import pygame as pg
import constants as c
class Turret(pg.sprite.Sprite):
    def __init__(self, sprite_sheet, tile_x, tile_y, pos):
        pg.sprite.Sprite.__init__(self)

        self.range = 90
        self.cooldown = 500
        self.last_shot = pg.time.get_ticks()
        self.selected = False
        self.damage = 0.1
        self.pos = pos

        #position var
        self.tile_x = tile_x
        self.tile_y = tile_y

        #calculate center coordinates
        self.x = (self.tile_x+0.5) * c.Tile_size
        self.y = (self.tile_y+0.5) * c.Tile_size

        #animation var
        self.sprite_sheet = sprite_sheet
        self.animation_list = self.load_images()
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()
        print(f"In initial class{self.update_time}")

        #update image
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        #create transparent circle showing range
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0,0,0))
        self.range_image.set_colorkey((0,0,0))
        pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center


#put other functions as private in other language, each function that start with _
    def load_images(self):
        #extract img from sprite sheet
        size = self.sprite_sheet.get_height()
        animation_list = []
        for x in range(c.ANIMATION_STEPS):
            temp_img = self.sprite_sheet.subsurface(x * size, 0, size, size)
            animation_list.append(temp_img)
        return animation_list

    def update(self, game_started, enemy_group):
        if game_started:
            enemy_in_range = False

            for enemy in enemy_group:
                if self.in_range(enemy):
                    enemy_in_range = True
                    if pg.time.get_ticks() - self.last_shot > self.cooldown:
                        self.attack(enemy)
                        self.play_animation()
                    break # Exit after the first enemy found in range
            if not enemy_in_range:
                self.frame_index = 0
                self.image = self.animation_list[self.frame_index]
                self.is_animating = False


    def play_animation(self):
        #only animate if we havn't finished the cycle
        if not self.is_animating:
            self.is_animating = True
        #update image
        self.image = self.animation_list[self.frame_index]
        #check if enough time has passed since last update
        if pg.time.get_ticks() - self.update_time > c.ANIMATION_DELAY:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
                #record completed time and clear target to start cd
                self.last_shot = pg.time.get_ticks()
                self.is_animating = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)

    def attack(self, enemy):
        if self.in_range(enemy):
            enemy.hp -= self.damage

    def in_range(self, enemy):
        distance = self.pos.distance_to(enemy.pos)
        return distance <= self.range





