import pygame
from pygame.locals import *
import random

pygame.init()
screen = pygame.display.set_mode((600, 400))
coin_position = (random.randint(10, 590), random.randint(10, 390))
class Snake:
    def __init__(self):
        self.body = [(100, 100), (90, 100), (80, 100)]
        self.direction = 'RIGHT'
        self.grow = False

    def move(self):
        head_x, head_y = self.body[0]
        if self.direction == 'RIGHT':
            new_head = (head_x + 10, head_y)
        elif self.direction == 'LEFT':
            new_head = (head_x - 10, head_y)
        elif self.direction == 'UP':
            new_head = (head_x, head_y - 10)
        elif self.direction == 'DOWN':
            new_head = (head_x, head_y + 10)

        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_direction(self, new_direction):
        opposite_directions = {'RIGHT': 'LEFT', 'LEFT': 'RIGHT', 'UP': 'DOWN', 'DOWN': 'UP'}
        if new_direction != opposite_directions[self.direction]:
            self.direction = new_direction

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, (0, 255, 0), (*segment, 10, 10))
    def check_collision(self):
        head = self.body[0]
        if head[0] < 0 or head[0] >= 600 or head[1] < 0 or head[1] >= 400:
            return True
        if head in self.body[1:]:
            return True
        return False
running = True
snake = Snake()
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
                snake.change_direction('RIGHT')
            elif event.key == K_LEFT:
                snake.change_direction('LEFT')
            elif event.key == K_UP:
                snake.change_direction('UP')
            elif event.key == K_DOWN:
                snake.change_direction('DOWN')
    snake.move()
    coin_rect = pygame.Rect(coin_position[0], coin_position[1], 10, 10)
    snake_head_rect = pygame.Rect(snake.body[0][0], snake.body[0][1], 10, 10)
    if snake.check_collision():
        print("Game Over!")
        running = False
    if snake_head_rect.colliderect(coin_rect):
        snake.grow = True
        coin_position = (random.randint(10, 590), random.randint(10, 390))
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (255, 0, 0), (coin_position[0] + 5, coin_position[1] + 5), 5)
    snake.draw(screen)
    pygame.display.flip()
    pygame.time.Clock().tick(15)
pygame.quit()