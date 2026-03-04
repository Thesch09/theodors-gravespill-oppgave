import pygame
from terrain import make_terrain

pygame.init()

# Set up
screen = pygame.display.set_mode((640, 480))
running = True
clock = pygame.time.Clock()
delta_time = 0.1
y = 0

# Temporary creation of stone
stone = pygame.image.load('img/stone-v1.png').convert_alpha()
stone = pygame.transform.scale(stone,
                               (stone.get_width() * 2,
                               stone.get_height() * 2))

while running:
    screen.fill((0,0,0))

    screen.blit(stone, (0,0))
    temp = pygame.Rect(240, y, 24, 32)
    y += 50 * delta_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.draw.rect(screen, (255,255,255), temp)

    pygame.display.flip()

    delta_time = clock.tick(60) / 1000
    delta_time = max(0.001, min((0.1, delta_time)))

pygame.quit()