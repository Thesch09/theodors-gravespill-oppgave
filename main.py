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
deltaTime = 0.1
shopOverlay = False
# Debug
debugUsed = False
debugDig = False
debugHitbox = False
debugMovement = False
debugHealth = False
debugJump = False
debugMoney = False
# Player VARs
x = 304
y = -640
speedY = 0
moveSpeed = 80
jumpStrength = 150
jumpable = False
digPower = 30
money = 0
uniqueOres = 0
maxHealth = 25
health = maxHealth
moneyLoss = 0.0 # Float. 0 is lose all, 1 is keep all
deathTimer = 0
controlls = "move"
depth = 0
playerHasUniqueMoneyBag = False
playerHasUniqueHeart = False
playerHasUniquePickaxe = 0.0 # Float so it scales slower
# Player movement VARs
keyDPressed = False
keyAPressed = False
keyWPressed = False
keySPressed = False
keyAnyPressed = False
keySpacePressed = False
degrees = 0
shopCursorSlot = 0
shopTab = ["upgrades", "unique", "stats", "stats 2","drill", "hull"]
shopTabId = 0
moveShop = 0
# End of player VARs
cam_y = y
renderDistance = 10
collision = False
gravity = 200
world_depth = 1250
font = pygame.font.Font(None, size=30)
recentlyBroken = font.render("nothing", True, (255,255,255))
brokenCooldown = 0

# These are if Trues so that I can hide them in editor
if True: # Breakage
    break1 = pygame.image.load('img/gui/break1.png').convert_alpha()
    break1 = pygame.transform.scale(break1,
                                (break1.get_width() * 2,
                                break1.get_height() * 2))
    break2 = pygame.image.load('img/gui/break2.png').convert_alpha()
    break2 = pygame.transform.scale(break2,
                                (break2.get_width() * 2,
                                break2.get_height() * 2))
    break3 = pygame.image.load('img/gui/break3.png').convert_alpha()
    break3 = pygame.transform.scale(break3,
                                (break3.get_width() * 2,
                                break3.get_height() * 2))
if True: # Drills
    drillGrey = pygame.image.load('img/drill/drillGrey.png').convert_alpha()
    drillGrey = pygame.transform.scale(drillGrey,
                                (drillGrey.get_width() * 2,
                                drillGrey.get_height() * 2))
    drillBlue = pygame.image.load("img/drill/drillBlue.png").convert_alpha
    drillBlue = pygame.transform.scale(drillBlue,
                                (drillBlue.get_width() * 2,
                                drillBlue.get_height() * 2))
if True: # Hulls
    hullOrange = pygame.image.load('img/hull/hullOrange.png').convert_alpha()
    hullOrange = pygame.transform.scale(hullOrange,
                                (hullOrange.get_width() * 2,
                                hullOrange.get_height() * 2))
    hullRed = pygame.image.load('img/hull/hullRed.png').convert_alpha()
    hullRed = pygame.transform.scale(hullRed,
                                (hullRed.get_width() * 2,
                                hullRed.get_height() * 2))
if True: # Tiles
    dirt = pygame.image.load('img/tiles/dirtV3.png').convert_alpha()
    dirt = pygame.transform.scale(dirt,
                                (dirt.get_width() * 2,
                                dirt.get_height() * 2))
    dirtBackground = pygame.image.load('img/tiles/dirtBackground.png').convert_alpha()
    dirtBackground = pygame.transform.scale(dirtBackground,
                                (dirtBackground.get_width() * 2,
                                dirtBackground.get_height() * 2))
    grass = pygame.image.load('img/tiles/grass.png').convert_alpha()
    grass = pygame.transform.scale(grass,
                                (grass.get_width() * 2,
                                grass.get_height() * 2))
    grassBackground = pygame.image.load('img/tiles/grassBackground.png').convert_alpha()
    grassBackground = pygame.transform.scale(grassBackground,
                                (grassBackground.get_width() * 2,
                                grassBackground.get_height() * 2))
    stone = pygame.image.load('img/tiles/stoneV2.png').convert_alpha()
    stone = pygame.transform.scale(stone,
                                (stone.get_width() * 2,
                                stone.get_height() * 2))
    stoneBackground = pygame.image.load('img/tiles/stoneBackground.png').convert_alpha()
    stoneBackground = pygame.transform.scale(stoneBackground,
                                (stoneBackground.get_width() * 2,
                                stoneBackground.get_height() * 2))
    bluestone = pygame.image.load('img/tiles/bluestone.png').convert_alpha()
    bluestone = pygame.transform.scale(bluestone,
                                (bluestone.get_width() * 2,
                                bluestone.get_height() * 2))
    bluestoneBackground = pygame.image.load('img/tiles/bluestoneBackground.png').convert_alpha()
    bluestoneBackground = pygame.transform.scale(bluestoneBackground,
                                (bluestoneBackground.get_width() * 2,
                                bluestoneBackground.get_height() * 2))
    redstone = pygame.image.load('img/tiles/redstone.png').convert_alpha()
    redstone = pygame.transform.scale(redstone,
                                (redstone.get_width() * 2,
                                redstone.get_height() * 2))
    redstoneBackground = pygame.image.load('img/tiles/redstoneBackground.png').convert_alpha()
    redstoneBackground = pygame.transform.scale(redstoneBackground,
                                (redstoneBackground.get_width() * 2,
                                redstoneBackground.get_height() * 2))
    spaceStone = pygame.image.load('img/tiles/spaceStone.png').convert_alpha()
    spaceStone = pygame.transform.scale(spaceStone,
                                (spaceStone.get_width() * 2,
                                spaceStone.get_height() * 2))
    spaceStoneBackground = pygame.image.load('img/tiles/spaceStoneBackground.png').convert_alpha()
    spaceStoneBackground = pygame.transform.scale(spaceStoneBackground,
                                (spaceStoneBackground.get_width() * 2,
                                spaceStoneBackground.get_height() * 2))
    space = pygame.image.load('img/tiles/space.png').convert_alpha()
    space = pygame.transform.scale(space,
                                (space.get_width() * 2,
                                space.get_height() * 2))
    spaceBackground = pygame.image.load('img/tiles/spaceBackground.png').convert_alpha()
    spaceBackground = pygame.transform.scale(spaceBackground,
                                (spaceBackground.get_width() * 2,
                                spaceBackground.get_height() * 2))
    bloodstone = pygame.image.load('img/tiles/bloodstoneV2.png').convert_alpha()
    bloodstone = pygame.transform.scale(bloodstone,
                                (bloodstone.get_width() * 2,
                                bloodstone.get_height() * 2))
    bloodstoneBackground = pygame.image.load('img/tiles/bloodstoneBackground.png').convert_alpha()
    bloodstoneBackground = pygame.transform.scale(bloodstoneBackground,
                                (bloodstoneBackground.get_width() * 2,
                                bloodstoneBackground.get_height() * 2))
    abyssmarine = pygame.image.load('img/tiles/abyssmarine.png').convert_alpha()
    abyssmarine = pygame.transform.scale(abyssmarine,
                                (abyssmarine.get_width() * 2,
                                abyssmarine.get_height() * 2))
    abyssmarineBackground = pygame.image.load('img/tiles/abyssmarineBackground.png').convert_alpha()
    abyssmarineBackground = pygame.transform.scale(abyssmarineBackground,
                                (abyssmarineBackground.get_width() * 2,
                                abyssmarineBackground.get_height() * 2))
    magma = pygame.image.load('img/tiles/magma.png').convert_alpha()
    magma = pygame.transform.scale(magma,
                                (magma.get_width() * 2,
                                magma.get_height() * 2))
    magmaBackground = pygame.image.load('img/tiles/magmaBackground.png').convert_alpha()
    magmaBackground = pygame.transform.scale(magmaBackground,
                                (magmaBackground.get_width() * 2,
                                magmaBackground.get_height() * 2))
if True: # Ores
    iron = pygame.image.load('img/ores/iron.png').convert_alpha()
    iron = pygame.transform.scale(iron,
                                (iron.get_width() * 2,
                                iron.get_height() * 2))
    copper = pygame.image.load('img/ores/copper.png').convert_alpha()
    copper = pygame.transform.scale(copper,
                                (copper.get_width() * 2,
                                copper.get_height() * 2))
    diamond = pygame.image.load('img/ores/diamond.png').convert_alpha()
    diamond = pygame.transform.scale(diamond,
                                (diamond.get_width() * 2,
                                diamond.get_height() * 2))
    bismuth = pygame.image.load('img/ores/bismuth.png').convert_alpha()
    bismuth = pygame.transform.scale(bismuth,
                                (bismuth.get_width() * 2,
                                bismuth.get_height() * 2))
    coal = pygame.image.load('img/ores/coal.png').convert_alpha()
    coal = pygame.transform.scale(coal,
                                (coal.get_width() * 2,
                                coal.get_height() * 2))
    rainbowite = pygame.image.load('img/ores/rainbowite.png').convert_alpha()
    rainbowite = pygame.transform.scale(rainbowite,
                                (rainbowite.get_width() * 2,
                                rainbowite.get_height() * 2))
    uniqueOre = pygame.image.load('img/ores/uniqueOre.png').convert_alpha()
    uniqueOre = pygame.transform.scale(uniqueOre,
                                (uniqueOre.get_width() * 2,
                                uniqueOre.get_height() * 2))
    uniqueOre2 = pygame.image.load('img/ores/uniqueOre2.png').convert_alpha()
    uniqueOre2 = pygame.transform.scale(uniqueOre2,
                                (uniqueOre2.get_width() * 2,
                                uniqueOre2.get_height() * 2))
    uniqueOre3 = pygame.image.load('img/ores/uniqueOre3.png').convert_alpha()
    uniqueOre3 = pygame.transform.scale(uniqueOre3,
                                (uniqueOre3.get_width() * 2,
                                uniqueOre3.get_height() * 2))
    star = pygame.image.load('img/ores/star.png').convert_alpha()
    star = pygame.transform.scale(star,
                                (star.get_width() * 2,
                                star.get_height() * 2))
    bigStar = pygame.image.load('img/ores/starBig.png').convert_alpha()
    bigStar = pygame.transform.scale(bigStar,
                                (bigStar.get_width() * 2,
                                bigStar.get_height() * 2))
    gold = pygame.image.load('img/ores/gold.png').convert_alpha()
    gold = pygame.transform.scale(gold,
                                (gold.get_width() * 2,
                                gold.get_height() * 2))
    lapisLazuli = pygame.image.load('img/ores/lapisLazuli.png').convert_alpha()
    lapisLazuli = pygame.transform.scale(lapisLazuli,
                                (lapisLazuli.get_width() * 2,
                                lapisLazuli.get_height() * 2))
    eyeBlue = pygame.image.load('img/ores/eyeBlue.png').convert_alpha()
    eyeBlue = pygame.transform.scale(eyeBlue,
                                (eyeBlue.get_width() * 2,
                                eyeBlue.get_height() * 2))
    eyeBlueSquint = pygame.image.load('img/ores/eyeBlueSquint.png').convert_alpha()
    eyeBlueSquint = pygame.transform.scale(eyeBlueSquint,
                                (eyeBlueSquint.get_width() * 2,
                                eyeBlueSquint.get_height() * 2))
    eyeGreen = pygame.image.load('img/ores/eyeGreen.png').convert_alpha()
    eyeGreen = pygame.transform.scale(eyeGreen,
                                (eyeGreen.get_width() * 2,
                                eyeGreen.get_height() * 2))
    eyeGreenSquint = pygame.image.load('img/ores/eyeGreenSquint.png').convert_alpha()
    eyeGreenSquint = pygame.transform.scale(eyeGreenSquint,
                                (eyeGreenSquint.get_width() * 2,
                                eyeGreenSquint.get_height() * 2))
    eyeRed = pygame.image.load('img/ores/eyeRed.png').convert_alpha()
    eyeRed = pygame.transform.scale(eyeRed,
                                (eyeRed.get_width() * 2,
                                eyeRed.get_height() * 2))
    eyeRedSquint = pygame.image.load('img/ores/eyeRedSquint.png').convert_alpha()
    eyeRedSquint = pygame.transform.scale(eyeRedSquint,
                                (eyeRedSquint.get_width() * 2,
                                eyeRedSquint.get_height() * 2))
    mouth = pygame.image.load('img/ores/mouth.png').convert_alpha()
    mouth = pygame.transform.scale(mouth,
                                (mouth.get_width() * 2,
                                mouth.get_height() * 2))
if True: # Upgrades
    heart = pygame.image.load('img/upgrades/heart.png').convert_alpha()
    heart = pygame.transform.scale(heart,
                                (heart.get_width() * 2,
                                heart.get_height() * 2))
    heartUnique = pygame.image.load('img/upgrades/heartUnique.png').convert_alpha()
    heartUnique = pygame.transform.scale(heartUnique,
                                (heartUnique.get_width() * 2,
                                heartUnique.get_height() * 2))
    digPowerGUI = pygame.image.load('img/upgrades/digPower.png').convert_alpha()
    digPowerGUI = pygame.transform.scale(digPowerGUI,
                                (digPowerGUI.get_width() * 2,
                                digPowerGUI.get_height() * 2))
    digPowerUnique = pygame.image.load('img/upgrades/digPowerUnique.png').convert_alpha()
    digPowerUnique = pygame.transform.scale(digPowerUnique,
                                (digPowerUnique.get_width() * 2,
                                digPowerUnique.get_height() * 2))
    jumpStrengthGUI = pygame.image.load('img/upgrades/jumpStrength.png').convert_alpha()
    jumpStrengthGUI = pygame.transform.scale(jumpStrengthGUI,
                                (jumpStrengthGUI.get_width() * 2,
                                jumpStrengthGUI.get_height() * 2))
    jumpStrengthUnique = pygame.image.load('img/upgrades/jumpStrengthUnique.png').convert_alpha()
    jumpStrengthUnique = pygame.transform.scale(jumpStrengthUnique,
                                (jumpStrengthUnique.get_width() * 2,
                                jumpStrengthUnique.get_height() * 2))
    moneyBag = pygame.image.load('img/upgrades/moneyBag.png').convert_alpha()
    moneyBag = pygame.transform.scale(moneyBag,
                                (moneyBag.get_width() * 2,
                                moneyBag.get_height() * 2))
    moneyBagUnique = pygame.image.load('img/upgrades/moneyBagUnique.png').convert_alpha()
    moneyBagUnique = pygame.transform.scale(moneyBagUnique,
                                (moneyBagUnique.get_width() * 2,
                                moneyBagUnique.get_height() * 2))
    moveSpeedGUI = pygame.image.load('img/upgrades/moveSpeed.png').convert_alpha()
    moveSpeedGUI = pygame.transform.scale(moveSpeedGUI,
                                (moveSpeedGUI.get_width() * 2,
                                moveSpeedGUI.get_height() * 2))
    moveSpeedUnique = pygame.image.load('img/upgrades/moveSpeedUnique.png').convert_alpha()
    moveSpeedUnique = pygame.transform.scale(moveSpeedUnique,
                                (moveSpeedUnique.get_width() * 2,
                                moveSpeedUnique.get_height() * 2))
if True: # Shop buttons and titles
    shopBuy = pygame.image.load('img/gui/shopBuy.png').convert_alpha()
    shopBuy = pygame.transform.scale(shopBuy,
                                (shopBuy.get_width() * 2,
                                shopBuy.get_height() * 2))
    shopBuyUnique = pygame.image.load('img/gui/shopBuyUnique.png').convert_alpha()
    shopBuyUnique = pygame.transform.scale(shopBuyUnique,
                                (shopBuyUnique.get_width() * 2,
                                shopBuyUnique.get_height() * 2))
    shopPoor = pygame.image.load('img/gui/shopPoor.png').convert_alpha()
    shopPoor = pygame.transform.scale(shopPoor,
                                (shopPoor.get_width() * 2,
                                shopPoor.get_height() * 2))
    shopButtonSelect = pygame.image.load('img/gui/shopButtonSelect.png').convert_alpha()
    shopButtonSelect = pygame.transform.scale(shopButtonSelect,
                                (shopButtonSelect.get_width() * 2,
                                shopButtonSelect.get_height() * 2))
    drillSkins = pygame.image.load('img/gui/drillSkins.png').convert_alpha()
    drillSkins = pygame.transform.scale(drillSkins,
                                (drillSkins.get_width() * 2,
                                drillSkins.get_height() * 2))
    hullSkins = pygame.image.load('img/gui/hullSkins.png').convert_alpha()
    hullSkins = pygame.transform.scale(hullSkins,
                                (hullSkins.get_width() * 2,
                                hullSkins.get_height() * 2))
    upgrades = pygame.image.load('img/gui/upgrades.png').convert_alpha()
    upgrades = pygame.transform.scale(upgrades,
                                (upgrades.get_width() * 2,
                                upgrades.get_height() * 2))
    upgradesUnique = pygame.image.load('img/gui/upgradesUnique.png').convert_alpha()
    upgradesUnique = pygame.transform.scale(upgradesUnique,
                                (upgradesUnique.get_width() * 2,
                                upgradesUnique.get_height() * 2))
    stats = pygame.image.load('img/gui/stats.png').convert_alpha()
    stats = pygame.transform.scale(stats,
                                (stats.get_width() * 2,
                                stats.get_height() * 2))
    stats2 = pygame.image.load('img/gui/stats2.png').convert_alpha()
    stats2 = pygame.transform.scale(stats2,
                                (stats2.get_width() * 2,
                                stats2.get_height() * 2))
    shopVisual = pygame.image.load('img/gui/shopVisual.png').convert_alpha()
    shopVisual = pygame.transform.scale(shopVisual,
                                (shopVisual.get_width() * 2,
                                shopVisual.get_height() * 2))
    shopEquip = pygame.image.load('img/gui/shopEquip.png').convert_alpha()
    shopEquip = pygame.transform.scale(shopEquip,
                                (shopEquip.get_width() * 2,
                                shopEquip.get_height() * 2))
if True: # Debug icons
    debugIcon = pygame.image.load('img/debug/debug.png').convert_alpha()
    debugIcon = pygame.transform.scale(debugIcon,
                                (debugIcon.get_width() * 2,
                                debugIcon.get_height() * 2))
    debugHealthIcon = pygame.image.load('img/debug/debugHealth.png').convert_alpha()
    debugHealthIcon = pygame.transform.scale(debugHealthIcon,
                                (debugHealthIcon.get_width() * 2,
                                debugHealthIcon.get_height() * 2))
    debugHitboxIcon = pygame.image.load('img/debug/debugHitbox.png').convert_alpha()
    debugHitboxIcon = pygame.transform.scale(debugHitboxIcon,
                                (debugHitboxIcon.get_width() * 2,
                                debugHitboxIcon.get_height() * 2))
    debugJumpIcon = pygame.image.load('img/debug/debugJump.png').convert_alpha()
    debugJumpIcon = pygame.transform.scale(debugJumpIcon,
                                (debugJumpIcon.get_width() * 2,
                                debugJumpIcon.get_height() * 2))
    debugMoneyIcon = pygame.image.load('img/debug/debugMoney.png').convert_alpha()
    debugMoneyIcon = pygame.transform.scale(debugMoneyIcon,
                                (debugMoneyIcon.get_width() * 2,
                                debugMoneyIcon.get_height() * 2))
    debugStatsIcon = pygame.image.load('img/debug/debugStats.png').convert_alpha()
    debugStatsIcon = pygame.transform.scale(debugStatsIcon,
                                (debugStatsIcon.get_width() * 2,
                                debugStatsIcon.get_height() * 2))

drill = drillGrey
player = hullOrange

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
def draw_terrain(screen, terrain, camera, depth):
    for i in terrain:
        y = i.y + 600 + camera

        if not i.mined and i.deep + renderDistance > abs(depth) and i.deep - renderDistance < abs(depth): # Not mined
            
            # Rock type
            if i.ore == 'Stone':
                screen.blit(stone, (i.x, y))
            if i.ore == 'Dirt':
                screen.blit(dirt, (i.x, y))
            if i.ore == 'Bluestone':
                screen.blit(bluestone, (i.x, y))
            if i.ore == 'Redstone':
                screen.blit(redstone, (i.x, y))
            if i.ore == 'Magma':
                screen.blit(magma, (i.x, y))
            if i.ore == 'Space':
                screen.blit(space, (i.x, y))
            if i.ore == 'Space Stone':
                screen.blit(spaceStone, (i.x, y))
            if i.ore == 'Abyssmarine':
                screen.blit(abyssmarine, (i.x, y))
            if i.ore == 'Bloodstone':
                screen.blit(bloodstone, (i.x, y))

            # Ore type
            if i.extra == 'Grass':
                screen.blit(grass, (i.x, y))
            if i.extra == 'Iron':
                screen.blit(iron, (i.x, y))
            if i.extra == 'Copper':
                screen.blit(copper, (i.x, y))
            if i.extra == 'Coal':
                screen.blit(coal, (i.x, y))
            if i.extra == 'Diamond':
                screen.blit(diamond, (i.x, y))
            if i.extra == 'Bismuth':
                screen.blit(bismuth, (i.x, y))
            if i.extra == 'Rainbowite':
                screen.blit(rainbowite, (i.x, y))
            if i.extra == 'Unique Ore':
                screen.blit(uniqueOre, (i.x, y))
            if i.extra == 'Big Unique Ore':
                screen.blit(uniqueOre2, (i.x, y))
            if i.extra == 'Large Unique Ore':
                screen.blit(uniqueOre3, (i.x, y))
            if i.extra == 'Star':
                screen.blit(star, (i.x, y))
            if i.extra == 'Large Star':
                screen.blit(bigStar, (i.x, y))
            if i.extra == 'Gold':
                screen.blit(gold, (i.x, y))
            if i.extra == 'Lapis Lazuli':
                screen.blit(lapisLazuli, (i.x, y))
            if i.extra == 'Blue Eye':
                screen.blit(eyeBlue, (i.x, y))
            if i.extra == 'Squinting Blue Eye':
                screen.blit(eyeBlueSquint, (i.x, y))
            if i.extra == 'Green Eye':
                screen.blit(eyeGreen, (i.x, y))
            if i.extra == 'Squinting Green Eye':
                screen.blit(eyeGreenSquint, (i.x, y))
            if i.extra == 'Red Eye':
                screen.blit(eyeRed, (i.x, y))
            if i.extra == 'Squinting Red Eye':
                screen.blit(eyeRedSquint, (i.x, y))
            if i.extra == "Mouth":
                screen.blit(mouth, (i.x, y))

            # Check if it's broken
            if i.health < i.hardness/4:
                screen.blit(break3, (i.x, y))
            if i.health < i.hardness/4*2:
                screen.blit(break2, (i.x, y))
            if i.health < i.hardness/4*3:
                screen.blit(break1, (i.x, y))
        
        if i.mined and i.deep + renderDistance > abs(depth) and i.deep - renderDistance < abs(depth): # Mined
            if i.ore == 'Dirt':
                screen.blit(dirtBackground, (i.x, y))
            if i.ore == 'Stone':
                screen.blit(stoneBackground, (i.x, y))
            if i.ore == 'Bluestone':
                screen.blit(bluestoneBackground, (i.x, y))
            if i.ore == 'Redstone':
                screen.blit(redstoneBackground, (i.x, y))
            if i.ore == 'Bloodstone':
                screen.blit(bloodstoneBackground, (i.x, y))
            if i.ore == 'Space Stone':
                screen.blit(spaceStoneBackground, (i.x, y))
            if i.ore == 'Abyssmarine':
                screen.blit(abyssmarineBackground, (i.x, y))
            if i.ore == 'Space':
                screen.blit(spaceBackground, (i.x, y))
            if i.ore == 'Magma':
                screen.blit(magmaBackground, (i.x, y))

            # Check for grass
            if i.extra == 'Grass':
                screen.blit(grassBackground, (i.x, y))

def collide(playerX):
    hitbox = pygame.Rect(playerX+4, 224, 24, 32)
    colly = 1
    for i in range(len(terrain)):
        collision = hitbox.colliderect(terrain[i].rect)
        if collision:
            return collision
def redoGroundRects(terrain, camera, depth):
    hitbox = pygame.Rect(x+4, 226, 24, 32)
    for i in range(len(terrain)):
        if terrain[i].deep + renderDistance > abs(depth) and terrain[i].deep - renderDistance < abs(depth):
            y = terrain[i].y + 600 + camera
            terrain[i].rect = pygame.Rect(0,0,32,32)
            if not terrain[i].mined:
                terrain[i].rect = pygame.Rect(terrain[i].x, y, 32, 32)  # This line causes the hitboxes to appear where the terrain is visually
            #pygame.draw.rect(screen, (0, 255, 0), terrain[i].rect)
            collision = hitbox.colliderect(terrain[i].rect)
            if collision:
                break

class shopItem:
    def __init__(self, cost, unique, flavour = str, sprite = None, tab = str, slot = None, priceIncrease = None, maxPrice = None, beyondIncrease = None, trueMaxPrice = None, maxPurchase = None):
        self.cost = cost
        self.unique = unique
        self.flavour = flavour
        self.sprite = sprite
        self.tab = tab
        self.slot = slot
        self.priceIncrease = priceIncrease
        self.maxPrice = maxPrice
        self.beyondIncrease = beyondIncrease
        self.trueMaxPrice = trueMaxPrice
        self.maxPurchase = maxPurchase

class cosmetic:
    def __init__(self, cost, flavour, sprite, tab, slot, owned = False):
        self.cost = cost
        self.flavour = flavour
        self.sprite = sprite
        self.owned = owned
        self.tab = tab
        self.slot = slot

# These are also if Trues so that I can hide them in editor
if True: # Upgrades
    heartShop = shopItem(100, False, "Increases maximum HP by 5.", heart, "upgrades", 0, 10, 1000000, 100000, 5000000)
    digPowerShop = shopItem(25, False, "Increases dig power by 5.", digPowerGUI, "upgrades", 1, 3, 500000, 30000, 100000)
    jumpStrengthShop = shopItem(75, False, "Increases jump strength by 5.", jumpStrengthGUI, "upgrades", 2, 2.5, 750000, 50000, 2500000)
    moveSpeedShop = shopItem(50, False, "Increases horisontal speed by 5.", moveSpeedGUI, "upgrades", 3, 500000, 30000, 100000)
    moneyBagShop = shopItem(500, False, "Saves 1% of money on death.", moneyBag, "upgrades", 4, 2.5, 10000, 10000, 1000000, 50)
if True: # Unique Upgrades
    heartUniqueShop = shopItem(2, True, "Increases maximum HP by 15.", heartUnique, "unique", 0, 5, 5000, 500, 10000)
    digPowerUniqueShop = shopItem(5, True, "Increases dig power by 20.", digPowerUnique, "unique", 1, 3, 1000, 750, 10000)
    jumpStrengthUniqueShop = shopItem(3, True, "Increases jump strength by 15.", jumpStrengthUnique, "unique", 2, 2.5, 3000, 300, 30000)
    moveSpeedUniqueShop = shopItem(5, True, "Increases horisontal speed by 15.", moveSpeedUnique, "unique", 3, 3, 1000, 100, 10000)
    moneyBagUniqueShop = shopItem(10, True, "Saves 5% of money on death.", moneyBagUnique, "unique", 4, 2.5, 5000, 100, 1000000, 5)
if True: # Drill skins
    drillGreyShop = cosmetic(0, "The classic drill.", drillGrey, "drill", 0, True)


shop = [heartShop, digPowerShop, jumpStrengthShop, moveSpeedShop, moneyBagShop, heartUniqueShop, digPowerUniqueShop, jumpStrengthUniqueShop, moveSpeedUniqueShop, moneyBagUniqueShop, drillGreyShop]

print(len(terrain)/20)
hitbox = pygame.Rect(x+4, 224, 24, 32)
digSquare = pygame.Rect(x, 224, 8, 8)
while running:
    # BG
    if health < 1:
        screen.fill((122, 0, 0))
    else:
        screen.fill((137, 210, 255)) # Default
        if y < -40932:
            screen.fill((29, 30, 54)) # TRANSITION 1: SPACE -> DEFAULT
        if y < -100:
            screen.fill((69, 92, 125)) # TRANSITION 2: SPACE -> DEFAULT
        if y < -742:
            screen.fill((139, 182, 210)) # TRANSITION 1: DEFAULT -> CAVE 1
        if y < -774:
            screen.fill((138, 172, 194)) # TRANSITION 2: DEFAULT -> CAVE 1
        if y < -806:
            screen.fill((135, 137, 138)) # CAVE 1
        if y < -3000:
            screen.fill((112, 124, 131)) # TRANSITION 1: CAVE 1 -> CAVE 2
        if y < -3032:
            screen.fill((96, 119, 132)) # TRANSITION 2: CAVE 1 -> CAVE 2
        if y < -3064:
            screen.fill((79, 112, 132)) # CAVE 2
        if y < -5398:
            screen.fill((88, 101, 117)) # TRANSITION 1: CAVE 2 -> CAVE 3
        if y < -5430:
            screen.fill((105, 88, 94)) # TRANSITION 2: CAVE 2 -> CAVE 3
        if y < -5462:
            screen.fill((112, 77, 79)) # CAVE 3
        if y < -10230:
            screen.fill((115, 67, 72)) # TRANSITION 1: CAVE 3 -> CAVE 4
        if y < -10262:
            screen.fill((115, 62, 72)) # TRANSITION 2: CAVE 3 -> CAVE 4
        if y < -10294:
            screen.fill((117, 57, 71)) # CAVE 4
        if y < -15030:
            screen.fill((103, 54, 74)) # TRANSITION 1: CAVE 4 -> CAVE 5
        if y < -15062:
            screen.fill((93, 54, 75)) # TRANSITION 2: CAVE 4 -> CAVE 5
        if y < -15094:
            screen.fill((69, 53, 80)) # CAVE 5
        if y < -24630:
            screen.fill((34, 34, 64)) # TRANSITION 1: CAVE 5 -> SPACE
        if y < -24662:
            screen.fill((24, 19, 44)) # TRANSITION 2: CAVE 5 -> SPACE
        if y < -24694:
            screen.fill((4, 0, 10)) # SPACE


    depth = math.floor(y/32)+23
    
    hitbox = pygame.Rect(x+4, 226, 24, 32)
    redoGroundRects(terrain, cam_y, depth)

    draw_terrain(screen, terrain, cam_y, depth)
    for i in range(len(terrain)): # Breaking of Blocks
        collision = digSquare.colliderect(terrain[i].rect)
        if collision and keyAnyPressed:
            if maxHealth > terrain[i].damage or debugHealth:
                terrain[i].health -= digPower * deltaTime
                if random.randint(1,20) == 1:
                    digNoises[random.randint(0,2)].play()
                    print("sound")
                if terrain[i].health <= 0:
                    terrain[i].mined = True
                    health -= terrain[i].damage
                    if terrain[i].extra == "":
                        recentlyBroken = font.render(f"{terrain[i].ore}", True, (255,255,255))
                    else:
                        recentlyBroken = font.render(f"{terrain[i].extra}", True, (255,255,255))
                    brokenCooldown = 1
                    moneyRepeat = 1
                    if playerHasUniquePickaxe > 0:
                        moneyRepeat += math.floor(playerHasUniquePickaxe)
                    if terrain[i].extra != '' and terrain[i].extra != 'Grass':
                        oreBreak.play()
                    elif random.randint(1,3) == 1:
                        rockBreak.play()
                    money += terrain[i].value * moneyRepeat
                    uniqueOres += terrain[i].uniqueOre * moneyRepeat
            else:
                recentlyBroken = font.render(f"Too weak! Need more Max HP", True, (255,255,255))
                brokenCooldown = 1

    brokenCooldown -= 1*deltaTime
    if brokenCooldown > 0:
        brokenX = 640-4-recentlyBroken.get_width()
        screen.blit(recentlyBroken, (brokenX,456))

    speedY += gravity * deltaTime
    if speedY > jumpStrength:
        speedY = jumpStrength

    y -= speedY * deltaTime
    collision = collide(x)
    if not collision:
        jumpable = False
    if collision:
        if not speedY < 0:
            jumpable = True
        while collision:
            if speedY < 0:
                y -= 1
            else:
                y += 1
            cam_y = y
            redoGroundRects(terrain, cam_y, depth)
            collision = collide(x)
        speedY = 0
        y -= 1

    screen.blit(player, (x, 223))
    screen.blit(drill, (x, 223))

    cam_y = y

    playerX = font.render(f"X: {x}", True, (255,255,255))
    velY = font.render(f"Vertical Velocity: {speedY}", True, (255,255,255))
    playerY = font.render(f"Y: {y}", True, (255,255,255))

    hitbox = pygame.Rect(x+4, 224, 24, 32)
    if debugHitbox:
        for i in range(len(terrain)):
            pygame.draw.rect(screen, (0, 255, 0), terrain[i].rect)
        pygame.draw.rect(screen, (255, 0, 0), hitbox)
        pygame.draw.rect(screen, (0, 0, 255), digSquare)
    if debugMovement:
        screen.blit(playerX, (4,94))
        screen.blit(playerY, (4,124))
        screen.blit(velY, (4,154))
    if debugHealth:
        health = maxHealth

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
            if event.key == pygame.K_SPACE and controlls == "move":
                speedY = 0
                y = -640
                cam_y = y
                redoGroundRects(terrain, cam_y, depth)
                draw_terrain(screen, terrain, cam_y, depth)
                x = 304
                health = maxHealth
            # Shop
            if event.key == pygame.K_SPACE and controlls == "shop":
                keySpacePressed = True
            if event.key == pygame.K_ESCAPE:
                if shopOverlay:
                    shopOverlay = False
                    controlls = "move"
                    keySpacePressed = False
                else:
                    shopOverlay = True
                    controlls = "shop"
                    shopCursorSlot = 0
                    shopTabId = 0
                    moveShop = 0
            # Debug
            if event.key == pygame.K_F1:
                if debugDig:
                    debugDig = False
                    digPower -= 90000
                    print("Insane dig power: Off")
                else:
                    debugDig = True
                    digPower += 90000
                    debugUsed = True
                    print("Insane dig power: On")
            if event.key == pygame.K_F2:
                if debugHitbox:
                    debugHitbox = False
                    print("Show hitboxes: Off")
                else:
                    debugHitbox = True
                    debugUsed = True
                    print("Show hitboxes: On")
            if event.key == pygame.K_F3:
                if debugMovement:
                    debugMovement = False
                    print("Movement info: Off")
                else:
                    debugMovement = True
                    debugUsed = True
                    print("Movement info: On")
            if event.key == pygame.K_F4:
                if debugHealth:
                    debugHealth = False
                    print("Infinite health: Off")
                else:
                    debugHealth = True
                    debugUsed = True
                    print("Infinite health: On")
            if event.key == pygame.K_F5:
                if debugJump:
                    jumpStrength -= 1000
                    debugJump = False
                    print("Insane jump power: Off")
                else:
                    debugJump = True
                    jumpStrength += 1000
                    debugUsed = True
                    print("Insane jump power: On")
            if event.key == pygame.K_F6:
                if debugMoney:
                    debugMoney = False
                    print("Infinite money: Off")
                else:
                    debugMoney = True
                    debugUsed = True
                    print("Infinite money: On")

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
            if event.key == pygame.K_SPACE and controlls == "shop":
                keySpacePressed = False
    
    moneyText = font.render(f"${money}", True, (255,255,0))
    uniqueOreText = font.render(f"UO: {uniqueOres}", True, (122,0,122))
    healthText = font.render(f"{health}/{maxHealth}", True, (255,0,0))
    depthText = font.render(f"Depth: {depth}", True, (255,255,255))
    shopTemp = pygame.Rect(32, 32, 576, 416)
    shopTempOutline = pygame.Rect(30, 30, 580, 420)
    if shopOverlay:
        pygame.draw.rect(screen, (50, 50, 50), shopTempOutline)
        pygame.draw.rect(screen, (122, 122, 122), shopTemp)
        if shopTab[shopTabId] == "upgrades":
            screen.blit(moneyText, (36, 36))
        elif shopTab[shopTabId] != "stats" and shopTab[shopTabId] != "stats 2":
            screen.blit(uniqueOreText, (36, 36))
    else:
        screen.blit(moneyText, (4,34))
        screen.blit(uniqueOreText, (4,64))
    screen.blit(heart, (4,4))
    screen.blit(healthText, (36, 10))
    screen.blit(depthText, (4, 456))

    keyAnyPressed = False
    if controlls == "move": # For movement, duh :) 
        if keyDPressed:
            x += moveSpeed * deltaTime
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
            x -= moveSpeed * deltaTime
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

    if controlls == "shop": # For when in the shop GUI

        if shopTab[shopTabId] == "drill":
            screen.blit(drillSkins, (240,32))
        if shopTab[shopTabId] == "upgrades":
            screen.blit(upgrades, (240,32))
        if shopTab[shopTabId] == "hull":
            screen.blit(hullSkins, (240,32))
        if shopTab[shopTabId] == "unique":
            screen.blit(upgradesUnique, (240,32))
        if shopTab[shopTabId] == "stats":
            screen.blit(stats, (240,32))
        if shopTab[shopTabId] == "stats 2":
            screen.blit(stats2, (240,32))

        for i in shop:
            shopText = font.render(f"{i.flavour} Cost: {i.cost}", True, (255,255,255))
            if i.tab == shopTab[shopTabId]:
                screen.blit(i.sprite, (32, 64+36*i.slot))
                screen.blit(shopText, (64, 72+36*i.slot))
                if not i.unique:
                    if money >= i.cost or debugMoney:
                        screen.blit(shopBuy, (540, 64+36*i.slot))
                        shopButtonHitbox = pygame.Rect(540, 64+36*i.slot, 64, 32)
                        shopCursorHitbox = pygame.Rect(540, 64+36*shopCursorSlot, 64, 32)
                        shopCollision = shopCursorHitbox.colliderect(shopButtonHitbox)
                        if shopCollision and keySpacePressed and moveShop <= 0:
                            if not debugMoney:
                                money -= i.cost
                            i.cost = math.floor(i.cost*i.priceIncrease)
                            if i.sprite == heart:
                                maxHealth += 5
                                health = maxHealth
                            if i.sprite == digPowerGUI:
                                digPower += 5
                            if i.sprite == jumpStrengthGUI:
                                jumpStrength += 5
                            if i.sprite == moveSpeedGUI:
                                moveSpeed += 5
                            if i.sprite == moneyBag:
                                moneyLoss += 0.01
                            print("oi")
                    else:
                        screen.blit(shopPoor, (540, 64+36*i.slot))
                if i.unique:
                    if uniqueOres >= i.cost or debugMoney:
                        screen.blit(shopBuyUnique, (540, 64+36*i.slot))
                        shopButtonHitbox = pygame.Rect(540, 64+36*i.slot, 64, 32)
                        shopCursorHitbox = pygame.Rect(540, 64+36*shopCursorSlot, 64, 32)
                        shopCollision = shopCursorHitbox.colliderect(shopButtonHitbox)
                        if shopCollision and keySpacePressed and moveShop <= 0:
                            if i.tab == "unique":
                                if not debugMoney:
                                    uniqueOres -= i.cost
                                i.cost = math.floor(i.cost*i.priceIncrease)
                                if i.sprite == heartUnique:
                                    maxHealth += 15
                                    health = maxHealth
                                    playerHasUniqueHeart = True
                                if i.sprite == digPowerUnique:
                                    digPower += 20
                                    playerHasUniquePickaxe += 0.5
                                if i.sprite == jumpStrengthUnique:
                                    jumpStrength += 15
                                if i.sprite == moveSpeedUnique:
                                    moveSpeed += 15
                                if i.sprite == moneyBagUnique:
                                    moneyLoss += 0.05
                                    playerHasUniqueMoneyBag = True
                                print("oi")
                    else:
                        screen.blit(shopPoor, (540, 64+36*i.slot))
            if shopTab[shopTabId] == "stats" and not i.unique:
                screen.blit(i.sprite, (32, 64+68*i.slot))
                if i.sprite == heart:
                    shopText = font.render(f"How much health you have before you die.", True, (255,255,255))
                    shopText2 = font.render(f"Value: {maxHealth}", True, (255,255,255))
                if i.sprite == digPowerGUI:
                    shopText = font.render(f"How much damage you deal to rocks.", True, (255,255,255))
                    shopText2 = font.render(f"Value: {digPower}", True, (255,255,255))
                if i.sprite == jumpStrengthGUI:
                    shopText = font.render(f"How high you jump and your max terminal velocity.", True, (255,255,255))
                    shopText2 = font.render(f"Value: {jumpStrength}", True, (255,255,255))
                if i.sprite == moveSpeedGUI:
                    shopText = font.render(f"How fast you move horizontally.", True, (255,255,255))
                    shopText2 = font.render(f"Value: {moveSpeed}", True, (255,255,255))
                if i.sprite == moneyBag:
                    shopText = font.render(f"How much money you save on death in %.", True, (255,255,255))
                    shopText2 = font.render(f"Value: {moneyLoss}", True, (255,255,255))
                screen.blit(shopText, (64, 72+68*i.slot))
                screen.blit(shopText2, (64, 104+68*i.slot))
            if shopTab[shopTabId] == "stats 2" and i.unique:
                screen.blit(i.sprite, (32, 64+68*i.slot))
                if i.sprite == heartUnique:
                    shopText = font.render(f"Having this upgrade gives you a chance to heal\nwhen you break rocks.", True, (255,255,255))
                if i.sprite == digPowerUnique:
                    shopText = font.render(f"Having this upgrade increases money from ores", True, (255,255,255))
                    shopText2 = font.render(f"Value: {playerHasUniquePickaxe}", True, (255,255,255))
                if i.sprite == jumpStrengthUnique:
                    shopText = font.render(f"This upgrade has no special ability.", True, (255,255,255))
                if i.sprite == moveSpeedUnique:
                    shopText = font.render(f"This upgrade has no special ability.", True, (255,255,255))
                if i.sprite == moneyBagUnique:
                    shopText = font.render(f"Having this upgrade ceilings saved money instead\nof flooring it. You save like $1", True, (255,255,255))
                screen.blit(shopText, (64, 72+68*i.slot))
                if i.sprite == digPowerUnique:
                    screen.blit(shopText2, (64, 104+68*i.slot))
        if shopTab[shopTabId] != "stats" and shopTab[shopTabId] != "stats 2":
            screen.blit(shopButtonSelect,(536,60+36*shopCursorSlot))
        if moveShop <= 0:
            if keySPressed:
                shopCursorSlot += 1
                moveShop = 1
            if keyWPressed:
                shopCursorSlot -= 1
                moveShop = 1
            if shopCursorSlot < 0:
                shopCursorSlot = 4
            if shopCursorSlot > 4:
                shopCursorSlot = 0
            if keyDPressed:
                shopTabId += 1
                shopCursorSlot = 0
                moveShop = 1
            if keyAPressed:
                shopTabId -= 1
                shopCursorSlot = 0
                moveShop = 1
            if shopTabId < 0:
                shopTabId = 5
            if shopTabId > 5:
                shopTabId = 0
        else:
            moveShop -= 2*deltaTime

    if x < 0:
        x = 0
    if x > 608:
        x = 608
    if y < (world_depth+50)*32*-1:
        y = -300
        print("loop")
    if y > -300:
        y = (world_depth+50)*32*-1
    
    if health < 1:
        print(deathTimer)
        keyAnyPressed = False
        controlls = "dead"
        if deathTimer == 0:
            deathTimer = 3
        else:
            deathTimer -= 1*deltaTime
            if deathTimer <= 0:
                if playerHasUniqueMoneyBag:
                    money = math.ceil(money *moneyLoss)
                else:
                    money = math.floor(money * moneyLoss)
                deathTimer = 0
                health = maxHealth
                controlls = "move"
                x = 304
                y = -640
                cam_y = y
                redoGroundRects(terrain, cam_y, depth)
    
    if debugUsed:
        screen.blit(debugIcon, (608, 0))
        if debugMovement:
            screen.blit(debugStatsIcon, (576, 0))
        if debugHitbox:
            screen.blit(debugHitboxIcon, (544, 0))
        if debugHealth:
            screen.blit(debugHealthIcon, (512, 0))
        if debugJump:
            screen.blit(debugJumpIcon, (480, 0))
        if debugMoney:
            screen.blit(debugMoneyIcon, (448, 0))

    # end stuff
    pygame.display.flip()
    deltaTime = clock.tick(60) / 1000
    deltaTime = max(0.001, min((0.1, deltaTime)))

pygame.quit()