import pygame
pygame.init()
screen = pygame.display.set_mode((640, 480))


stone = pygame.image.load('img/stone-v1.png').convert_alpha()
stone = pygame.transform.scale(stone,
                               (stone.get_width() * 2,
                               stone.get_height() * 2))
running = True

depth = 0
blocks = []
for i in range(20):
    class block:
        x=0
        y=0
        ore='Stone'
        rect=pygame.Rect(x,y,32,32)
        hardness=60
        mined=False
    blocks.append(block)
    blocks[-1].x=i*32
    blocks[-1].y=350+(depth*32)
    blocks[-1].rect=pygame.Rect(i,350,32,32)

while running:
    for i in blocks:
        if not i.mined and i.y<640 and i.y>-32:
            if i.ore=='Stone':
                screen.blit(stone,(i.x,i.y))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        pressed = pygame.key.get_pressed()