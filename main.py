import pygame
import math
import random
import time


pygame.init()

# Set up
flags = pygame.SCALED  |  pygame.RESIZABLE
screen = pygame.display.set_mode((640, 480), flags)
running = True
clock = pygame.time.Clock()
delta_time = 0.1
# Player VARs
x = 304
y = -640
speedY = 0
moveSpeed = 4
jumpStrength = 50
stuck = False
# Player movement VARs
keyDPressed = False
keyAPressed = False
keyWPressed = False
# End of player VARs
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
            terrain[-1].rect=pygame.Rect(terrain[-1].x,terrain[-1].y,32,32)
            if i <= 1 and height == 0:
                terrain[-1].ore=''
                terrain[-1].mined=True
            else:
                if height < 3:
                    if height == 2 and random.randint(1,2) == 2:
                        terrain[-1].ore='Stone'
                    else:
                        terrain[-1].ore='Dirt'
                else:
                    if height > 7 and random.randint(1,2) == 2:
                        terrain[-1].ore=''
                        terrain[-1].mined=True
                    else:
                        terrain[-1].ore='Stone'
        height += 1
    
    return(terrain)

# Drawing of terrain
terrain = make_terrain()
def draw_terrain(screen, terrain):
    for i in terrain:
        if not i.mined and i.y<640 and i.y>-32:
            y = i.y
            if i.ore=='Stone':
                screen.blit(stone,(i.x,i.y))
            if i.ore == 'Dirt':
                screen.blit(dirt,(i.x,i.y))

def collide(playerX):
    hitbox = pygame.Rect(playerX, 224, 32, 32)
    colly = 1
    for i in range(len(terrain)):
        collision = hitbox.colliderect(terrain[i].rect)
        if collision:
            colly += 1
            print("HEY", colly)
            return collision
def redoGroundRects(terrain):
    hitbox = pygame.Rect(x, 226, 32, 32)
    for i in range(len(terrain)):
        if not terrain[i].mined:
            terrain[i].rect = pygame.Rect(terrain[i].x,terrain[i].y,32,32)  # This line causes the hitboxes to appear where the terrain is visually
        #pygame.draw.rect(screen, (0, 255, 0), terrain[i].rect)
        collision = hitbox.colliderect(terrain[i].rect)
        if collision:
            break


    
print(len(terrain)/20)
hitbox = pygame.Rect(x, 224, 32, 32)
while running:
    screen.fill((0,0,0))
    
    hitbox = pygame.Rect(x, 226, 32, 32)
    redoGroundRects(terrain)
    
    
    draw_terrain(screen, terrain)
    collision = collide(x)
    if not collision:
        for i in terrain:
            i.y -= 1
        y -= 1
    collision = collide(x)
    while collision:
        for i in terrain:
            i.y += 1
        redoGroundRects(terrain)
        collision = collide(x)

    screen.blit(player, (x, 224))

    cam_y = y

    playerX = font.render(f"{x}", True, (255,255,255))
    velY = font.render(f"{speedY}", True, (255,255,255))
    screen.blit(playerX, (4,4))
    screen.blit(velY, (4,34))

    hitbox = pygame.Rect(x, 224, 32, 32)
    #pygame.draw.rect(screen, (255, 0, collision), hitbox)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Checking for when a button is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                print("D down")
                keyDPressed = True
            if event.key == pygame.K_a:
                print("a down")
                keyAPressed = True
            if event.key == pygame.K_w:
                print("w down")
                keyWPressed = True
        #Checking for when a button is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                print("D up")
                keyDPressed = False
            if event.key == pygame.K_a:
                print("a up")
                keyAPressed = False
            if event.key == pygame.K_w:
                print("w up")
                keyWPressed = False
        
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE]:
            print("spaced")
            terrain = make_terrain()
            y = -480
            cam_y = y
            speedY = 0
        if pressed[pygame.K_s]:
            print("s")
            y += 1
            cam_y = y
    if keyDPressed:
        x += moveSpeed
        collision = collide(x)
        while collision:
            x -= 1
            collision = collide(x)
    if keyAPressed:
        x -= moveSpeed
        collision = collide(x)
        while collision:
            x += 1
            collision = collide(x)

    if x < 0:
        x = 0
    if x > 608:
        x = 608

    # end stuff
    pygame.display.flip()
    delta_time = clock.tick(60) / 1000
    delta_time = max(0.001, min((0.1, delta_time)))

pygame.quit()