import pygame
import math
import datetime

pygame.init()

screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Clock")
clock = pygame.time.Clock()

center = (250, 250)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (0, 0, 0), center, 180, 3)

    now = datetime.datetime.now()
    min = now.minute
    sec = now.second

    sec_angle = math.radians(sec * 6 - 90)
    min_angle = math.radians(min * 6 - 90)

    sec_x = center[0] + math.cos(sec_angle) * 140
    sec_y = center[1] + math.sin(sec_angle) * 140

    min_x = center[0] + math.cos(min_angle) * 100
    min_y = center[1] + math.sin(min_angle) * 100

    pygame.draw.line(screen, (255, 0, 0), center, (sec_x, sec_y), 2)
    pygame.draw.line(screen, (0, 0, 255), center, (min_x, min_y), 5)

    pygame.draw.circle(screen, (0, 0, 0), center, 6)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()