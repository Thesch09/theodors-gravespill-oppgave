import pygame
import random
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