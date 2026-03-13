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
shopOverlay = False
# Player VARs
x = 304
y = -640
speedY = 0
moveSpeed = 80
jumpStrength = 150
jumpable = False
digPower = 30
money = 0
maxHealth = 25
health = maxHealth
moneyLoss = 0.0 # Float. 0 is lose all, 1 is keep all
deathTimer = 0
controlls = "move"
# Player movement VARs
keyDPressed = False
keyAPressed = False
keyWPressed = False
keySPressed = False
keyAnyPressed = False
degrees = 0
# End of player VARs
cam_y = y
collision = False
gravity = 5
world_depth = 30
font = pygame.font.Font(None, size=30)

# Creation of stones
if True: # Only so that I can hide it in editor
    stone = pygame.image.load('img/stoneV2.png').convert_alpha()
    stone = pygame.transform.scale(stone,
                                (stone.get_width() * 2,
                                stone.get_height() * 2))
    dirt = pygame.image.load('img/dirtV3.png').convert_alpha()
    dirt = pygame.transform.scale(dirt,
                                (dirt.get_width() * 2,
                                dirt.get_height() * 2))
    bluestone = pygame.image.load('img/bluestone.png').convert_alpha()
    bluestone = pygame.transform.scale(bluestone,
                                (bluestone.get_width() * 2,
                                bluestone.get_height() * 2))
    drill = pygame.image.load('img/drillNormalV2.png').convert_alpha()
    drill = pygame.transform.scale(drill,
                                (drill.get_width() * 2,
                                drill.get_height() * 2))
    player = pygame.image.load('img/drillBodyOrange.png').convert_alpha()
    player = pygame.transform.scale(player,
                                (player.get_width() * 2,
                                player.get_height() * 2))
    grass = pygame.image.load('img/grass.png').convert_alpha()
    grass = pygame.transform.scale(grass,
                                (grass.get_width() * 2,
                                grass.get_height() * 2))
    redstone = pygame.image.load('img/redstone.png').convert_alpha()
    redstone = pygame.transform.scale(redstone,
                                (redstone.get_width() * 2,
                                redstone.get_height() * 2))
    iron = pygame.image.load('img/iron.png').convert_alpha()
    iron = pygame.transform.scale(iron,
                                (iron.get_width() * 2,
                                iron.get_height() * 2))
    copper = pygame.image.load('img/copper.png').convert_alpha()
    copper = pygame.transform.scale(copper,
                                (copper.get_width() * 2,
                                copper.get_height() * 2))
    diamond = pygame.image.load('img/diamond.png').convert_alpha()
    diamond = pygame.transform.scale(diamond,
                                (diamond.get_width() * 2,
                                diamond.get_height() * 2))
    bismuth = pygame.image.load('img/bismuth.png').convert_alpha()
    bismuth = pygame.transform.scale(bismuth,
                                (bismuth.get_width() * 2,
                                bismuth.get_height() * 2))
    coal = pygame.image.load('img/coal.png').convert_alpha()
    coal = pygame.transform.scale(coal,
                                (coal.get_width() * 2,
                                coal.get_height() * 2))
    rainbowite = pygame.image.load('img/rainbowite.png').convert_alpha()
    rainbowite = pygame.transform.scale(rainbowite,
                                (rainbowite.get_width() * 2,
                                rainbowite.get_height() * 2))
    heart = pygame.image.load('img/heart.png').convert_alpha()
    heart = pygame.transform.scale(heart,
                                (heart.get_width() * 2,
                                heart.get_height() * 2))
    break1 = pygame.image.load('img/break1.png').convert_alpha()
    break1 = pygame.transform.scale(break1,
                                (break1.get_width() * 2,
                                break1.get_height() * 2))
    break2 = pygame.image.load('img/break2.png').convert_alpha()
    break2 = pygame.transform.scale(break2,
                                (break2.get_width() * 2,
                                break2.get_height() * 2))
    break3 = pygame.image.load('img/break3.png').convert_alpha()
    break3 = pygame.transform.scale(break3,
                                (break3.get_width() * 2,
                                break3.get_height() * 2))

digSFX1 = pygame.mixer.Sound('sfx/dig1.wav')
digSFX2 = pygame.mixer.Sound('sfx/dig2.wav')
digSFX3 = pygame.mixer.Sound('sfx/dig3.wav')
pygame.mixer.Sound.set_volume(digSFX1, 0.5)
pygame.mixer.Sound.set_volume(digSFX2, 0.5)
pygame.mixer.Sound.set_volume(digSFX3, 0.5)
digNoises = [digSFX1, digSFX2, digSFX3]
oreBreak = pygame.mixer.Sound('sfx/oreBreak.wav')
rockBreak = pygame.mixer.Sound('sfx/rockBreak.wav')



# Drawing of terrain
terrain = make_terrain(world_depth)
print(world_depth)
def draw_terrain(screen, terrain, camera):
    for i in terrain:
        if not i.mined:
            y = i.y + 600
            # Rock type
            if i.ore == 'Stone':
                screen.blit(stone,(i.x,y+camera))
            if i.ore == 'Dirt':
                screen.blit(dirt,(i.x,y+camera))
            if i.ore == 'Bluestone':
                screen.blit(bluestone,(i.x,y+camera))
            if i.ore == 'Redstone':
                screen.blit(redstone,(i.x,y+camera))

            # Ore type
            if i.extra == 'Grass':
                screen.blit(grass,(i.x,y+camera))
            if i.extra == 'Iron':
                screen.blit(iron,(i.x,y+camera))
            if i.extra == 'Copper':
                screen.blit(copper,(i.x,y+camera))
            if i.extra == 'Coal':
                screen.blit(coal,(i.x,y+camera))
            if i.extra == 'Diamond':
                screen.blit(diamond,(i.x,y+camera))
            if i.extra == 'Bismuth':
                screen.blit(bismuth,(i.x,y+camera))
            if i.extra == 'Rainbowite':
                screen.blit(rainbowite,(i.x,y+camera))

            # Check if it's broken
            if i.health < i.hardness/4:
                screen.blit(break3, (i.x, y+cam_y))
            if i.health < i.hardness/4*2:
                screen.blit(break2, (i.x, y+cam_y))
            if i.health < i.hardness/4*3:
                screen.blit(break1, (i.x, y+cam_y))

def collide(playerX):
    hitbox = pygame.Rect(playerX+4, 224, 24, 32)
    colly = 1
    for i in range(len(terrain)):
        collision = hitbox.colliderect(terrain[i].rect)
        if collision:
            return collision
def redoGroundRects(terrain, camera):
    hitbox = pygame.Rect(x+4, 226, 24, 32)
    for i in range(len(terrain)):
        y = terrain[i].y + 600 + camera
        terrain[i].rect = pygame.Rect(0,0,32,32)
        if not terrain[i].mined:
            terrain[i].rect = pygame.Rect(terrain[i].x, y, 32, 32)  # This line causes the hitboxes to appear where the terrain is visually
        #pygame.draw.rect(screen, (0, 255, 0), terrain[i].rect)
        collision = hitbox.colliderect(terrain[i].rect)
        if collision:
            break


    
print(len(terrain)/20)
hitbox = pygame.Rect(x+4, 224, 24, 32)
digSquare = pygame.Rect(x, 224, 8, 8)
while running:
    # BG
    screen.fill((112, 224, 255)) # Default
    if y < -742:
        screen.fill((107, 186, 209)) # TRANSITION 1: DEFAULT -> CAVE 1
    if y < -774:
        screen.fill((118, 169, 184)) # TRANSITION 2: DEFAULT -> CAVE 1
    if y < -806:
        screen.fill((118, 139, 145)) # TRANSITION 3: DEFAULT -> CAVE 1
    if y < -838:
        screen.fill((122, 122, 122)) # CAVE 1


    
    hitbox = pygame.Rect(x+4, 226, 24, 32)
    redoGroundRects(terrain, cam_y)

    draw_terrain(screen, terrain, cam_y)
    for i in range(len(terrain)): # Breaking of Blocks
        collision = digSquare.colliderect(terrain[i].rect)
        if collision and keyAnyPressed:
            terrain[i].health -= digPower * delta_time
            if random.randint(1,20) == 1:
                digNoises[random.randint(0,2)].play()
                print("sound")
            if terrain[i].health <= 0:
                terrain[i].mined = True
                money += terrain[i].value
                health -= terrain[i].damage
                if terrain[i].extra != '' and terrain[i].extra != 'Grass':
                    oreBreak.play()
                elif random.randint(1,3) == 1:
                    rockBreak.play()

    speedY += gravity
    if speedY > jumpStrength:
        speedY = jumpStrength

    y -= speedY * delta_time
    collision = collide(x)
    if not collision:
        jumpable = False
    if collision:
        if not speedY < 0:
            jumpable = True
        while collision:
            if speedY < 0:
                #for i in terrain:
                    #i.y -= 1
                y -= 1
            else:
                #for i in terrain:
                    #i.y += 1
                y += 1
            cam_y = y
            redoGroundRects(terrain, cam_y)
            collision = collide(x)
        speedY = 0
        #for i in terrain:
            #i.y -= 1
        y -= 1

    screen.blit(player, (x, 223))
    screen.blit(drill, (x, 223))

    cam_y = y

    playerX = font.render(f"X: {x}", True, (255,255,255))
    velY = font.render(f"Vertical Velocity: {speedY}", True, (255,255,255))
    playerY = font.render(f"Y: {y}", True, (255,255,255))
    moneyText = font.render(f"${money}", True, (255,255,0))
    healthText = font.render(f"{health}/{maxHealth}", True, (255,0,0))

    hitbox = pygame.Rect(x+4, 224, 24, 32)
    if debug:
        for i in range(len(terrain)):
            pygame.draw.rect(screen, (0, 255, 0), terrain[i].rect)
        pygame.draw.rect(screen, (255, 0, 0), hitbox)
        pygame.draw.rect(screen, (0, 0, 255), digSquare)
        screen.blit(playerX, (4,64))
        screen.blit(playerY, (4,94))
        screen.blit(velY, (4,124))

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
            if event.key == pygame.K_SPACE:
                speedY = 0
                y = -640
                cam_y = y
                x = 304
            if event.key == pygame.K_ESCAPE:
                if shopOverlay:
                    shopOverlay = False
                    controlls = "move"
                else:
                    shopOverlay = True
                    controlls = "shop"

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
        
    
    if controlls == "move":
        if keyDPressed:
            x += moveSpeed * delta_time
            collision = collide(x)
            digSquare = pygame.Rect(x+24, 224+8, 16, 16)
            while collision:
                x -= 1
                collision = collide(x)
            keyAnyPressed = True
            player = pygame.transform.rotate(player, degrees*-1)
            drill = pygame.transform.rotate(drill, degrees*-1)
            degrees = -90
            player = pygame.transform.rotate(player, degrees)
            drill = pygame.transform.rotate(drill, degrees)

        if keyAPressed:
            x -= moveSpeed * delta_time
            collision = collide(x)
            digSquare = pygame.Rect(x-8, 224+8, 16, 16)
            while collision:
                x += 1
                collision = collide(x)
            keyAnyPressed = True
            player = pygame.transform.rotate(player, degrees*-1)
            drill = pygame.transform.rotate(drill, degrees*-1)
            degrees = 90
            player = pygame.transform.rotate(player, degrees)
            drill = pygame.transform.rotate(drill, degrees)

        if keyWPressed:
            digSquare = pygame.Rect(x+8, 224-8, 16, 16)
            if jumpable:
                speedY -= jumpStrength
            keyAnyPressed = True
            player = pygame.transform.rotate(player, degrees*-1)
            drill = pygame.transform.rotate(drill, degrees*-1)
            degrees = 0
            player = pygame.transform.rotate(player, degrees)
            drill = pygame.transform.rotate(drill, degrees)
        if keySPressed:
            digSquare = pygame.Rect(x+8, 224+24, 16, 16)
            keyAnyPressed = True
            player = pygame.transform.rotate(player, degrees*-1)
            drill = pygame.transform.rotate(drill, degrees*-1)
            degrees = 180
            player = pygame.transform.rotate(player, degrees)
            drill = pygame.transform.rotate(drill, degrees)

    if x < 0:
        x = 0
    if x > 608:
        x = 608
    if y < (world_depth+10)*64*-1:
        y = -200
        print("loop")
    if health < 1:
        print(deathTimer)
        keyAnyPressed = False
        controlls = "dead"
        money = math.floor(money * moneyLoss)
        if deathTimer == 0:
            deathTimer = 3
        else:
            deathTimer -= 1*delta_time
            if deathTimer <= 0:
                deathTimer = 0
                health = maxHealth
                controlls = "move"
                x = 304
                y = -640

    shopTemp = pygame.Rect(32, 32, 576, 416)
    shopTempOutline = pygame.Rect(30, 30, 580, 420)
    if shopOverlay:
        pygame.draw.rect(screen, (50, 50, 50), shopTempOutline)
        pygame.draw.rect(screen, (122, 122, 122), shopTemp)
        screen.blit(moneyText, (36, 36))
    else:
        screen.blit(moneyText, (4,34))
    screen.blit(heart, (4,4))
    screen.blit(healthText, (36, 10))

    # end stuff
    pygame.display.flip()
    delta_time = clock.tick(60) / 1000
    delta_time = max(0.001, min((0.1, delta_time)))

pygame.quit()