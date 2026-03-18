import pygame
import math
import random
import time
import os
from terrain import make_terrain, saveTerrain, loadTerrain

pygame.init()

# Screen
flags = pygame.SCALED  |  pygame.RESIZABLE
screen = pygame.display.set_mode((640, 480), flags)

class playerClass:
    def __init__(self, debugUsed, moveSpeed, jumpStrength, digPower, money, uniqueOres, maxHealth, moneyLoss, hasUniqueMoneyBag, hasUniqueHeart, hasUniquePickaxe, drillBuff, drillBuffStat, hullBuff, hullBuffStat):
        # Has debug been used
        self.debugUsed = debugUsed
        # Stats
        self.moveSpeed = moveSpeed
        self.jumpStrength = jumpStrength
        self.digPower = digPower
        self.money = money
        self.uniqueOres = uniqueOres
        self.maxHealth = maxHealth
        self.health = self.maxHealth
        self.moneyLoss = moneyLoss # Float. 0 is lose all, 1 is keep all
        # Upgrades 
        self.hasUniqueMoneyBag = hasUniqueMoneyBag
        self.hasUniqueHeart = hasUniqueHeart
        self.hasUniquePickaxe = hasUniquePickaxe # Float so it scales slower
        self.drillBuff = drillBuff
        self.drillBuffStat = drillBuffStat
        self.hullBuff = hullBuff
        self.hullBuffStat = hullBuffStat

# Always
# Setup
running = True
inGame = False
clock = pygame.time.Clock()
deltaTime = 0.1
shopOverlay = False
renderDistance = 10
collision = False
gravity = 200
world_depth = 1250
font = pygame.font.Font(None, size=30)
recentlyBroken = font.render("nothing", True, (255,255,255))
brokenCooldown = 0
menuSlot = 0
menuMove = 0
menuSubMenu = ""
menuSubSlot = 0
# Debug
debugDig = False
debugHitbox = False
debugMovement = False
debugHealth = False
debugJump = False
debugMoney = False
# Player stuff that will not be saved
keyDPressed = False
keyAPressed = False
keyWPressed = False
keySPressed = False
keyAnyPressed = False
keySpacePressed = False
degrees = 0
shopCursorSlot = 0
shopTabId = 0
subShopTab = 0
moveShop = 0
deathTimer = 0
controlls = "menu"
depth = 0
# This is a chill game so these can be reset
x = 304
y = -640
speedY = 0
cam_y = y


def loadPlayer(save):
    with open(f"!saves/save{save}/player.txt") as save:
        playerData = []
        for line in save:
            lineSplit = line.split()
            if len(lineSplit) > 0:
                print(lineSplit[0])
                if lineSplit[0] != "--":
                    if lineSplit[2] == "False":
                        playerData.append(False)
                    elif lineSplit[2] == "True":
                        lineSplit[2] == True
                        playerData.append(True)
                    elif lineSplit[2] == "None":
                        playerData.append(None)
                    else:
                        tempValue = float(lineSplit[2])
                        try:
                            tempValue = int(tempValue)
                        except TypeError:
                            pass
                        playerData.append(tempValue)

    # Add playerData to an object
    return(playerClass(playerData[0],playerData[1],playerData[2],playerData[3],playerData[4],playerData[5],playerData[6],playerData[7],playerData[8],playerData[9],playerData[10],playerData[11],playerData[12],playerData[13],playerData[14]))
def loadSave(save):
    global player
    global terrain
    player = loadPlayer(save)
    terrain = loadTerrain(save)
def newSave(save):
    global player
    global terrain
    global world_depth
    os.makedirs(f"!saves/save{save}")
    player = playerClass(False, 80, 150, 30, 0, 0, 25, 0.0, False, False, 0.0, None, None, None, None)
    terrain = make_terrain(world_depth, save)


tiles = []
class materials:
    def __init__(self, name, type, image):
        self.name = name
        self.type = type
        self.sprite = pygame.image.load(image).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite,
                                (self.sprite.get_width() * 2,
                                self.sprite.get_height() * 2))
        tiles.append(self)
        #for i in tiles:
            #print(f"AAA{i.name}AAA")

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
    drillGrey = materials("Grey Drill", "drill","img/drill/drillGrey.png")
    drillBlue = materials("Blue Drill", "drill","img/drill/drillBlue.png")
    drillRed = materials("Red Drill", "drill","img/drill/drillRed.png")
    drillGold = materials("Gold Drill", "drill","img/drill/drillGold.png")
    drillUnique = materials("Unique Drill", "drill","img/drill/drillUnique.png")
    drillInverted = materials("Inverted Drill", "drill","img/drill/drillInverted.png")
    drillCloak = materials("Cloak Drill", "drill","img/drill/drillCloak.png")
    drillHornet = materials("Hornet Drill", "drill","img/drill/drillHornet.png")
if True: # Hulls
    hullOrange = materials("Orange Hull", "hull","img/hull/hullOrange.png")
    hullRed = materials("Red Hull", "hull","img/hull/hullRed.png")
    hullPurple = materials("Purple Hull", "hull","img/hull/hullPurple.png")
    hullInverted = materials("Inverted Hull", "hull","img/hull/hullInverted.png")
    hullGold = materials("Gold Hull", "hull","img/hull/hullGold.png")
    hullDiamond = materials("Diamond Hull", "hull","img/hull/hullDiamond.png")
    hullCloak = materials("Cloak Hull", "hull","img/hull/hullCloak.png")
    hullHornet = materials("Hornet Hull", "hull","img/hull/hullHornet.png")
if True: # Stones
    dirt = materials("Dirt", "stone",'img/tiles/dirtV3.png')
    stone = materials("Stone", "stone",'img/tiles/stoneV2.png')
    bluestone = materials("Bluestone", "stone",'img/tiles/bluestone.png')
    redstone = materials("Redstone", "stone",'img/tiles/redstone.png')
    bloodstone = materials("Bloodstone", "stone",'img/tiles/bloodstoneV2.png')
    abyssmarine = materials("Abyssmarine", "stone",'img/tiles/abyssmarine.png')
    spaceStone = materials("Space Stone", "stone",'img/tiles/spaceStone.png')
    space = materials("Space", "stone",'img/tiles/space.png')
    magma = materials("Magma", "stone",'img/tiles/Magma.png')
    grass = materials("Grass", "extra",'img/tiles/grass.png')
if True: # Backgrounds
    dirtBackground = materials("Dirt", "background", "img/tiles/dirtBackground.png")
    stoneBackground = materials("Stone", "background", "img/tiles/stoneBackground.png")
    bluestoneBackground = materials("Bluestone", "background", "img/tiles/bluestoneBackground.png")
    redstoneBackground = materials("Redstone", "background", "img/tiles/redstoneBackground.png")
    bloodstoneBackground = materials("Bloodstone", "background", "img/tiles/bloodstoneBackground.png")
    abyssmarineBackground = materials("Abyssmarine", "background", "img/tiles/abyssmarineBackground.png")
    spaceStoneBackground = materials("Space Stone", "background", "img/tiles/spaceStoneBackground.png")
    spaceBackground = materials("Space", "background", "img/tiles/spaceBackground.png")
    magmaBackground = materials("Magma", "background", "img/tiles/magmaBackground.png")
    grassBackground = materials("Grass", "background", "img/tiles/grassBackground.png")
if True: # Ores
    coal = materials("Coal", "extra", "img/ores/coal.png")
    iron = materials("Iron", "extra", 'img/ores/iron.png')
    copper = materials("Copper", "extra", "img/ores/copper.png")
    diamond = materials("Diamond", "extra", 'img/ores/diamond.png')
    bismuth = materials("Bismuth", "extra", "img/ores/bismuth.png")
    rainbowite = materials("Rainbowite", "extra", 'img/ores/rainbowite.png')
    uniqueOre = materials("Unique Ore", "extra", "img/ores/uniqueOre.png")
    uniqueOre2 = materials("Big Unique Ore", "extra", 'img/ores/uniqueOre2.png')
    uniqueOre3 = materials("Large Unique Ore", "extra", 'img/ores/uniqueOre3.png')
    star = materials("Star", "extra", "img/ores/star.png")
    starBig = materials("Large Star", "extra", 'img/ores/starBig.png')
    gold = materials("Gold", "extra", "img/ores/gold.png")
    lapisLazuli = materials("Lapis Lazuli", "extra", 'img/ores/lapisLazuli.png')
    eyeBlue = materials("Blue Eye", "extra", "img/ores/eyeBlue.png")
    eyeBlueSquint = materials("Squinting Blue Eye", "extra", 'img/ores/eyeBlueSquint.png')
    eyeGreen = materials("Green Eye", "extra", 'img/ores/eyeGreen.png')
    eyeGreenSquint = materials("Squinting Green Eye", "extra", 'img/ores/eyeGreenSquint.png')
    eyeRed = materials("Red Eye", "extra", "img/ores/eyeRed.png")
    eyeRedSquint = materials("Squinting Red Eye", "extra", 'img/ores/eyeRedSquint.png')
    mouth = materials("Mouth", "extra", "img/ores/mouth.png")
if True: # Upgrades
    heart = materials("Heart", "upgrade", "img/upgrades/heart.png")
    heartUnique = materials("Unique Heart", "upgrade", "img/upgrades/heartUnique.png")
    digPowerGUI = materials("Dig Power", "upgrade", "img/upgrades/digPower.png")
    digPowerUnique = materials("Unique Dig Power", "upgrade", "img/upgrades/digPowerUnique.png")
    jumpStrengthGUI = materials("Jump Strength", "upgrade", "img/upgrades/jumpStrength.png")
    jumpStrengthUnique = materials("Unique Jump Strength", "upgrade", "img/upgrades/jumpStrengthUnique.png")
    moveSpeedGUI = materials("Move Speed", "upgrade", "img/upgrades/moveSpeed.png")
    moveSpeedUnique = materials("Unique Move Speed", "upgrade", "img/upgrades/moveSpeedUnique.png")
    moneyBag = materials("Money Bag", "upgrade", "img/upgrades/moneyBag.png")
    moneyBagUnique = materials("Unique Money Bag", "upgrade", "img/upgrades/moneyBagUnique.png")
if True: # Shop buttons and titles
    shopBuy = materials("Shop Buy", "shop", "img/gui/shopBuy.png")
    shopBuyUnique = materials("Shop Buy Unique", "shop", "img/gui/shopBuyUnique.png")
    shopPoor = materials("Shop Poor", "shop", "img/gui/shopPoor.png")
    shopButtonSelect = materials("Shop Button Select", "shop", "img/gui/shopButtonSelect.png")
    drillSkins = materials("Drill Skins", "shop", "img/gui/drillSkins.png")
    hullSkins = materials("Hull Skins", "shop", "img/gui/hullSkins.png")
    upgrades = materials("Upgrades", "shop", "img/gui/upgrades.png")
    upgradesUnique = materials("Upgrades Unique", "shop", "img/gui/upgradesUnique.png")
    stats = materials("Stats", "shop", "img/gui/stats.png")
    stats2 = materials("Stats 2", "shop", "img/gui/stats2.png")
    shopVisual = materials("Shop Visual", "shop", "img/gui/shopVisual.png")
    shopEquip = materials("Shop Equip", "shop", "img/gui/shopEquip.png")
    # Main menu
    menuEmpty = materials("Menu Empty", "mainMenu", "img/gui/menuEmpty.png")
    menuSlot1 = materials("Menu Slot 1", "mainMenu", "img/gui/menuSlot1.png")
    menuSlot2 = materials("Menu Slot 2", "mainMenu", "img/gui/menuSlot2.png")
    menuSlot3 = materials("Menu Slot 3", "mainMenu", "img/gui/menuSlot3.png")
    menuSlotSelect = materials("Menu Slot Select", "mainMenu", "img/gui/menuSlotSelect.png")
    menuSelect = materials("Menu Select", "mainMenu", "img/gui/menuSelect.png")
    menuNew = materials("Menu New", "mainMenu", "img/gui/menuNew.png")
    menuLoad = materials("Menu Load", "mainMenu", "img/gui/menuLoad.png")
    menuDelete = materials("Menu Delete", "mainMenu", "img/gui/menuDelete.png")
    
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

class shopTabs:
    def __init__(self, name, title, slots):
        self.name = name
        self.title = title
        self.slots = slots
        if slots != None:
            self.slots = slots-1
if True:
    upgradesShop = shopTabs("upgrades", upgrades.sprite, 5)
    uniqueShop = shopTabs("unique", upgradesUnique.sprite, 5)
    statsPage1 = shopTabs("stats", stats.sprite, None)
    statsPage2 = shopTabs("stats 2", stats2.sprite, None)
    drillSkinsShop = shopTabs("drill", drillSkins.sprite, 8)
    hullSkinsShop = shopTabs("hull", hullSkins.sprite, 8)

shopTab = [upgradesShop, uniqueShop, statsPage1, statsPage2, drillSkinsShop, hullSkinsShop]

drill = drillGrey.sprite
hull = hullOrange.sprite

if True: # SFX
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
# terrain = make_terrain(world_depth, 1)
print(world_depth)
def draw_terrain(screen, terrain, camera, depth):
    for i in terrain:
        y = i.y + 1000 + camera

        if not i.mined and i.deep + renderDistance > depth and i.deep - renderDistance < abs(depth): # Not mined
            for tile in tiles:
                if tile.type == "stone" and i.ore == tile.name:
                    screen.blit(tile.sprite, (i.x, y))
                if tile.type == "extra" and i.extra == tile.name:
                    screen.blit(tile.sprite, (i.x, y))

            # Check if it's broken
            if i.health < i.hardness/4:
                screen.blit(break3, (i.x, y))
            if i.health < i.hardness/4*2:
                screen.blit(break2, (i.x, y))
            if i.health < i.hardness/4*3:
                screen.blit(break1, (i.x, y))
        
        if i.mined and i.deep + renderDistance > depth and i.deep - renderDistance < abs(depth): # Mined
            for tile in tiles:
                if tile.type == "background" and i.ore == tile.name or tile.type == "background" and i.extra == tile.name:
                    screen.blit(tile.sprite, (i.x, y))
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
        if terrain[i].deep + renderDistance > depth and terrain[i].deep - renderDistance < abs(depth):
            y = terrain[i].y + 1000 + camera
            terrain[i].rect = pygame.Rect(0,0,32,32)
            if not terrain[i].mined:
                terrain[i].rect = pygame.Rect(terrain[i].x, y, 32, 32)  # This line causes the hitboxes to appear where the terrain is visually
            #pygame.draw.rect(screen, (0, 255, 0), terrain[i].rect)
            collision = hitbox.colliderect(terrain[i].rect)
            if collision:
                break
def rotate(dir):
    global degrees
    global hull
    global drill
    hull = pygame.transform.rotate(hull, degrees*-1)
    drill = pygame.transform.rotate(drill, degrees*-1)
    degrees = dir
    hull = pygame.transform.rotate(hull, degrees)
    drill = pygame.transform.rotate(drill, degrees)
def checkSkinBuffs(check, amount, player, multiplier = 1): #This function checks changes the stat that a skin does. A multiplier of 1 increases, -1 decreases
    
    if check == "digPower":
        player.digPower += amount * multiplier
    if check == "maxHealth":
        player.maxHealth += amount * multiplier
        if multiplier > 0:
            player.health += amount
        if multiplier < 0 and player.health > player.maxHealth:
            player.health = player.maxHealth
    if check == "moveSpeed":
        player.moveSpeed += amount * multiplier
    if check == "moneyLoss":
        player.moneyLoss +=amount * multiplier
    if check == "jumpStrength":
        player.jumpStrength += amount * multiplier
    if check == "moneyRepeat":
        player.jumpStrength += amount * multiplier

def whatSave(save, base, bonusString = "", extraComment = ""):
    with open(f"!saves/save{save}/player.txt", "a") as save:
        save.write(f"{base} {str(bonusString)} {extraComment}\n")


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
    def __init__(self, cost, flavour, sprite, tab, slot, associatedStat, amount, owned = False):
        self.cost = cost
        self.flavour = flavour
        self.sprite = sprite
        self.associatedStat = associatedStat
        self.amount = amount
        self.owned = owned
        self.tab = tab
        self.slot = slot

# These are also if Trues so that I can hide them in editor
if True: # Upgrades
    heartShop = shopItem(100, False, "Increases maximum HP by 5.", heart.sprite, "upgrades", 0, 10, 1000000, 100000, 5000000)
    digPowerShop = shopItem(25, False, "Increases dig power by 5.", digPowerGUI.sprite, "upgrades", 1, 3, 500000, 30000, 100000)
    jumpStrengthShop = shopItem(75, False, "Increases jump strength by 5.", jumpStrengthGUI.sprite, "upgrades", 2, 2.5, 750000, 50000, 2500000)
    moveSpeedShop = shopItem(50, False, "Increases horisontal speed by 5.", moveSpeedGUI.sprite, "upgrades", 3, 500000, 30000, 100000)
    moneyBagShop = shopItem(500, False, "Saves 1% of money on death.", moneyBag.sprite, "upgrades", 4, 2.5, 10000, 10000, 1000000, 50)
if True: # Unique upgrades
    heartUniqueShop = shopItem(2, True, "Increases maximum HP by 15.", heartUnique.sprite, "unique", 0, 5, 5000, 500, 10000)
    digPowerUniqueShop = shopItem(5, True, "Increases dig power by 20.", digPowerUnique.sprite, "unique", 1, 3, 1000, 750, 10000)
    jumpStrengthUniqueShop = shopItem(3, True, "Increases jump strength by 15.", jumpStrengthUnique.sprite, "unique", 2, 2.5, 3000, 300, 30000)
    moveSpeedUniqueShop = shopItem(5, True, "Increases horisontal speed by 15.", moveSpeedUnique.sprite, "unique", 3, 3, 1000, 100, 10000)
    moneyBagUniqueShop = shopItem(10, True, "Saves 5% of money on death.", moneyBagUnique.sprite, "unique", 4, 2.5, 5000, 100, 1000000, 5)
if True: # Drill skins
    drillGreyShop = cosmetic(0, "The classic drill.", drillGrey.sprite, "drill", 0, None, None, True)
    drillBlueShop = cosmetic(10, "+15 dig power when equipped.", drillBlue.sprite, "drill", 1, "digPower", 15)
    drillRedShop = cosmetic(10, "+30 dig power when equipped.", drillRed.sprite, "drill", 2, "digPower", 30)
    drillGoldShop = cosmetic(10, "+45 dig power when equipped.", drillGold.sprite, "drill", 3, "digPower", 45)
    drillUniqueShop = cosmetic(10, "+90 dig power when equipped.", drillUnique.sprite, "drill", 4, "digPower", 90)
    drillInvertedShop = cosmetic(10, "+10 max HP when equipped.", drillInverted.sprite, "drill", 5, "maxHealth", 10)
    drillCloakShop = cosmetic(20, "The cloak of a hunter.", drillCloak.sprite, "drill", 6, None, None)
    drillHornetShop = cosmetic(20, "The head of a hunter.", drillHornet.sprite, "drill", 7, None, None)
if True: # Hull skins
    hullOrangeShop = cosmetic(0, "The classic hull.", hullOrange.sprite, "hull", 0, None, None, True)
    hullRedShop = cosmetic(10, "+10 max HP when equipped.", hullRed.sprite, "hull", 1, "maxHealth", 10)
    hullPurpleShop = cosmetic(10, "+20 max HP when equipped", hullPurple.sprite, "hull", 2, "maxHealth", 20)
    hullGoldShop = cosmetic(10, "+30 max HP when equipped", hullGold.sprite, "hull", 3, "maxHealth", 30)
    hullInvertedShop = cosmetic(10, "+15 dig power when equipped", hullInverted.sprite, "hull", 4, "digPower", 15)
    hullDiamondShop = cosmetic(10, "Increases money earnt", hullDiamond.sprite, "hull", 5, "moneyRepeat", 1)
    hullHornetShop = cosmetic(20, "A familiar bug", hullHornet.sprite, "hull", 7, None, None)
    hullCloakShop = cosmetic(20, "A familiar cloak.", hullCloak.sprite, "hull", 6, None, None)
if True: # Lists
    upgradesList = [heartShop, digPowerShop, jumpStrengthShop, moveSpeedShop, moneyBagShop]
    uniqueUpgradesList = [heartUniqueShop, digPowerUniqueShop, jumpStrengthUniqueShop, moveSpeedUniqueShop, moneyBagUniqueShop]
    drillSkinsList = [drillGreyShop, drillBlueShop, drillRedShop, drillGoldShop, drillUniqueShop, drillCloakShop, drillInvertedShop, drillHornetShop]
    hullSkinsList = [hullOrangeShop, hullRedShop, hullPurpleShop, hullInvertedShop, hullHornetShop, hullGoldShop, hullCloakShop, hullDiamondShop]
    listList = [upgradesList, uniqueUpgradesList, drillSkinsList, hullSkinsList]
    shop = []
    for i in range(len(listList)):
        for o in listList[i]:
            shop.append(o)

def saveGame(player, terrain, save):
    saveTerrain(terrain, save)
    if os.path.exists(f"!saves/save{save}/player.txt"):
        os.remove(f"!saves/save{save}/player.txt")
    else:
        print("The file does not exist")
    with open(f"!saves/save{save}/player.txt", "x"):
        whatSave(save, "-- Use two dashes (--) with a space ( ) after to mark as a comment. Only on the start is required, but at the end makes it pretty. Only at the start if it's a comment on a line --\n\n")
        whatSave(save, "-- Has debug been used? --\n")
        whatSave(save, "debugUsed = ", player.debugUsed)
        whatSave(save, "-- Stats --\n")
        whatSave(save, "moveSpeed = ", player.moveSpeed)
        whatSave(save, "jumpStrength = ", player.jumpStrength)
        whatSave(save, "digPower = ", player.digPower)
        whatSave(save, "money = ", player.money)
        whatSave(save, "uniqueOres = ", player.uniqueOres)
        whatSave(save, "maxHealth = ", player.maxHealth)
        whatSave(save, "moneyLoss = ", player.moneyLoss, "-- something something I |Ii|II|I_")
        whatSave(save, "-- Upgrades --")
        whatSave(save, "hasUniqueMoneyBag = ", player.hasUniqueMoneyBag)
        whatSave(save, "hasUniqueHeart = ", player.hasUniqueHeart)
        whatSave(save, "hasUniquePickaxe = ", player.hasUniquePickaxe, "-- Float so it scales slower")
        whatSave(save, "drillBuff = ", player.drillBuff)
        whatSave(save, "drillBuffStat = ", player.drillBuffStat)
        whatSave(save, "hullBuff = ", player.hullBuff)
        whatSave(save, "hullBuffStat = ", player.hullBuffStat)

#print(len(terrain)/20)
hitbox = pygame.Rect(x+4, 224, 24, 32)
digSquare = pygame.Rect(x, 224, 8, 8)
while running:
    if inGame: # Main game loop
        # BG
        if player.health < 1:
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
                if player.maxHealth > terrain[i].damage or debugHealth:
                    terrain[i].health -= player.digPower * deltaTime
                    if random.randint(1,20) == 1:
                        digNoises[random.randint(0,2)].play()
                        print("sound")
                    if terrain[i].health <= 0:
                        terrain[i].mined = True
                        player.health -= terrain[i].damage
                        if terrain[i].extra == "":
                            recentlyBroken = font.render(f"{terrain[i].ore}", True, (255,255,255))
                        else:
                            recentlyBroken = font.render(f"{terrain[i].extra}", True, (255,255,255))
                        brokenCooldown = 1
                        moneyRepeat = 1
                        if player.hasUniquePickaxe > 0:
                            moneyRepeat += math.floor(player.hasUniquePickaxe)
                        if terrain[i].extra != '' and terrain[i].extra != 'Grass':
                            oreBreak.play()
                        elif random.randint(1,3) == 1:
                            rockBreak.play()
                        player.money += terrain[i].value * moneyRepeat
                        player.uniqueOres += terrain[i].uniqueOre * moneyRepeat
                else:
                    recentlyBroken = font.render(f"Too weak! Need more Max HP", True, (255,255,255))
                    brokenCooldown = 1

        brokenCooldown -= 1*deltaTime
        if brokenCooldown > 0:
            brokenX = 640-4-recentlyBroken.get_width()
            screen.blit(recentlyBroken, (brokenX,456))

        speedY += gravity * deltaTime
        if speedY > player.jumpStrength:
            speedY = player.jumpStrength

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

        screen.blit(hull, (x, 223))
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
            player.health = player.maxHealth

        moneyText = font.render(f"${player.money}", True, (255,255,0))
        uniqueOreText = font.render(f"UO: {player.uniqueOres}", True, (122,0,122))
        healthText = font.render(f"{player.health}/{player.maxHealth}", True, (255,0,0))
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
        screen.blit(heart.sprite, (4,4))
        screen.blit(healthText, (36, 10))
        screen.blit(depthText, (4, 456))

        keyAnyPressed = False
        if controlls == "move": # For movement, duh :) 
            if keyDPressed:
                x += player.moveSpeed * deltaTime
                collision = collide(x)
                digSquare = pygame.Rect(x+24, 224+8, 16, 16)
                while collision:
                    x -= 1
                    collision = collide(x)
                keyAnyPressed = True
                rotate(-90)

            if keyAPressed:
                x -= player.moveSpeed * deltaTime
                collision = collide(x)
                digSquare = pygame.Rect(x-8, 224+8, 16, 16)
                while collision:
                    x += 1
                    collision = collide(x)
                keyAnyPressed = True
                rotate(90)

            if keyWPressed:
                digSquare = pygame.Rect(x+8, 224-8, 16, 16)
                if jumpable:
                    speedY -= player.jumpStrength
                keyAnyPressed = True
                rotate(0)

            if keySPressed:
                digSquare = pygame.Rect(x+8, 224+24, 16, 16)
                keyAnyPressed = True
                rotate(180)

        if controlls == "shop": # For when in the shop GUI

            screen.blit(shopTab[shopTabId].title, (240, 32))

            for i in shop:
                shopText = font.render(f"{i.flavour} Cost: {i.cost}", True, (255,255,255))
                shopText2 = font.render("", True, (255,255,255))
                if i.tab == shopTab[shopTabId].name:
                    if shopTab[shopTabId].name == "drill" or shopTab[shopTabId].name == "hull":
                        if i.owned:
                            shopText = font.render(f"{i.flavour}", True, (255,255,255))
                    screen.blit(i.sprite, (32, 64+36*i.slot))
                    screen.blit(shopText, (64, 72+36*i.slot))

                    if shopTab[shopTabId].name == "upgrades" or shopTab[shopTabId].name == "unique":
                        if not i.unique:
                            if player.money >= i.cost or debugMoney:
                                screen.blit(shopBuy.sprite, (540, 64+36*i.slot))
                                shopButtonHitbox = pygame.Rect(540, 64+36*i.slot, 64, 32)
                                shopCursorHitbox = pygame.Rect(540, 64+36*shopCursorSlot, 64, 32)
                                shopCollision = shopCursorHitbox.colliderect(shopButtonHitbox)
                                if shopCollision and keySpacePressed and moveShop <= 0:
                                    if not debugMoney:
                                        player.money -= i.cost
                                    i.cost = math.floor(i.cost*i.priceIncrease)
                                    if i.sprite == heart:
                                        player.maxHealth += 5
                                        player.health = player.maxHealth
                                    if i.sprite == digPowerGUI:
                                        player.digPower += 5
                                    if i.sprite == jumpStrengthGUI:
                                        player.jumpStrength += 5
                                    if i.sprite == moveSpeedGUI:
                                        player.moveSpeed += 5
                                    if i.sprite == moneyBag:
                                        player.moneyLoss += 0.01
                                    print("oi")
                            else:
                                screen.blit(shopPoor.sprite, (540, 64+36*i.slot))
                        if i.unique:
                            if player.uniqueOres >= i.cost or debugMoney:
                                screen.blit(shopBuyUnique.sprite, (540, 64+36*i.slot))
                                shopButtonHitbox = pygame.Rect(540, 64+36*i.slot, 64, 32)
                                shopCursorHitbox = pygame.Rect(540, 64+36*shopCursorSlot, 64, 32)
                                shopCollision = shopCursorHitbox.colliderect(shopButtonHitbox)
                                if shopCollision and keySpacePressed and moveShop <= 0:
                                    if i.tab == "unique":
                                        if not debugMoney:
                                            player.uniqueOres -= i.cost
                                        i.cost = math.floor(i.cost*i.priceIncrease)
                                        if i.sprite == heartUnique:
                                            player.maxHealth += 15
                                            player.health = player.maxHealth
                                            player.hasUniqueHeart = True
                                        if i.sprite == digPowerUnique:
                                            player.digPower += 20
                                            player.hasUniquePickaxe += 0.5
                                        if i.sprite == jumpStrengthUnique:
                                            player.jumpStrength += 15
                                        if i.sprite == moveSpeedUnique:
                                            player.moveSpeed += 15
                                        if i.sprite == moneyBagUnique:
                                            player.moneyLoss += 0.05
                                            player.hasUniqueMoneyBag = True
                                        print("oi")
                            else:
                                screen.blit(shopPoor.sprite, (540, 64+36*i.slot))
                    if shopTab[shopTabId].name == "drill" or shopTab[shopTabId].name == "hull":
                        if not i.owned:
                            for verySpecificVaribleJustForThisSpotInTheCode in range(2):
                                if player.uniqueOres >= i.cost or debugMoney:
                                    screen.blit(shopBuyUnique.sprite, (468+72*verySpecificVaribleJustForThisSpotInTheCode, 64+36*i.slot))
                                    shopButtonHitbox = pygame.Rect(468+72*verySpecificVaribleJustForThisSpotInTheCode, 64+36*i.slot, 64, 32)
                                    shopCursorHitbox = pygame.Rect(468+72*verySpecificVaribleJustForThisSpotInTheCode, 64+36*shopCursorSlot, 64, 32)
                                    shopCollision = shopCursorHitbox.colliderect(shopButtonHitbox)
                                    if shopCollision and keySpacePressed and moveShop <= 0:
                                        i.owned = True
                                        if not debugMoney:
                                            player.uniqueOres -= i.cost
                                        moveShop += 0.5
                                else:
                                    screen.blit(shopPoor.sprite, (468+72*verySpecificVaribleJustForThisSpotInTheCode, 64+36*i.slot))
                        else:
                            screen.blit(shopEquip.sprite, (540, 64+36*i.slot))
                            shopButtonHitbox = pygame.Rect(540, 64+36*i.slot, 64, 32)
                            shopCursorHitbox = pygame.Rect(540, 64+36*shopCursorSlot, 64, 32)
                            shopCollision = shopCursorHitbox.colliderect(shopButtonHitbox)
                            if shopCollision and keySpacePressed and moveShop <= 0:
                                if i.associatedStat != None:
                                    if shopTab[shopTabId].name == "drill":
                                        checkSkinBuffs(player.drillBuffStat, player.drillBuff, -1)
                                    else:
                                        checkSkinBuffs(player.hullBuffStat, player.hullBuff, -1)
                                    checkSkinBuffs(i.associatedStat, i.amount, 1)
                                else:
                                    if shopTab[shopTabId] == "drill":
                                        checkSkinBuffs(player.drillBuffStat, player.drillBuff, -1)
                                    else:
                                        checkSkinBuffs(player.hullBuffStat, player.hullBuff, -1)
                                print(f"DB: {player.drillBuff}, {player.drillBuffStat}")
                                print(f"HB: {player.hullBuff}, {player.hullBuffStat}")
                                print(f"AS: {i.amount}, {i.associatedStat}")
                                
                                if i.tab == "hull":
                                    hull = i.sprite
                                    player.hullBuff = i.amount
                                    player.hullBuffStat = i.associatedStat
                                if i.tab == "drill":
                                    drill = i.sprite
                                    player.drillBuff = i.amount
                                    player.drillBuffStat = i.associatedStat
                                rotate(0)
                                moveShop = 0.5
                                
                            screen.blit(shopVisual.sprite, (468, 64+36*i.slot))
                            shopButtonHitbox = pygame.Rect(468, 64+36*i.slot, 64, 32)
                            shopCursorHitbox = pygame.Rect(468, 64+36*shopCursorSlot, 64, 32)
                            shopCollision = shopCursorHitbox.colliderect(shopButtonHitbox)
                            if shopCollision and keySpacePressed and moveShop <= 0:
                                if i.tab == "hull":
                                    hull = i.sprite
                                if i.tab == "drill":
                                    drill = i.sprite
                                rotate(0)
                                moveShop = 0.5
                if i.tab != "drill" and i.tab != "hull":
                    if shopTab[shopTabId].name == "stats" and not i.unique:
                        screen.blit(i.sprite, (32, 64+68*i.slot))
                        if i.sprite == heart:
                            shopText = font.render(f"How much health you have before you die.", True, (255,255,255))
                            shopText2 = font.render(f"Value: {player.maxHealth}", True, (255,255,255))
                        if i.sprite == digPowerGUI:
                            shopText = font.render(f"How much damage you deal to rocks.", True, (255,255,255))
                            shopText2 = font.render(f"Value: {player.digPower}", True, (255,255,255))
                        if i.sprite == jumpStrengthGUI:
                            shopText = font.render(f"How high you jump and your max terminal velocity.", True, (255,255,255))
                            shopText2 = font.render(f"Value: {player.jumpStrength}", True, (255,255,255))
                        if i.sprite == moveSpeedGUI:
                            shopText = font.render(f"How fast you move horizontally.", True, (255,255,255))
                            shopText2 = font.render(f"Value: {player.moveSpeed}", True, (255,255,255))
                        if i.sprite == moneyBag:
                            shopText = font.render(f"How much money you save on death in %.", True, (255,255,255))
                            shopText2 = font.render(f"Value: {player.moneyLoss}", True, (255,255,255))
                        screen.blit(shopText, (64, 72+68*i.slot))
                        screen.blit(shopText2, (64, 104+68*i.slot))
                    if shopTab[shopTabId].name == "stats 2" and i.unique:
                        screen.blit(i.sprite, (32, 64+68*i.slot))
                        if i.sprite == heartUnique:
                            shopText = font.render(f"Having this upgrade gives you a chance to heal\nwhen you break rocks.", True, (255,255,255))
                        if i.sprite == digPowerUnique:
                            shopText = font.render(f"Having this upgrade increases money from ores", True, (255,255,255))
                            shopText2 = font.render(f"Value: {player.hasUniquePickaxe}", True, (255,255,255))
                        if i.sprite == jumpStrengthUnique:
                            shopText = font.render(f"This upgrade has no special ability.", True, (255,255,255))
                        if i.sprite == moveSpeedUnique:
                            shopText = font.render(f"This upgrade has no special ability.", True, (255,255,255))
                        if i.sprite == moneyBagUnique:
                            shopText = font.render(f"Having this upgrade ceilings saved money instead\nof flooring it. You save like $1", True, (255,255,255))
                        screen.blit(shopText, (64, 72+68*i.slot))
                        if i.sprite == digPowerUnique:
                            screen.blit(shopText2, (64, 104+68*i.slot))
            if shopTab[shopTabId].name != "stats" and shopTab[shopTabId].name != "stats 2":
                if shopTab[shopTabId].name == "drill" or shopTab[shopTabId].name == "hull":
                    screen.blit(shopButtonSelect.sprite, (464+72*subShopTab,60+36*shopCursorSlot))
                else:
                    screen.blit(shopButtonSelect.sprite,(536,60+36*shopCursorSlot))
            if moveShop <= 0:
                print(shopTabId)
                if keySPressed and shopTab[shopTabId].name != "stats" and shopTab[shopTabId].name != "stats 2":
                    shopCursorSlot += 1
                    moveShop = 0.5
                if keyWPressed and shopTab[shopTabId].name != "stats" and shopTab[shopTabId].name != "stats 2":
                    shopCursorSlot -= 1
                    moveShop = 0.5
                if shopTab[shopTabId].name != "stats" and shopTab[shopTabId].name != "stats 2":
                    if shopCursorSlot < 0:
                        shopCursorSlot = shopTab[shopTabId].slots
                    if shopCursorSlot > shopTab[shopTabId].slots:
                        shopCursorSlot = 0
                if keyDPressed:
                    if shopTab[shopTabId].name == "drill" or shopTab[shopTabId].name == "hull":
                        if subShopTab == 1:
                            shopTabId += 1
                            shopCursorSlot = 0
                            subShopTab = 0
                        else:
                            subShopTab += 1
                    else:
                        shopTabId += 1
                        shopCursorSlot = 0
                        subShopTab = 0
                    moveShop = 0.5
                if keyAPressed:
                    if shopTab[shopTabId].name == "drill" or shopTab[shopTabId].name == "hull":
                        if subShopTab == 0:
                            shopTabId -= 1
                            shopCursorSlot = 0
                            subShopTab = 1
                        else:
                            subShopTab -= 1
                    else:
                        shopTabId -= 1
                        shopCursorSlot = 0
                        subShopTab = 1
                    moveShop = 0.5
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

        if player.health < 1:
            print(deathTimer)
            keyAnyPressed = False
            controlls = "dead"
            if deathTimer == 0:
                deathTimer = 3
            else:
                deathTimer -= 1*deltaTime
                if deathTimer <= 0:
                    if player.hasUniqueMoneyBag:
                        player.money = math.ceil(player.money * player.moneyLoss)
                    else:
                        player.money = math.floor(player.money * player.moneyLoss)
                    deathTimer = 0
                    player.health = player.maxHealth
                    controlls = "move"
                    x = 304
                    y = -640
                    cam_y = y
                    redoGroundRects(terrain, cam_y, depth)

        if player.debugUsed:
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

    else: # Main Menu
        savedGames = os.listdir("!saves")
        screen.fill((122,122,122))
        saveExists = False
        for i in range(3):
            for o in savedGames:
                if o == f"save{i+1}":
                    saveExists = True
                    break
                else:
                    saveExists = False
            if saveExists:
                if i == 0:
                    slotX = [432,176,-80]
                    effectiveSlot = menuSlot+1
                    if effectiveSlot > 2:
                        effectiveSlot = 0
                    screen.blit(menuSlot1.sprite, (slotX[effectiveSlot],0))
                if i == 1:
                    slotX = [432,176,-80]
                    screen.blit(menuSlot2.sprite, (slotX[menuSlot],0))
                if i == 2:
                    slotX = [432,176,-80]
                    effectiveSlot = menuSlot-1
                    if effectiveSlot < 0:
                        effectiveSlot = 2
                    screen.blit(menuSlot3.sprite, (slotX[effectiveSlot],0))
            else:
                if i == 0:
                    slotX = [432,176,-80]
                    effectiveSlot = menuSlot+1
                    if effectiveSlot > 2:
                        effectiveSlot = 0
                    screen.blit(menuEmpty.sprite, (slotX[effectiveSlot],0))
                if i == 1:
                    slotX = [432,176,-80]
                    screen.blit(menuEmpty.sprite, (slotX[menuSlot],0))
                    
                if i == 2:
                    slotX = [432,176,-80]
                    effectiveSlot = menuSlot-1
                    if effectiveSlot < 0:
                        effectiveSlot = 2
                    screen.blit(menuEmpty.sprite, (slotX[effectiveSlot],0))

        if keySpacePressed and menuMove <= 0:
            save = menuSlot + 1
            if menuSubMenu == "":
                saveExists = False
                for i in savedGames:
                    if i == f"save{save}":
                        saveExists = True
                        break
            if menuSubMenu == "load":
                if menuSubSlot == 2:
                    loadSave(save)
                    inGame = True
                    controlls = "move"
                elif menuSubSlot == 1:
                    menuSubMenu = "delete"
                    menuSubSlot = 0
                    print("DELETE")
                elif menuSubSlot == 0:
                    menuSubMenu = ""
                    menuSubSlot = 0
            elif menuSubMenu == "new":
                if menuSubSlot == 1:
                    newSave(save)
                    inGame = True
                    controlls = "move"
                if menuSubSlot == 0:
                    menuSubMenu = ""
                    menuSubSlot = 0
            elif menuSubMenu == "delete":
                if menuSubSlot == 1:
                    os.remove(f"!saves/save{save}/player.txt")
                    os.remove(f"!saves/save{save}/terrain.txt")
                    os.rmdir(f"!saves/save{save}")
                    menuSubMenu = ""
                    menuSubSlot = 0
                if menuSubSlot == 0:
                    menuSubMenu = ""
                    menuSubSlot = 0
            elif saveExists:
                menuSubMenu = "load"
                menuSubSlot = 0
            else:
                menuSubMenu = "new"
                menuSubSlot = 0
            menuMove += 0.5
        if menuSubMenu == "new":
            screen.blit(menuNew.sprite,(176,0))
        if menuSubMenu == "load":
            screen.blit(menuLoad.sprite,(176,0))
        if menuSubMenu == "delete":
            screen.blit(menuDelete.sprite,(176-2,0))
        if menuMove <= 0:
            if keyAPressed:
                menuSlot -= 1
                menuMove += 0.5
            if keyDPressed:
                menuSlot += 1
                menuMove += 0.5
            if keyWPressed:
                menuSubSlot +=1
                menuMove += 0.5
            if keySPressed:
                menuSubSlot -=1
                menuMove += 0.5
            if menuSlot > 2:
                menuSlot = 0
            if menuSlot < 0:
                menuSlot = 2
            if menuSubSlot > 1:
                if menuSubMenu != "load" or menuSubSlot > 2:
                    menuSubSlot = 0
            if menuSubSlot < 0:
                menuSubSlot = 1
                if menuSubMenu == "load":
                    menuSubSlot += 1
        else:
            menuMove -= 2*deltaTime
        if menuSubMenu == "":
            screen.blit(menuSlotSelect.sprite,(176,0))
        else:
            screen.blit(menuSelect.sprite,(176,320-96*(menuSubSlot+1)))
        #print(menuSubMenu, menuSubSlot)

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if inGame:
                    saveGame(player, terrain, save)
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
                    player.health = player.maxHealth
                # Shop
                if event.key == pygame.K_SPACE and controlls != "move":
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
                        subShopTab = 0
                        shopTabId = 0
                        moveShop = 0
                # Debug
                if event.key == pygame.K_F1:
                    if debugDig:
                        debugDig = False
                        player.digPower -= 90000
                        print("Insane dig power: Off")
                    else:
                        debugDig = True
                        player.digPower += 90000
                        player.debugUsed = True
                        print("Insane dig power: On")
                if event.key == pygame.K_F2:
                    if debugHitbox:
                        debugHitbox = False
                        print("Show hitboxes: Off")
                    else:
                        debugHitbox = True
                        player.debugUsed = True
                        print("Show hitboxes: On")
                if event.key == pygame.K_F3:
                    if debugMovement:
                        debugMovement = False
                        print("Movement info: Off")
                    else:
                        debugMovement = True
                        player.debugUsed = True
                        print("Movement info: On")
                if event.key == pygame.K_F4:
                    if debugHealth:
                        debugHealth = False
                        print("Infinite health: Off")
                    else:
                        debugHealth = True
                        player.debugUsed = True
                        print("Infinite health: On")
                if event.key == pygame.K_F5:
                    if debugJump:
                        player.jumpStrength -= 1000
                        debugJump = False
                        print("Insane jump power: Off")
                    else:
                        debugJump = True
                        player.jumpStrength += 1000
                        player.debugUsed = True
                        print("Insane jump power: On")
                if event.key == pygame.K_F6:
                    if debugMoney:
                        debugMoney = False
                        print("Infinite money: Off")
                    else:
                        debugMoney = True
                        player.debugUsed = True
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
                if event.key == pygame.K_SPACE and controlls != "move":
                    keySpacePressed = False
    # end stuff
    pygame.display.flip()
    deltaTime = clock.tick(60) / 1000
    deltaTime = max(0.001, min((0.1, deltaTime)))

pygame.quit()