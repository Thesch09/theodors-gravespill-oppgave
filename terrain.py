import pygame
import random
import math
import os
# Generate the terrain
def saveTerrain(terrain,save):
    if os.path.exists(f"!saves/save{save}/terrain.txt"):
        os.remove(f"!saves/save{save}/terrain.txt")
    else:
        print("The file does not exist")
    for i in terrain:
        with open(f"!saves/save{save}/terrain.txt", "a") as world:
            world.write(f"Position: {str(int(i.y/32))},{str(int(i.x/32))}\n")
            if not i.mined:
                if i.extra != "":
                    world.write(f"\tStone: {i.ore} with {i.extra}\n")
                else:
                    world.write(f"\tStone: {i.ore}\n")
                world.write(f"\tHardness: {i.hardness}\n")
                if i.health < i.hardness:
                    world.write(f"\tRemaining Health: {i.health}")
                world.write(f"\tValue: {i.value}\n")
                if i.uniqueOre > 0:
                    world.write(f"\tUnique Ore: {i.uniqueOre}\n")
                if i.damage > 0:
                    world.write(f"\tDamage: {i.damage}\n")
            if i.mined:
                world.write("\tMined\n")
                if i.extra == "Grass":
                    world.write(f"\tStone: {i.ore} with {i.extra}\n")
                else:
                    world.write(f"\tStone: {i.ore}\n")


def loadTerrain(save):
    terrain = []
    with open(f"!saves/save{save}/terrain.txt") as world:
        for tile in world:
            class block:
                # Can be modified by ore/mineral
                ore = ''
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
                deep = None
            split = tile.split()
            if split[0] == "Position:":
                terrain.append(block)
                splits = split[1].split(",") 
                terrain[-1].deep = int(splits[0])
                terrain[-1].y = 32*int(splits[0])
                terrain[-1].x = 32*int(splits[1])
            if split[0] == "Stone:":
                withFound = False
                for i in split:
                    if i != "Stone:" and i != "with":
                        if not withFound:
                            terrain[-1].ore = terrain[-1].ore + i
                        else:
                            terrain[-1].extra = terrain[-1].extra + i
                    if i == "with":
                        withFound = True
            if split[0] == "Hardness:":
                terrain[-1].hardness == int(split[1])
            if split[0] == "Mined":
                terrain[-1].mined = True
            if split[0] == "Health:":
                terrain[-1].health = float(split[1])
            if split[0] == "Damage:":
                terrain[-1].damage += int(split[1])
    return(terrain)
                


def make_terrain(depth, save):
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
            if ore.name == "eye":
                terrain[location].extra = eyes[random.randint(0,2)]
            elif ore.name == "squint":
                terrain[location].extra = f"Squinting {eyes[random.randint(0,2)]}"
            else:
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
        if len(rockTions) >= 1:
            if i.type == "rock":
                selectedRockTion = rockTions[random.randint(0, len(rockTions)-1)]
                addOre(selectedRockTion, terrain, -1)
            if i.type == "mineral":
                for i in rockTions:
                    if random.randint(1, i.chance) == 1 and terrain[-1].ore != "" and terrain[-1].ore != "Dirt":
                        addOre(i, terrain, -1)
                        break
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
    space = ore("rock", "Space", 5000, 1000, 100, 998, depth)

    rocks = [dirt, stone, bluestone, redstone, bloodstone, abyssmarine, spaceStone, space]

    # Creation of minerals
    # mineralName = ore("mineral", "Name of the mineral for drawing it", hardness, value, damage, minimum height, maximum height, chance for it to appear)
    coal = ore("mineral", "Coal", 10, 2, 1, 4, 200, 35)
    iron = ore("mineral", "Iron", 20, 7, 1, 15, 500, 40)
    star = ore("mineral", "Star", 500, 1000, 25, 750, depth, 30)
    star2 = ore("mineral", "Large Star", 1000, 2000, 25, 1000, depth, 50)
    gold = ore("mineral", "Gold", 50, 20, 2, 175, 550, 50)
    copper = ore("mineral", "Copper", 35, 10, 0, 15, 400, 80)
    diamond = ore("mineral", "Diamond", 100, 500, 10, 50, 900, 150)
    rainbowite = ore("mineral", "Rainbowite", 50, 50000, 100, 100, 1200, 1000)
    bismuth = ore("mineral", "Bismuth", -25, 300, 5, 100, 200, 35)
    lapisLazuli = ore("mineral", "Lapis Lazuli", 50, 150, 2, 450, 725, 50)
    uniqueOre1 = ore("mineral", "Unique Ore", 100, 15, 5, 0, depth, 100, 1)
    uniqueOre2 = ore("mineral", "Big Unique Ore", 500, 100, 30, 0, depth, 200, 2)
    uniqueOre3 = ore("mineral", "Large Unique Ore", 1000, 1000, 90, 0, depth, 300, 3)
    eye = ore("mineral", "eye", 100, 50, 0, 300, 440, 90)
    eyeSquint = ore("mineral", "squint", 150, 50, 0, 300, 440, 90)
    mouth = ore("mineral", "Mouth", 200, 200, 20, 300, 440, 80)

    eyes = ["Blue Eye","Green Eye","Red Eye"]
    ores = [coal, iron, star, star2, gold, copper, diamond, rainbowite, bismuth, lapisLazuli, uniqueOre1, uniqueOre2, uniqueOre3, eye, eyeSquint, mouth]

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
            terrain[-1].y = height*32

            # Base rock
            addToTerrain(rocks, terrain)
            if height >= 175 and height <= 700 and random.randint(1, 50) == 1:
                addOre(magma, terrain, -1)
            if height >= 1200 and random.randint(1,4) == 1:
                terrain[-1].mined = True
            if height >= 1248 and random.randint(1,2) == 1:
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
    # Add to the terrain.txt file
    saveTerrain(terrain, save)



    return(terrain)