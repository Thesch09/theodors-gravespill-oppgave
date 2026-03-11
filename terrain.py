import pygame
import random
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
            terrain.append(block)
            terrain[-1].x = i*32
            terrain[-1].y = 350+height*32
            terrain[-1].rect = pygame.Rect(terrain[-1].x,terrain[-1].y,32,32)

            # Base rock
            if height < 3:
                terrain[-1].ore = 'Dirt'
                terrain[-1].value = 1
            if height == 2 and random.randint(1,2) == 2:
                terrain[-1].ore = 'Stone'
                terrain[-1].hardness = 25
                terrain[-1].extra = ''
                terrain[-1].value = 2
            if height >= 3:
                terrain[-1].ore = 'Stone'
                terrain[-1].hardness = 25
                terrain[-1].extra = ''
                terrain[-1].value = 2
            if height > 25:
                if random.randint(1,2) == 2:
                    terrain[-1].ore = 'Bluestone'
                    terrain[-1].hardness = 50
                    terrain[-1].extra = ''
                    terrain[-1].value = 7
                else:
                    terrain[-1].ore = 'Stone'
                    terrain[-1].hardness = 25
                    terrain[-1].extra = ''
                    terrain[-1].value = 2
            if height > 27:
                    terrain[-1].ore = 'Bluestone'
                    terrain[-1].hardness = 50
                    terrain[-1].extra = ''
                    terrain[-1].value = 7
            
            # Ore
            if height == 0:
                terrain[-1].extra = 'Grass'
                terrain[-1].hardness += 5
            if height > 3 and height < 50 and random.randint(1,15) == 1:
                terrain[-1].extra = 'Coal'
                terrain[-1].hardness += 10
                terrain[-1].value += 2
            if height > 3 and height < 50 and random.randint(1,20) == 1:
                terrain[-1].extra = 'Iron'
                terrain[-1].hardness += 20
                terrain[-1].value += 5
            

        height += 1
    
    return(terrain)

