import pygame
import random
import math
# Generate the terrain
def make_terrain(depth):
    terrain = []
    height = 0
    for i in range(depth):
        for i in range(20):
            class block:
                x = 0
                y = 0
                ore = 'Dirt'
                rect = pygame.Rect(x,y,32,32)
                hardness = 10
                mined = False
                extra = ''
                value = 1
                damage = 0
                health = hardness
                uniqueOre = 0
                deep = height
            terrain.append(block)
            terrain[-1].x = i*32
            terrain[-1].y = 350+height*32
            terrain[-1].rect = pygame.Rect(terrain[-1].x,terrain[-1].y,32,32)

            # Base rock
            if height < 3:
                terrain[-1].ore = 'Dirt'
                terrain[-1].value = 1
                terrain[-1].damage = 0
            if height == 2 and random.randint(1,2) == 2:
                terrain[-1].ore = 'Stone'
                terrain[-1].hardness = 25
                terrain[-1].value = 2
                terrain[-1].damage = 1
            if height >= 3:
                terrain[-1].ore = 'Stone'
                terrain[-1].hardness = 25
                terrain[-1].value = 2
                terrain[-1].damage = 1
            if height > 73:
                if random.randint(1,2) == 2:
                    terrain[-1].ore = 'Bluestone'
                    terrain[-1].hardness = 50
                    terrain[-1].value = 7
                    terrain[-1].damage = 3
                else:
                    terrain[-1].ore = 'Stone'
                    terrain[-1].hardness = 25
                    terrain[-1].value = 2
                    terrain[-1].damage = 3
            if height > 75:
                terrain[-1].ore = 'Bluestone'
                terrain[-1].hardness = 50
                terrain[-1].value = 7
                terrain[-1].damage = 3
            if height > 148:
                if random.randint(1,2) == 1:
                    terrain[-1].ore = 'Redstone'
                    terrain[-1].hardness = 200
                    terrain[-1].value = 50
                    terrain[-1].damage = 7
                else:
                    terrain[-1].ore = 'Bluestone'
                    terrain[-1].hardness = 50
                    terrain[-1].value = 7
                    terrain[-1].damage = 3
            if height > 150:
                terrain[-1].ore = 'Redstone'
                terrain[-1].hardness = 200
                terrain[-1].value = 50
                terrain[-1].damage = 7
            if height > 298:
                if random.randint(1,2) == 1:
                    terrain[-1].ore = 'Bloodstone'
                    terrain[-1].hardness = 500
                    terrain[-1].value = 150
                    terrain[-1].damage = 15
                else:
                    terrain[-1].ore = 'Redstone'
                    terrain[-1].hardness = 200
                    terrain[-1].value = 50
                    terrain[-1].damage = 7
            if height > 300:
                terrain[-1].ore = 'Bloodstone'
                terrain[-1].hardness = 500
                terrain[-1].value = 150
                terrain[-1].damage = 15
            if height > 448:
                if random.randint(1,2) == 1:
                    terrain[-1].ore = 'Abyssmarine'
                    terrain[-1].hardness = 1000
                    terrain[-1].value = 350
                    terrain[-1].damage = 35
                else:
                    terrain[-1].ore = 'Bloodstone'
                    terrain[-1].hardness = 500
                    terrain[-1].value = 150
                    terrain[-1].damage = 15
            if height > 450:
                terrain[-1].ore = 'Abyssmarine'
                terrain[-1].hardness = 1000
                terrain[-1].value = 350
                terrain[-1].damage = 35
            if height > 748:
                if random.randint(1,2) == 1:
                    terrain[-1].ore = 'Space Stone'
                    terrain[-1].hardness = 1500
                    terrain[-1].value = 500
                    terrain[-1].damage = 50
                else:
                    terrain[-1].ore = 'Abyssmarine'
                    terrain[-1].hardness = 1000
                    terrain[-1].value = 350
                    terrain[-1].damage = 35
            if height > 750:
                terrain[-1].ore = 'Space Stone'
                terrain[-1].hardness = 1500
                terrain[-1].value = 500
                terrain[-1].damage = 50
            if height > 998:
                if random.randint(1,2) == 1:
                    terrain[-1].ore = 'Space'
                    terrain[-1].hardness = 5000
                    terrain[-1].value = 1000
                    terrain[-1].damage = 100
                else:
                    terrain[-1].ore = 'Space Stone'
                    terrain[-1].hardness = 1500
                    terrain[-1].value = 500
                    terrain[-1].damage = 50
            if height > 1000:
                terrain[-1].ore = 'Space'
                terrain[-1].hardness = 5000
                terrain[-1].value = 1000
                terrain[-1].damage = 100
            if height > 1199:
                if random.randint(1,4) == 1:
                    terrain[-1].ore = ''
                    terrain[-1].mined = True
                else:
                    terrain[-1].ore = 'Space'
                    terrain[-1].hardness = 5000
                    terrain[-1].value = 1000
                    terrain[-1].damage = 100
            if height > 1248:
                if random.randint(1,2) == 1:
                    terrain[-1].ore = ''
                    terrain[-1].mined = True
                else:
                    terrain[-1].ore = 'Space'
                    terrain[-1].hardness = 5000
                    terrain[-1].value = 1000
                    terrain[-1].damage = 100

            if height > 174 and random.randint(1, 50) == 1 and height < 700:
                terrain[-1].ore = 'Magma'
                terrain[-1].hardness = 70
                terrain[-1].value = 50
                terrain[-1].damage = 50
            

            if height == 0 and i == 9 or height == 0 and i == 10:
                terrain[-1].ore = 'Bluestone'
                terrain[-1].hardness = 50
                terrain[-1].value = 7
                terrain[-1].damage = 3
            
            # Ore
            if height == 0:
                terrain[-1].extra = 'Grass'
                terrain[-1].hardness += 5
            if height > 3 and height < 50 and random.randint(1,15) == 1 and terrain[-1].extra == '':
                terrain[-1].extra = 'Coal'
                terrain[-1].hardness += 10
                terrain[-1].value += 2
                terrain[-1].damage += 1
            if height > 15 and height < 50 and random.randint(1,20) == 1 and terrain[-1].extra == '':
                terrain[-1].extra = 'Iron'
                terrain[-1].hardness += 20
                terrain[-1].value += 7
                terrain[-1].damage += 1
            
            # Unique ore
            if terrain[-1].extra == '' and terrain[-1].ore != 'Dirt' and terrain[-1].ore != '' and random.randint(1,100) == 1:
                terrain[-1].extra = 'Unique Ore'
                terrain[-1].hardness += 100
                terrain[-1].uniqueOre = 1
                terrain[-1].damage += 5
                terrain[-1].value += 15
            if terrain[-1].extra == '' and terrain[-1].ore != 'Dirt' and terrain[-1].ore != '' and random.randint(1,200) == 1:
                terrain[-1].extra = 'Big Unique Ore'
                terrain[-1].hardness += 500
                terrain[-1].uniqueOre = 2
                terrain[-1].damage += 30
                terrain[-1].value += 100
            if terrain[-1].extra == '' and terrain[-1].ore != 'Dirt' and terrain[-1].ore != '' and random.randint(1,300) == 1:
                terrain[-1].extra = 'Large Unique Ore'
                terrain[-1].hardness += 1000
                terrain[-1].uniqueOre = 3
                terrain[-1].damage += 90
                terrain[-1].value += 1000

            # Extra health the deeper you go
            terrain[-1].hardness += 5*math.floor(((height-10)/10))
            if math.floor(((height-10)/10)) >= 1:
                terrain[-1].value = math.ceil(terrain[-1].value * 1.1 * math.floor(((height-10)/10)))
            terrain[-1].health = terrain[-1].hardness
            
        height += 1
    
    return(terrain)

