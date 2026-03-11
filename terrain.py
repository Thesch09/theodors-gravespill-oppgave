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
            terrain.append(block)
            terrain[-1].x = i*32
            terrain[-1].y = 350+height*32
            terrain[-1].rect = pygame.Rect(terrain[-1].x,terrain[-1].y,32,32)
            if height < 3:
                terrain[-1].ore = 'Dirt'
                if height == 2 and random.randint(1,2) == 2:
                    terrain[-1].ore = 'Stone'
                    terrain[-1].hardness = 15
            if height >= 3:
                terrain[-1].ore = 'Stone'
                terrain[-1].hardness = 15
            if height > 25:
                if random.randint(1,2) == 2:
                    terrain[-1].ore = 'Bluestone'
                    terrain[-1].hardness = 50
                else:
                    terrain[-1].ore = 'Stone'
                    terrain[-1].hardness = 15
            if height > 27:
                    terrain[-1].ore = 'Bluestone'
                    terrain[-1].hardness = 50
            

        height += 1
    
    return(terrain)

