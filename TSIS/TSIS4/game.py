import random
import pygame

WIDTH, HEIGHT = 600, 400
CELL = 20

class SnakeGame:
    def __init__(self, username):
        self.username = username
        self.snake_color = (0, 180, 80)

        self.snake = [(WIDTH // 2, HEIGHT // 2), (WIDTH // 2 - CELL, HEIGHT // 2), (WIDTH // 2 - 2 * CELL, HEIGHT // 2)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)

        self.score = 0
        self.level = 1
        self.eaten_for_level = 0
        self.game_over = False

        self.move_delay = 130
        self.last_move = pygame.time.get_ticks()

        self.food = None
        self.poison = None
        self.power_up = None
        self.power_spawn_tick = pygame.time.get_ticks()

        self.speed_until = 0
        self.slow_until = 0
        self.shield_hits = 0

        self.obstacles = []
        self.spawn_food()

    def cell_positions(self):
        return [(x, y) for x in range(0, WIDTH, CELL) for y in range(0, HEIGHT, CELL)]

    def random_free_cell(self, blocked):
        free = [c for c in self.cell_positions() if c not in blocked]
        return random.choice(free) if free else None

    def blocked_cells(self):
        blocked = set(self.snake)
        blocked.update(self.obstacles)
        if self.food:
            blocked.add(self.food["pos"])
        if self.poison:
            blocked.add(self.poison)
        if self.power_up:
            blocked.add(self.power_up["pos"])
        return blocked

    def spawn_food(self):
        values = [10, 20, 30]
        weights = [60, 30, 10]
        value = random.choices(values, weights=weights, k=1)[0]
        pos = self.random_free_cell(self.blocked_cells())
        if pos:
            self.food = {"pos": pos, "value": value, "expire": pygame.time.get_ticks() + 9000}

    def spawn_poison(self):
        if self.poison is not None:
            return
        if random.random() < 0.02:
            pos = self.random_free_cell(self.blocked_cells())
            if pos:
                self.poison = pos

    def spawn_power(self):
        now = pygame.time.get_ticks()
        if self.power_up is not None:
            if now > self.power_up["expire"]:
                self.power_up = None
            return
        if now - self.power_spawn_tick < 6000:
            return
        self.power_spawn_tick = now
        pos = self.random_free_cell(self.blocked_cells())
        if not pos:
            return
        kind = random.choice(["speed_boost", "slow_motion", "shield"])
        self.power_up = {"pos": pos, "kind": kind, "expire": now + 8000}

    def can_turn(self, d):
        return (d[0] * -1, d[1] * -1) != self.direction

    def set_direction(self, d):
        if self.can_turn(d):
            self.next_direction = d

    def effective_delay(self):
        base = max(55, 130 - (self.level - 1) * 8)
        now = pygame.time.get_ticks()
        if now < self.speed_until:
            base = int(base * 0.65)
        if now < self.slow_until:
            base = int(base * 1.5)
        return max(40, base)

    def level_up(self):
        self.level += 1
        self.eaten_for_level = 0
        if self.level >= 3:
            self.generate_obstacles()

    def generate_obstacles(self):
        head = self.snake[0]
        count = min(self.level, 8)
        blocked = self.blocked_cells()
        new_obs = []
        tries = 0
        while len(new_obs) < count and tries < 400:
            tries += 1
            pos = self.random_free_cell(blocked.union(set(new_obs)))
            if not pos:
                break
            dx = abs(pos[0] - head[0]) // CELL
            dy = abs(pos[1] - head[1]) // CELL
            if dx + dy <= 1:
                continue
            new_obs.append(pos)

        neighbors = [(head[0] + CELL, head[1]), (head[0] - CELL, head[1]), (head[0], head[1] + CELL), (head[0], head[1] - CELL)]
        free_neighbors = 0
        for n in neighbors:
            if 0 <= n[0] < WIDTH and 0 <= n[1] < HEIGHT and n not in new_obs:
                free_neighbors += 1
        if free_neighbors >= 2:
            self.obstacles = new_obs

    def use_shield_or_die(self):
        if self.shield_hits > 0:
            self.shield_hits = 0
            return
        self.game_over = True

    def step(self):
        self.direction = self.next_direction
        hx, hy = self.snake[0]
        nx = hx + self.direction[0] * CELL
        ny = hy + self.direction[1] * CELL
        head = (nx, ny)

        if nx < 0 or nx >= WIDTH or ny < 0 or ny >= HEIGHT:
            self.use_shield_or_die()
            if self.game_over:
                return
            head = self.snake[0]

        if head in self.snake:
            self.use_shield_or_die()
            if self.game_over:
                return

        if head in self.obstacles:
            self.use_shield_or_die()
            if self.game_over:
                return

        self.snake.insert(0, head)
        grow = False

        if self.food and head == self.food["pos"]:
            self.score += self.food["value"]
            self.eaten_for_level += 1
            grow = True
            self.food = None
            self.spawn_food()
            if self.eaten_for_level >= 5:
                self.level_up()

        if self.poison and head == self.poison:
            self.poison = None
            for _ in range(2):
                if len(self.snake) > 1:
                    self.snake.pop()
            if len(self.snake) <= 1:
                self.game_over = True
                return

        if self.power_up and head == self.power_up["pos"]:
            kind = self.power_up["kind"]
            now = pygame.time.get_ticks()
            if kind == "speed_boost":
                self.speed_until = now + 5000
            elif kind == "slow_motion":
                self.slow_until = now + 5000
            elif kind == "shield":
                self.shield_hits = 1
            self.power_up = None

        if not grow:
            self.snake.pop()

    def update(self):
        now = pygame.time.get_ticks()
        if self.food and now > self.food["expire"]:
            self.food = None
            self.spawn_food()

        self.spawn_poison()
        self.spawn_power()

        if now - self.last_move >= self.effective_delay() and not self.game_over:
            self.last_move = now
            self.step()

    def draw(self, screen, font_small):
        screen.fill((26, 26, 26))

        for o in self.obstacles:
            pygame.draw.rect(screen, (110, 110, 110), (o[0], o[1], CELL - 2, CELL - 2))

        if self.food:
            color = (255, 70, 70)
            if self.food["value"] == 20:
                color = (255, 165, 0)
            if self.food["value"] == 30:
                color = (255, 220, 120)
            pygame.draw.rect(screen, color, (self.food["pos"][0], self.food["pos"][1], CELL - 2, CELL - 2))

        if self.poison:
            pygame.draw.rect(screen, (140, 0, 140), (self.poison[0], self.poison[1], CELL - 2, CELL - 2))

        if self.power_up:
            pygame.draw.rect(screen, (0, 220, 220), (self.power_up["pos"][0], self.power_up["pos"][1], CELL - 2, CELL - 2))

        for i, s in enumerate(self.snake):
            c = self.snake_color if i > 0 else (220, 220, 220)
            pygame.draw.rect(screen, c, (s[0], s[1], CELL - 2, CELL - 2))

        screen.blit(font_small.render(f"User: {self.username}", True, (255, 255, 255)), (10, 8))
        screen.blit(font_small.render(f"Score: {self.score}", True, (255, 255, 255)), (10, 30))
        screen.blit(font_small.render(f"Level: {self.level}", True, (255, 255, 255)), (10, 52))
        screen.blit(font_small.render(f"Shield: {'On' if self.shield_hits else 'Off'}", True, (255, 255, 255)), (10, 74))
