import pygame
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Moving Ball")
running = True
x, y=50, 50
clock = pygame.time.Clock()
while running:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    key=pygame.key.get_pressed()
    if key[K_LEFT]:
        x += -20
    if key[K_RIGHT]:
        x += 20
    if key[K_UP]:
        y += -20
    if key[K_DOWN]:
        y += 20

    if x<25: x=25
    if x>375: x=375
    if y<25: y=25
    if y>275: y=275

    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (255, 0, 0), (x, y), 25)
    pygame.display.flip()
pygame.quit()