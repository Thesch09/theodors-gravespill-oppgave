import pygame
import random
import math
# Generate the terrain
def make_terrain(depth):
    class ore:
        def __init__(self, type, name, hardness, value, damage, minHeight = None, maxHeight = None, chance = None, uniqueOre = None):
            self.type = type
            self.name = name
            self.hardness = hardness
            self.value = value
            self.damage = damage
            self.minHeight = minHeight
            self.maxHeight = maxHeight
            self.chance = chance
            self.uniqueOre = uniqueOre

    def addOre(ore, terrain, location):
        if ore.type == "rock":
            terrain[location].ore = ore.name
            terrain[location].hardness = ore.hardness
            terrain[location].value = ore.value
            terrain[location].damage = ore.damage
        elif ore.type == "mineral":
            terrain[location].extra = ore.name
            terrain[location].hardness += ore.hardness
            terrain[location].value += ore.value
            terrain[location].damage += ore.damage
            if ore.uniqueOre != None:
                terrain[location].uniqueOre = ore.uniqueOre
        else:
            print("UNDIFINED RESOURCE TYPE")
    
    def addToTerrain(list, terrain):
        rockTions = [] # A portmanteau of rock and options
        for i in list:
            if i.minHeight != None and i.maxHeight != None:
                if height >= i.minHeight and height <= i.maxHeight:
                    rockTions.append(i)
        print(len(rockTions))
        if len(rockTions) >= 1:
            selectedRockTion = rockTions[random.randint(0, len(rockTions)-1)]
            if i.type == "rock" or i.type == "mineral" and random.randint(1, selectedRockTion.chance) == 1 and terrain[-1].ore != "" and terrain[-1].ore != "Dirt":
                addOre(selectedRockTion, terrain, -1)
        else:
            pass

    # Creation of stones
    # rockName = ore("rock", "Name of the rock for drawing it", hardness, value, damage, minimum height, maximum height)
    dirt = ore("rock", "Dirt", 10, 1, 0, 0, 2)
    stone = ore("rock", "Stone", 25, 2, 1, 2, 74)
    bluestone = ore("rock", "Bluestone", 50, 7, 3, 73, 149)
    redstone = ore("rock", "Redstone", 200, 50, 7, 147, 299)
    bloodstone = ore("rock", "Bloodstone", 500, 150, 15, 298, 449)
    abyssmarine = ore("rock", "Abyssmarine", 1000, 350, 35, 448, 749)
    spaceStone = ore("rock", "Space Stone", 1500, 500, 50, 748, 999)
    space = ore("rock", "Space", 5000, 1000, 100, 998, 1250)

    rocks = [dirt, stone, bluestone, redstone, bloodstone, abyssmarine, spaceStone, space]

    # Creation of minerals
    # mineralName = ore("mineral", "Name of the mineral for drawing it", hardness, value, damage, minimum height, maximum height, chance for it to appear)
    coal = ore("mineral", "Coal", 10, 2, 1, 4, 50, 15)
    iron = ore("mineral", "Iron", 20, 7, 1, 15, 50, 20)
    uniqueOre1 = ore("mineral", "Unique Ore", 100, 15, 5, 0, depth, 100, 1)
    uniqueOre2 = ore("mineral", "Big Unique Ore", 500, 100, 30, 0, depth, 200, 2)
    uniqueOre3 = ore("mineral", "Large Unique Ore", 1000, 1000, 90, 0, depth, 300, 3)

    ores = [coal, iron, uniqueOre1, uniqueOre2, uniqueOre3]

    # Special stuff
    magma = ore("rock","Magma", 70, 50, 50)
    grass = ore("mineral", "Grass", 5, 0, 0)

    # I am le genius

    terrain = []
    height = 0
    for i in range(depth):
        for i in range(20):
            class block:
                # Can be modified by ore/mineral
                ore = 'Dirt'
                extra = ''
                hardness = 10
                value = 1
                damage = 0
                # Exclusivly by unique ore
                uniqueOre = 0
                # Can't be modified by ore/mineral
                x = 0
                y = 0
                rect = pygame.Rect(x,y,32,32)
                mined = False
                health = hardness
                deep = height
            terrain.append(block)
            terrain[-1].x = i*32
            terrain[-1].y = 350+height*32
            terrain[-1].rect = pygame.Rect(terrain[-1].x,terrain[-1].y,32,32)

            # Base rock
            addToTerrain(rocks, terrain)
            if height >= 175 and height <= 700 and random.randint(1, 50) == 1:
                addOre(magma, terrain, -1)
            if height >= 1200 and random.randint(1,4) == 1:
                terrain[-1].ore = ""
                terrain[-1].mined = True
            if height >= 1248 and random.randint(1,2) == 1:
                terrain[-1].ore = ""
                terrain[-1].mined = True

            # Minerals
            addToTerrain(ores, terrain)
            if height == 0:
                addOre(grass, terrain, -1)

            # Extra health the deeper you go
            terrain[-1].hardness += 5*math.floor(((height-10)/10))
            if math.floor(((height-10)/10)) >= 1:
                terrain[-1].value = math.ceil(terrain[-1].value * 1.1 * math.floor(((height-10)/10)))
            terrain[-1].health = terrain[-1].hardness
            
        height += 1
    
    return(terrain)

