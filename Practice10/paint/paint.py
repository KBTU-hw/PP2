import pygame
from pygame.locals import *
import math

pygame.init()
screen=pygame.display.set_mode((800, 600))
canvas=pygame.Surface(screen.get_size())
canvas.fill((255, 255, 255))
running = True
drawing = False
points=[]
mode="brush"
colors=[(255,0, 0), (0, 255, 0), (0, 0, 255)]
color=0
previous_pos=0
x=5
while running:
    screen.fill((255, 255, 255))
    screen.blit(canvas, (0, 0))
    for event in pygame.event.get():
        if event.type==QUIT:
            running=False

        elif event.type==MOUSEBUTTONDOWN:
            if event.button==1:
                drawing=True
                start_pos=event.pos
        elif event.type==MOUSEMOTION:
            current_pos=event.pos
            if drawing:
                if mode=="brush": 
                    if previous_pos: pygame.draw.line(canvas, colors[color], previous_pos, current_pos, x)
                    else: pygame.draw.line(canvas, colors[color], start_pos, current_pos, x)
                if mode=="eraser": 
                    if previous_pos: pygame.draw.line(canvas, (255, 255, 255), previous_pos, current_pos, x)
                    else: pygame.draw.line(canvas, (255, 255, 255), start_pos, current_pos, x)
                if mode=="brush" or mode=="eraser": previous_pos=current_pos
        elif event.type==MOUSEBUTTONUP:
            if event.button==1:
                drawing=False
                end_pos=event.pos
                if mode=="circle": pygame.draw.circle(canvas, colors[color], ((start_pos[0]+end_pos[0])/2, (start_pos[1]+end_pos[1])/2), math.sqrt((start_pos[0]-end_pos[0])**2+(start_pos[1]-end_pos[1])**2)/2)
                if mode=="rect": pygame.draw.rect(canvas, colors[color], (min(start_pos[0], end_pos[0]), min(start_pos[1], end_pos[1]), abs(start_pos[0]-end_pos[0]), abs(start_pos[1]-end_pos[1])))
        elif event.type==KEYDOWN:
            if event.key==K_c: mode="circle"
            if event.key==K_r: mode="rect"
            if event.key==K_b: mode="brush"
            if event.key==K_e: mode="eraser"
            if event.key==K_RIGHT: color=(color+1)%len(colors)
            if event.key==K_LEFT: color=(color-1)%len(colors)
            if event.key==K_UP: x+=1
            if event.key==K_DOWN: x-=1
    if drawing:
        if mode=="circle": pygame.draw.circle(screen, colors[color], ((start_pos[0]+current_pos[0])/2, (start_pos[1]+current_pos[1])/2), math.sqrt((start_pos[0]-current_pos[0])**2+(start_pos[1]-current_pos[1])**2)/2)
        if mode=="rect": pygame.draw.rect(screen, colors[color], (min(start_pos[0], current_pos[0]), min(start_pos[1], current_pos[1]), abs(start_pos[0]-current_pos[0]), abs(start_pos[1]-current_pos[1])))
    pygame.draw.circle(screen, colors[color], (15, 15), 10)
    
    pygame.display.flip()
pygame.quit()