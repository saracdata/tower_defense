import pygame
import constants as const

pygame.init()
screen = pygame.display.set_mode((const.SCREEN_WIDTH,const.SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defense")
clock = pygame.time.Clock()

# sky_surface = pygame.image.load('graphics/Sky.png')
# ground_surface = pygame.image.load('graphics/ground.png')

#game loop
run = True
while run:
    clock.tick(const.FPS)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()

#new change