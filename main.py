import pygame
import math
import random
import time


pygame.init()

# Set up
screen = pygame.display.set_mode((640, 480))
running = True
clock = pygame.time.Clock()
delta_time = 0.1
x = 304
y = -480
speedY = 0
cam_y = y
collision = False
font = pygame.font.Font(None, size=30)

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
    idx = 0
    x = 0
    y = 0 - player_y
    length = len(terrain)/20
    for i in range(int(length)):
        for i in range(20):
            if terrain[idx] != "":
                screen.blit(terrain[idx], (x,y))
                if idx == 0:
                    first_block = font.render(f"First Block: {x}, {math.floor(y)}", True, (255, 255, 255))

            idx += 1
            x += 32
        x = 0
        y += 32
    return(first_block)


def squares(player_x, player_y):
    if player_y > -240:
        global temp1
        global temp2
        global temp3
        global temp4
        global temp5
        global temp6
        global temp7
        global temp8
        global temp9

        idx = 0
        y = 0
        

        # Top right
        temp1 = pygame.Rect(math.floor(player_x/32)*32-32, 192, 32, 32)
        pygame.draw.rect(screen, (0, 0, 255), temp1)
        # Top center
        temp2 = pygame.Rect(math.floor(player_x/32)*32, 192, 32, 32)
        pygame.draw.rect(screen, (0, 0, 255), temp2)
        # Top left
        temp3 = pygame.Rect(math.floor(player_x/32)*32+32, 192, 32, 32)
        pygame.draw.rect(screen, (0, 0, 255), temp3)
        # Right
        temp4 = pygame.Rect(math.floor(player_x/32)*32-32, 224, 32, 32)
        pygame.draw.rect(screen, (0, 0, 255), temp4)
        # Center
        temp5 = pygame.Rect(math.floor(player_x/32)*32, 224, 32, 32)
        pygame.draw.rect(screen, (0, 0, 255), temp5)
        # Left
        temp6 = pygame.Rect(math.floor(player_x/32)*32+32, 224, 32, 32)
        pygame.draw.rect(screen, (0, 0, 255), temp6)
        # Bottom right
        temp7 = pygame.Rect(math.floor(player_x/32)*32-32, 256, 32, 32)
        pygame.draw.rect(screen, (0, 0, 255), temp7)
        #Bottom center
        temp8 = pygame.Rect(math.floor(player_x/32)*32, 256, 32, 32)
        pygame.draw.rect(screen, (255, 0, 255), temp8)
        # Bottom left
        temp9 = pygame.Rect(math.floor(player_x/32)*32+32, 256, 32, 32)
        pygame.draw.rect(screen, (0, 0, 255), temp9)
    #print(collision)
    
print(len(terrain)/20)
hitbox = pygame.Rect(x, 224, 32, 32)
first_block = font.render(f"Not spawned", True, (255, 255, 255))
squares(0,0)
while running:
    screen.fill((0,0,0))

    first_block=draw_terrain(screen, terrain, cam_y)
    screen.blit(player, (x, 224))

    y_pos = font.render(f"Y pos: {y}", True, (255, 255, 255))
    screen.blit(y_pos,(4,4))
    
    y += speedY * delta_time
    hitbox = pygame.Rect(x, 226, 32, 32)
    collision = hitbox.colliderect(temp8)

    #print(collision)
    if collision:
        speedY = 0
    elif speedY != 50:
        speedY = speedY+1
        
    y_vel = font.render(f"Y vel: {speedY}", True, (255, 255, 255))
    screen.blit(first_block,(4,20))
    screen.blit(y_vel,(4,36))


    squares(x,y)
    cam_y = y

    hitbox = pygame.Rect(x, 224, 32, 32)
    
    #for i in range(len(ground)):
        #collision = hitbox.colliderect(ground[i])
        #print(collision)
    pygame.draw.rect(screen, (255, 0, collision), hitbox)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE]:
            print("spaced")
            terrain = make_terrain()
            y = -480
            cam_y = y
            speedY = 0
        if pressed[pygame.K_w]:
            print("w")
            speedY = -10
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