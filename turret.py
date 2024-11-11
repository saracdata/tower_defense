import math
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

        #precompute rotations and add alignment variables
        self.rotated_images = self.precompute_rotated_images()
        self.current_angle = 0
        self.is_aligned = False

#put other functions as private in other language, each function that start with _
    def load_images(self):
        #extract img from sprite sheet
        size = self.sprite_sheet.get_height()
        animation_list = []
        for x in range(c.ANIMATION_STEPS):
            temp_img = self.sprite_sheet.subsurface(x * size, 0, size, size)
            animation_list.append(temp_img)
        return animation_list

    def precompute_rotated_images(self):
        rotated_images = {}
        for angle in range(0, 360, 30): #pick at chunks of 15 degrees
            rotated_images[angle] = [pg.transform.rotate(img, angle) for img in self.animation_list]
        return rotated_images

    def get_rotated_image(self, angle, frame_index):
        nearest_angle = int(round(angle / 30) * 30) % 360
        image = self.rotated_images[nearest_angle][frame_index]
        return image

    def update(self, game_started, enemy_group):
        if not game_started:
            return

        closest_enemy, angle_to_enemy = None, None

        for enemy in enemy_group:
            if self.in_range(enemy):
                closest_enemy = enemy
                direction = closest_enemy.pos - self.pos
                initial_angle_offset = 90
                angle_to_enemy = math.degrees(math.atan2(-direction[1], direction[0])) - initial_angle_offset
                #angle_to_enemy = -30

                break # Exit after the first enemy found in range

        if closest_enemy:
            target_enemy_angle = int(round(angle_to_enemy / 30) * 30) % 360
            self.align_to_target_angle(target_enemy_angle)

            if self.is_aligned \
                    and (pg.time.get_ticks() - self.last_shot) > self.cooldown:
                self.attack(closest_enemy)
                self.play_animation()

        else:
            self.reset_animation()


    def align_to_target_angle(self, target_enemy_angle):

        self.is_aligned = True
        self.image = self.get_rotated_image(target_enemy_angle, self.frame_index)



    def play_animation(self):

        if pg.time.get_ticks() - self.update_time <= c.ANIMATION_DELAY:
            return

        self.update_time = pg.time.get_ticks()

        if self.frame_index < (len(self.animation_list) - 1):
            self.frame_index += 1
        else:
            self.frame_index = 0
            self.last_shot = pg.time.get_ticks()

    def reset_animation(self):
        self.frame_index = 0
        self.image = self.animation_list[self.frame_index]

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





