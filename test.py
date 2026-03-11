import pygame
screen = pygame.display.set_mode((640, 480))

class egg:
    def __init__(self, name, idx):
        self.name = name+ str(idx)
        self.rect = pygame.Rect(32, 32, 32, 32)

idx = "4"
ground = egg("ground", 4)
print(ground.name)
print(ground.rect)
running = True
while running:

    pygame.draw.rect(screen, (255, 0, 0), ground)

    pygame.display.flip()


pygame.quit()