import pygame
import random
import math
from config import *


class Snake:
    def __init__(self, color=SNAKE_COLOR_DEFAULT):
        self.body = [(WIDTH // 2, HEIGHT // 2), (WIDTH // 2 - GRID_SIZE, HEIGHT // 2), (WIDTH // 2 - 2 * GRID_SIZE, HEIGHT // 2)]
        self.direction = (1, 0)  # Right
        self.next_direction = (1, 0)
        self.color = color
        self.grow_pending = 0
    
    def update(self, speed):
        """Move snake in the current direction"""
        # Update direction if a new direction was queued
        self.direction = self.next_direction
        
        # Calculate new head position
        head_x, head_y = self.body[0]
        new_x = head_x + self.direction[0] * GRID_SIZE * speed
        new_y = head_y + self.direction[1] * GRID_SIZE * speed
        
        self.body.insert(0, (new_x, new_y))
        
        # Handle growing
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()
    
    def change_direction(self, new_direction):
        """Queue a new direction (prevents reversing into itself)"""
        # Prevent reversing
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.next_direction = new_direction
    
    def grow(self, segments=1):
        """Queue growth"""
        self.grow_pending += segments
    
    def shrink(self, segments=1):
        """Remove segments from the tail"""
        for _ in range(min(segments, len(self.body) - 1)):
            self.body.pop()
    
    def check_wall_collision(self):
        """Check collision with walls"""
        head_x, head_y = self.body[0]
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            return True
        return False
    
    def check_self_collision(self):
        """Check collision with itself"""
        head = self.body[0]
        return head in self.body[1:]
    
    def check_obstacle_collision(self, obstacles):
        """Check collision with obstacles"""
        head = self.body[0]
        for obs in obstacles:
            if head == obs:
                return True
        return False
    
    def draw(self, surface):
        """Draw snake on surface"""
        for i, segment in enumerate(self.body):
            pygame.draw.rect(surface, self.color, (segment[0], segment[1], GRID_SIZE - 2, GRID_SIZE - 2))
            # Draw head with outline
            if i == 0:
                pygame.draw.rect(surface, (255, 255, 255), (segment[0], segment[1], GRID_SIZE - 2, GRID_SIZE - 2), 2)


class Food:
    def __init__(self, food_type=FOOD_NORMAL, snake_body=None, obstacles=None):
        self.type = food_type
        self.spawn_time = pygame.time.get_ticks()
        self.position = self.random_position(snake_body, obstacles)
    
    def random_position(self, snake_body=None, obstacles=None):
        """Generate random position avoiding snake body and obstacles"""
        while True:
            x = random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE
            y = random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
            
            # Check if position is valid
            if snake_body and (x, y) in snake_body:
                continue
            if obstacles and (x, y) in obstacles:
                continue
            
            return (x, y)
    
    def get_color(self):
        """Get color based on food type"""
        if self.type == FOOD_NORMAL:
            return FOOD_COLOR
        elif self.type == FOOD_WEIGHTED:
            return (255, 165, 0)  # Orange
        elif self.type == FOOD_DISAPPEARING:
            return (255, 192, 203)  # Light pink
        elif self.type == FOOD_POISON:
            return POISON_COLOR
        return FOOD_COLOR
    
    def get_points(self):
        """Get points for eating this food"""
        if self.type == FOOD_NORMAL:
            return FOOD_NORMAL_POINTS
        elif self.type == FOOD_WEIGHTED:
            return FOOD_WEIGHTED_POINTS
        elif self.type == FOOD_POISON:
            return FOOD_POISON_POINTS
        return FOOD_NORMAL_POINTS
    
    def is_expired(self):
        """Check if food has expired (for disappearing food)"""
        if self.type == FOOD_DISAPPEARING:
            return pygame.time.get_ticks() - self.spawn_time > FOOD_DISAPPEAR_TIME
        return False
    
    def draw(self, surface):
        """Draw food on surface"""
        color = self.get_color()
        pygame.draw.rect(surface, color, (self.position[0], self.position[1], GRID_SIZE - 2, GRID_SIZE - 2))
        pygame.draw.rect(surface, (255, 255, 255), (self.position[0], self.position[1], GRID_SIZE - 2, GRID_SIZE - 2), 1)


class PowerUp:
    def __init__(self, powerup_type, snake_body=None, obstacles=None):
        self.type = powerup_type
        self.spawn_time = pygame.time.get_ticks()
        self.position = self.random_position(snake_body, obstacles)
    
    def random_position(self, snake_body=None, obstacles=None):
        """Generate random position avoiding snake body and obstacles"""
        while True:
            x = random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE
            y = random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
            
            if snake_body and (x, y) in snake_body:
                continue
            if obstacles and (x, y) in obstacles:
                continue
            
            return (x, y)
    
    def is_expired(self):
        """Check if power-up has expired"""
        return pygame.time.get_ticks() - self.spawn_time > POWERUP_SPAWN_TIME
    
    def draw(self, surface):
        """Draw power-up on surface"""
        color = POWER_UP_COLOR if self.type != POWERUP_SHIELD else SHIELD_COLOR
        pygame.draw.rect(surface, color, (self.position[0], self.position[1], GRID_SIZE - 2, GRID_SIZE - 2))
        pygame.draw.rect(surface, (255, 255, 255), (self.position[0], self.position[1], GRID_SIZE - 2, GRID_SIZE - 2), 2)


class GameState:
    def __init__(self, username, snake_color=SNAKE_COLOR_DEFAULT):
        self.username = username
        self.snake = Snake(color=snake_color)
        self.foods = [self.spawn_food()]
        self.power_up = None
        self.obstacles = []
        self.score = 0
        self.level = 1
        self.food_count = 0
        self.game_over = False
        self.game_over_reason = ""
        self.speed = INITIAL_SPEED
        self.speed_boost_active = False
        self.speed_boost_end = 0
        self.slow_motion_active = False
        self.slow_motion_end = 0
        self.shield_active = False
        self.powerup_effect_end = 0
        self.frame_count = 0
        self.power_up_spawn_counter = 0
        self.next_power_up_spawn = random.randint(30, 80)  # Frames until next power-up
    
    def spawn_food(self):
        """Spawn a new food item with random type"""
        food_type = random.choices(
            [FOOD_NORMAL, FOOD_WEIGHTED, FOOD_DISAPPEARING, FOOD_POISON],
            weights=[60, 20, 15, 5],
            k=1
        )[0]
        return Food(food_type, self.snake.body, self.obstacles)
    
    def spawn_powerup(self):
        """Spawn a new power-up"""
        if self.power_up is None:
            powerup_type = random.choice([POWERUP_SPEED_BOOST, POWERUP_SLOW_MOTION, POWERUP_SHIELD])
            self.power_up = PowerUp(powerup_type, self.snake.body, self.obstacles)
    
    def spawn_obstacles_for_level(self):
        """Spawn obstacles for the current level"""
        if self.level >= OBSTACLE_START_LEVEL:
            num_obstacles = min(self.level - 2, MAX_OBSTACLES_PER_LEVEL)
            self.obstacles = []
            
            # Generate obstacles without trapping the snake
            attempts = 0
            while len(self.obstacles) < num_obstacles and attempts < 100:
                obs_x = random.randint(1, (WIDTH // GRID_SIZE) - 2) * GRID_SIZE
                obs_y = random.randint(1, (HEIGHT // GRID_SIZE) - 2) * GRID_SIZE
                
                # Don't spawn on snake
                if (obs_x, obs_y) not in self.snake.body:
                    self.obstacles.append((obs_x, obs_y))
                
                attempts += 1
    
    def level_up(self):
        """Advance to the next level"""
        self.level += 1
        self.speed = min(self.speed + 1, MAX_SPEED)
        self.food_count = 0
        self.spawn_obstacles_for_level()
    
    def update(self):
        """Update game state"""
        self.frame_count += 1
        
        # Update speed effects
        current_time = pygame.time.get_ticks()
        
        if self.speed_boost_active and current_time > self.speed_boost_end:
            self.speed_boost_active = False
        
        if self.slow_motion_active and current_time > self.slow_motion_end:
            self.slow_motion_active = False
        
        if self.shield_active and current_time > self.powerup_effect_end:
            self.shield_active = False
        
        # Calculate actual speed
        actual_speed = self.speed
        if self.speed_boost_active:
            actual_speed = min(actual_speed * 1.5, MAX_SPEED)
        elif self.slow_motion_active:
            actual_speed = max(actual_speed * 0.5, 1)
        
        # Move snake
        self.snake.update(actual_speed)
        
        # Check collisions
        if self.snake.check_wall_collision():
            if not self.shield_active:
                self.game_over = True
                self.game_over_reason = "Hit a wall"
            else:
                self.shield_active = False
        
        if self.snake.check_self_collision():
            if not self.shield_active:
                self.game_over = True
                self.game_over_reason = "Hit yourself"
            else:
                self.shield_active = False
        
        if self.snake.check_obstacle_collision(self.obstacles):
            if not self.shield_active:
                self.game_over = True
                self.game_over_reason = "Hit an obstacle"
            else:
                self.shield_active = False
        
        # Check food collision
        for food in self.foods[:]:
            if self.snake.body[0] == food.position:
                self.foods.remove(food)
                
                points = food.get_points()
                if food.type == FOOD_POISON:
                    self.snake.shrink(2)
                    if len(self.snake.body) <= 1:
                        self.game_over = True
                        self.game_over_reason = "Ate poison food"
                else:
                    self.snake.grow(1)
                    self.food_count += 1
                
                self.score += max(0, points)
                
                # Check level up
                if self.food_count >= LEVEL_FOOD_THRESHOLD:
                    self.level_up()
                
                # Spawn new food
                self.foods.append(self.spawn_food())
            elif food.is_expired():
                self.foods.remove(food)
                self.foods.append(self.spawn_food())
        
        # Check power-up collision
        if self.power_up and self.snake.body[0] == self.power_up.position:
            self.apply_powerup(self.power_up.type)
            self.power_up = None
        
        # Spawn power-up
        if self.power_up is None or self.power_up.is_expired():
            if self.power_up and self.power_up.is_expired():
                self.power_up = None
            
            self.power_up_spawn_counter += 1
            if self.power_up_spawn_counter >= self.next_power_up_spawn:
                self.spawn_powerup()
                self.power_up_spawn_counter = 0
                self.next_power_up_spawn = random.randint(30, 80)
    
    def apply_powerup(self, powerup_type):
        """Apply power-up effect"""
        current_time = pygame.time.get_ticks()
        
        if powerup_type == POWERUP_SPEED_BOOST:
            self.speed_boost_active = True
            self.speed_boost_end = current_time + POWERUP_EFFECT_DURATION
        elif powerup_type == POWERUP_SLOW_MOTION:
            self.slow_motion_active = True
            self.slow_motion_end = current_time + POWERUP_EFFECT_DURATION
        elif powerup_type == POWERUP_SHIELD:
            self.shield_active = True
            self.powerup_effect_end = current_time + SHIELD_DURATION
    
    def draw(self, surface, show_grid=False):
        """Draw game state on surface"""
        surface.fill(BG_COLOR)
        
        # Draw grid if enabled
        if show_grid:
            for x in range(0, WIDTH, GRID_SIZE):
                pygame.draw.line(surface, (50, 50, 50), (x, 0), (x, HEIGHT), 1)
            for y in range(0, HEIGHT, GRID_SIZE):
                pygame.draw.line(surface, (50, 50, 50), (0, y), (WIDTH, y), 1)
        
        # Draw obstacles
        for obs in self.obstacles:
            pygame.draw.rect(surface, OBSTACLE_COLOR, (obs[0], obs[1], GRID_SIZE - 2, GRID_SIZE - 2))
        
        # Draw food
        for food in self.foods:
            food.draw(surface)
        
        # Draw power-up
        if self.power_up:
            self.power_up.draw(surface)
        
        # Draw snake
        self.snake.draw(surface)
        
        # Draw UI
        self.draw_ui(surface)
    
    def draw_ui(self, surface):
        """Draw UI elements like score and level"""
        font = pygame.font.Font(None, 24)
        
        # Score
        score_text = font.render(f"Score: {self.score}", True, TEXT_COLOR)
        surface.blit(score_text, (10, 10))
        
        # Level
        level_text = font.render(f"Level: {self.level}", True, TEXT_COLOR)
        surface.blit(level_text, (10, 35))
        
        # Speed
        speed_text = font.render(f"Speed: {self.speed}", True, TEXT_COLOR)
        surface.blit(speed_text, (10, 60))
        
        # Power-up status
        if self.speed_boost_active:
            boost_text = font.render("SPEED BOOST", True, (255, 255, 0))
            surface.blit(boost_text, (WIDTH - 150, 10))
        
        if self.slow_motion_active:
            slow_text = font.render("SLOW MOTION", True, (100, 200, 255))
            surface.blit(slow_text, (WIDTH - 150, 10))
        
        if self.shield_active:
            shield_text = font.render("SHIELD", True, (0, 255, 255))
            surface.blit(shield_text, (WIDTH - 150, 10))
