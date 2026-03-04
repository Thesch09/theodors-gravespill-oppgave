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
            class block:
                x=0
                y=0
                ore='Stone'
                rect=pygame.Rect(x,y,32,32)
                hardness=60
                mined=False
            terrain.append(block)
            terrain[-1].x=i*32
            terrain[-1].y=350+(height*32)
            terrain[-1].rect=pygame.Rect(i,350,32,32)
            if height < 3:
                if height == 2 and random.randint(1,2) == 2:
                    terrain[-1].ore='Stone'
                else:
                    terrain[-1].ore='Dirt'
            else:
                if height > 7 and random.randint(1,2) == 2:
                    terrain[-1].ore=''
                else:
                    terrain[-1].ore='Stone'
        height += 1
    
    return(terrain)

# Drawing of terrain
terrain = make_terrain()
def draw_terrain(screen, terrain):
    for i in terrain:
        if not i.mined and i.y<640 and i.y>-32:
            if i.ore=='Stone':
                screen.blit(stone,(i.x,i.y))
            if i.ore == 'Dirt':
                screen.blit(dirt,(i.x,i.y))



    
print(len(terrain)/20)
hitbox = pygame.Rect(x, 224, 32, 32)
while running:
    screen.fill((0,0,0))

    draw_terrain(screen, terrain)
    screen.blit(player, (x, 224))
    
    hitbox = pygame.Rect(x, 226, 32, 32)
    for i in terrain:
        pygame.draw.rect(screen, (0, 255, 0), i.rect)
        collision = hitbox.colliderect(i.rect)
        if collision:
            break

    if not collision:
        for i in terrain:
            i.y -= 1
        y -= 1


    #print(collision)
    #if speedY < 100:
        #speedY = speedY+1
    #if #collision:
        #speedY = 0

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
            #speedY = 0
        if pressed[pygame.K_w]:
            print("w")
            speedY = -50
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