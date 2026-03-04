import pygame
import math
import random

pygame.init()

# Set up
screen = pygame.display.set_mode((640, 480))
running = True
clock = pygame.time.Clock()
delta_time = 0.1
y = 0
moving = False

# Temporary creation of stone
stone = pygame.image.load('img/stone-v1.png').convert_alpha()
stone = pygame.transform.scale(stone,
                               (stone.get_width() * 2,
                               stone.get_height() * 2))
dirt = pygame.image.load('img/dirt-v1.png').convert_alpha()
dirt = pygame.transform.scale(dirt,
                               (dirt.get_width() * 2,
                               dirt.get_height() * 2))
player = pygame.image.load('img/pixil-frame-0 (24).png').convert_alpha()
player = pygame.transform.scale(player,
                               (player.get_width() * 2,
                               player.get_height() * 2))

# Generate the terrain
def make_terrain():
    terrain = []
    height = 0
    for i in range(10):
        for i in range(20):
            if height < 3:
                if height == 2 and random.randint(1,2) == 2:
                    terrain.append(stone)
                else:
                    terrain.append(dirt)
            else:
                terrain.append(stone)
        height += 1
    
    return(terrain)

# Drawing of terrain
terrain = make_terrain()
def draw_terrain(screen, terrain, player_y):
    idx = 0
    x = 0
    y = 0 - player_y
    length = len(terrain)/20
    for i in range(int(length)):
        for i in range(20):


            screen.blit(terrain[idx], (x,y))
            idx += 1
            x += 32
        x = 0
        y += 32
print(len(terrain)/20)
while running:
    screen.fill((0,0,0))

    #screen.blit(stone, (0,0))

    draw_terrain(screen, terrain, y)
    screen.blit(player, (240, 0))
    if moving:
        y += 50 * delta_time

    hitbox = pygame.Rect(240, 0, 32, 32)
    pygame.draw.rect(screen, (255, 0, 0), hitbox)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE]:
            print("spaced")
            terrain = make_terrain()
        if pressed[pygame.K_w]:
            print("w")
            y -=1
        if pressed[pygame.K_s]:
            print("s")
            y += 1

    pygame.display.flip()

    delta_time = clock.tick(60) / 1000
    delta_time = max(0.001, min((0.1, delta_time)))

pygame.quit()