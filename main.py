import pygame
import math
import random
import time
from terrain import make_terrain


pygame.init()

# Set up
flags = pygame.SCALED  |  pygame.RESIZABLE
screen = pygame.display.set_mode((640, 480), flags)
running = True
clock = pygame.time.Clock()
delta_time = 0.1
debug = False
# Player VARs
x = 304
y = -640
speedY = 0
moveSpeed = 80
jumpStrength = 150
jumpable = False
digPower = 30
# Player movement VARs
keyDPressed = False
keyAPressed = False
keyWPressed = False
keySPressed = False
keyAnyPressed = False
# End of player VARs
cam_y = y
collision = False
gravity = 5
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
            return collision
def redoGroundRects(terrain):
    hitbox = pygame.Rect(x, 226, 32, 32)
    for i in range(len(terrain)):
        terrain[i].rect = pygame.Rect(0,0,32,32)
        if not terrain[i].mined:
            terrain[i].rect = pygame.Rect(terrain[i].x,terrain[i].y,32,32)  # This line causes the hitboxes to appear where the terrain is visually
        #pygame.draw.rect(screen, (0, 255, 0), terrain[i].rect)
        collision = hitbox.colliderect(terrain[i].rect)
        if collision:
            break


    
print(len(terrain)/20)
hitbox = pygame.Rect(x, 224, 32, 32)
digSquare = pygame.Rect(x, 224, 8, 8)
while running:
    screen.fill((0,0,0))
    
    hitbox = pygame.Rect(x, 226, 32, 32)
    redoGroundRects(terrain)
    
    for i in range(len(terrain)):
        collision = digSquare.colliderect(terrain[i].rect)
        if collision and keyAnyPressed:
            terrain[i].hardness -= digPower * delta_time
            print("OI", terrain[i].hardness)
            if terrain[i].hardness <= 0:
                terrain[i].mined = True

    speedY += gravity
    if speedY > jumpStrength:
        speedY = jumpStrength

    draw_terrain(screen, terrain)

    for i in terrain:
        i.y -= speedY * delta_time
    y -= speedY * delta_time
    collision = collide(x)
    if not collision:
        jumpable = False
    if collision:
        if not speedY < 0:
            jumpable = True
        while collision:
            if speedY < 0:
                for i in terrain:
                    i.y -= 1
                y -= 1
            else:
                for i in terrain:
                    i.y += 1
                y += 1
            redoGroundRects(terrain)
            collision = collide(x)
        speedY = 0
        for i in terrain:
            i.y -= 1
        y -= 1

    screen.blit(player, (x, 223))

    if y > cam_y + 4 or y < cam_y - 4:
        cam_y = y

    playerX = font.render(f"{x}", True, (255,255,255))
    velY = font.render(f"{speedY}", True, (255,255,255))
    screen.blit(playerX, (4,4))
    screen.blit(velY, (4,34))

    hitbox = pygame.Rect(x, 224, 32, 32)
    if debug:
        pygame.draw.rect(screen, (0, 0, 255), digSquare)
        for i in range(len(terrain)):
            pygame.draw.rect(screen, (0, 255, 0), terrain[i].rect)
        pygame.draw.rect(screen, (255, 0, 0), hitbox)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Checking for when a button is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                print("D down")
                keyDPressed = True
            if event.key == pygame.K_a:
                print("A down")
                keyAPressed = True
            if event.key == pygame.K_w:
                print("W down")
                keyWPressed = True
            if event.key == pygame.K_s:
                print("S down")
                keySPressed = True
            if event.key == pygame.K_F3:
                if debug:
                    debug = False
                    print("DEBUG OFF")
                else:
                    debug = True
                    print("DEBUG ON")

        #Checking for when a button is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                print("D up")
                keyDPressed = False
            if event.key == pygame.K_a:
                print("A up")
                keyAPressed = False
            if event.key == pygame.K_w:
                print("W up")
                keyWPressed = False
            if event.key == pygame.K_s:
                print("S up")
                keySPressed = False
        
    
    keyAnyPressed = False
    if keyDPressed:
        x += moveSpeed * delta_time
        collision = collide(x)
        digSquare = pygame.Rect(x+24, 224+8, 16, 16)
        while collision:
            x -= 1
            collision = collide(x)
        keyAnyPressed = True
    if keyAPressed:
        x -= moveSpeed * delta_time
        collision = collide(x)
        digSquare = pygame.Rect(x-8, 224+8, 16, 16)
        while collision:
            x += 1
            collision = collide(x)
        keyAnyPressed = True
    if keyWPressed:
        digSquare = pygame.Rect(x+8, 224-8, 16, 16)
        if jumpable:
            speedY -= jumpStrength
        keyAnyPressed = True
    if keySPressed:
        digSquare = pygame.Rect(x+8, 224+24, 16, 16)
        keyAnyPressed = True


    if x < 0:
        x = 0
    if x > 608:
        x = 608

    # end stuff
    pygame.display.flip()
    delta_time = clock.tick(60) / 1000
    delta_time = max(0.001, min((0.1, delta_time)))

pygame.quit()