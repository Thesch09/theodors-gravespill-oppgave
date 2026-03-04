import pygame
import math
import random

pygame.init()

# Set up
screen = pygame.display.set_mode((640, 480))
running = True
clock = pygame.time.Clock()
delta_time = 0.1
x = 304
y = -480
cam_y = y
collision = False

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
                if height > 7 and random.randint(1,2) == 2:
                    terrain.append("")
                else:
                    terrain.append(stone)
        height += 1
    
    return(terrain)

# Drawing of terrain
terrain = make_terrain()
def draw_terrain(screen, terrain, player_y):
    grounds = []
    idx = 0
    x = 0
    y = 0 - player_y
    length = len(terrain)/20
    for i in range(int(length)):
        for i in range(20):
            if terrain[idx] != "":
                screen.blit(terrain[idx], (x,y))
                ground = pygame.Rect(x, y, 32, 32)
                pygame.draw.rect(screen, (0, 255, 0), ground)
                grounds.append(ground)
            idx += 1
            x += 32
        x = 0
        y += 32
    return(grounds)
    
print(len(terrain)/20)
while running:
    screen.fill((0,0,0))

    ground = draw_terrain(screen, terrain, cam_y)
    screen.blit(player, (x, 224))
    speedY = 50
    if not collision:
        y += speedY * delta_time
    cam_y = y

    hitbox = pygame.Rect(x, 224, 32, 32)
    #collision = hitbox.colliderect(ground)
    #print(collision)
    for i in range(len(ground)):
        collision = hitbox.colliderect(ground[i])
        print(collision)
    pygame.draw.rect(screen, (255, 0, collision), hitbox)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE]:
            print("spaced")
            terrain = make_terrain()
            y = -640
            cam_y = y
        if pressed[pygame.K_w]:
            print("w")
            y -=1
            cam_y = y
        if pressed[pygame.K_s]:
            print("s")
            y += 1
            cam_y = y
        if pressed[pygame.K_d]:
            print("d")
            x +=1
        if pressed[pygame.K_a]:
            print("a")
            x -= 1

    pygame.display.flip()

    delta_time = clock.tick(60) / 1000
    delta_time = max(0.001, min((0.1, delta_time)))

pygame.quit()