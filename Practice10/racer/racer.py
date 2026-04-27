import pygame
from pygame.locals import *
import random

pygame.init()
screen=pygame.display.set_mode((600,800))
def new(): return random.randint(50, 450)
car=pygame.transform.scale(pygame.image.load("Practice10/racer/objects/car.png"), (100, 150))
cone=pygame.transform.scale(pygame.image.load("Practice10/racer/objects/cone.png"), (100, 150))
road=pygame.transform.rotate(pygame.transform.scale(pygame.image.load("Practice10/racer/objects/road.webp"), (800, 600)), 90)

running=True
p_x, p_y=275, 700 
o_x, o_y=new(), 0
c_x, c_y=new(), 0
v=10
points=0

while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
    
    key=pygame.key.get_pressed()
    if key[K_RIGHT]: p_x+=10
    if key[K_LEFT]: p_x-=10
    o_y+=v
    c_y+=v
    if p_x<0: p_x=0
    if p_x>500: p_x=500
    if o_y>800: o_x, o_y=new(), 0
    if c_y>800: c_x, c_y=new(), 0
    car_rect=pygame.Rect(p_x, p_y, 100, 150)
    cone_rect=pygame.Rect(o_x, o_y, 100, 150)
    coin_rect=pygame.Rect(c_x, c_y, 100, 100)
    if car_rect.colliderect(cone_rect): running=False
    if car_rect.colliderect(coin_rect):
        points, v=points+1, v+1
        c_x, c_y=new(), 0

    
    screen.blit(road, (0, 0))
    pygame.draw.circle(screen, (255, 215, 0), (c_x+50, c_y+50), 50)
    screen.blit(cone, (o_x, o_y))
    screen.blit(car, (p_x, p_y))

    pygame.display.flip()
    pygame.time.Clock().tick(45)
pygame.quit()