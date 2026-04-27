import json
import random
from pathlib import Path

import pygame

pygame.init()

W, H = 900, 650
ROAD_X, ROAD_W = 170, 560
LANES = 4
LANE_W = ROAD_W // LANES
FPS = 60

BASE = Path(__file__).resolve().parent
ASSETS_DIR = BASE / "assets"
LEADER_FILE = BASE / "leaderboard.json"

DIFF = {"easy": 0.85, "normal": 1.0, "hard": 1.2}
POWERUP_TYPES = ["nitro"]


class Button:
    def __init__(self, x, y, w, h, text, action):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.action = action

    def draw(self, screen, font):
        mouse = pygame.mouse.get_pos()
        hover = self.rect.collidepoint(mouse)
        pygame.draw.rect(screen, (120, 160, 255) if hover else (230, 234, 244), self.rect, border_radius=8)
        pygame.draw.rect(screen, (30, 30, 30), self.rect, 2, border_radius=8)
        txt = font.render(self.text, True, (20, 20, 20))
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    def click(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


def lane_center(idx):
    return ROAD_X + idx * LANE_W + LANE_W // 2


def load_json(path, default):
    try:
        if not path.exists():
            return default
        data = json.loads(path.read_text(encoding="utf-8"))
        return data
    except Exception:
        return default


def save_json(path, data):
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def load_image(filename, size):
    try:
        img = pygame.image.load(ASSETS_DIR / filename)
        return pygame.transform.scale(img, size)
    except Exception:
        return None


def load_leaderboard():
    data = load_json(LEADER_FILE, [])
    return data if isinstance(data, list) else []


def add_score(name, score, distance, coins, difficulty):
    rows = load_leaderboard()
    rows.append({"name": name, "score": int(score), "distance": int(distance), "coins": int(coins), "difficulty": difficulty})
    rows.sort(key=lambda x: x.get("score", 0), reverse=True)
    save_json(LEADER_FILE, rows[:10])


class Game:
    def __init__(self, username):
        self.username = username
        self.diff = "normal"
        self.diff_mul = DIFF.get(self.diff, 1.0)

        self.player_lane = 1
        self.player = pygame.Rect(0, 0, 56, 96)
        self.player.center = (lane_center(self.player_lane), H - 90)

        self.img_player = load_image("player_car.png", (56, 96))
        self.img_traffic = load_image("traffic_car.webp", (52, 90))
        self.img_coin = load_image("coin.png", (18, 18))
        self.img_obstacle = load_image("barrier.png", (50, 50))
        self.img_powerup = load_image("power_up.png", (30, 30))

        self.traffic = []
        self.obstacles = []
        self.coins = []
        self.powerups = []

        self.max_traffic = 2
        self.max_obstacles = 1
        self.max_coins = 2
        self.max_powerups = 1

        self.distance = 0.0
        self.coin_count = 0
        self.score_bonus = 0

        self.base_speed = 1.2 * self.diff_mul
        self.road_off = 0

        self.nitro_until = 0

        self.t_coin = 0
        self.t_traffic = 0
        self.t_obstacle = 0
        self.t_power = 0

        self.game_over = False

    def total_score(self):
        return int(self.distance * 0.6 + self.coin_count * 25 + self.score_bonus)

    def safe_lane(self):
        choices = list(range(LANES))
        if self.player_lane in choices and random.random() < 0.7:
            choices.remove(self.player_lane)
        return random.choice(choices) if choices else random.randint(0, LANES - 1)

    def spawn(self, dt, now):
        scale = 1.0 + min(1.2, self.distance / 2500.0)

        self.t_coin += dt
        if self.t_coin >= 0.9 / scale and len(self.coins) < self.max_coins:
            self.t_coin = 0
            lane = random.randint(0, LANES - 1)
            r = pygame.Rect(0, -20, 18, 18)
            r.center = (lane_center(lane), -10)
            self.coins.append(r)

        self.t_traffic += dt
        if self.t_traffic >= 1.0 / scale and len(self.traffic) < self.max_traffic:
            self.t_traffic = 0
            lane = self.safe_lane()
            r = pygame.Rect(0, -110, 52, 90)
            r.center = (lane_center(lane), -50)
            self.traffic.append({"rect": r, "speed": random.uniform(0.85, 1.25)})

        self.t_obstacle += dt
        if self.t_obstacle >= 1.4 / scale and len(self.obstacles) < self.max_obstacles:
            self.t_obstacle = 0
            lane = self.safe_lane()
            r = pygame.Rect(0, -60, 60, 26)
            r.center = (lane_center(lane), -20)
            self.obstacles.append(r)

        self.t_power += dt
        if self.t_power >= 6.0 / scale and len(self.powerups) < self.max_powerups:
            self.t_power = 0
            lane = self.safe_lane()
            r = pygame.Rect(0, -28, 24, 24)
            r.center = (lane_center(lane), -10)
            self.powerups.append({"rect": r, "kind": "mystery", "expire": now + 8000})

    def update(self, dt, keys, now):
        if self.game_over:
            return

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.x -= int(280 * dt)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.x += int(280 * dt)

        self.player.x = max(ROAD_X + 6, min(ROAD_X + ROAD_W - self.player.width - 6, self.player.x))
        self.player_lane = max(0, min(LANES - 1, int((self.player.centerx - ROAD_X) / LANE_W)))

        speed = self.base_speed * (1.0 + min(1.3, self.distance / 3000.0))
        if now < self.nitro_until:
            speed *= 1.65

        self.distance += speed * dt * 40
        scroll = int(speed * dt * 250)
        self.road_off = (self.road_off + scroll) % 60

        self.spawn(dt, now)

        for t in self.traffic:
            t["rect"].y += int(scroll * t["speed"])
        for o in self.obstacles:
            o.y += scroll
        for c in self.coins:
            c.y += scroll
        for p in self.powerups:
            p["rect"].y += scroll

        self.traffic = [t for t in self.traffic if t["rect"].top < H + 120]
        self.obstacles = [o for o in self.obstacles if o.top < H + 50]
        self.coins = [c for c in self.coins if c.top < H + 40]
        self.powerups = [p for p in self.powerups if p["rect"].top < H + 40 and now <= p["expire"]]

        for c in self.coins[:]:
            if self.player.colliderect(c):
                self.coins.remove(c)
                self.coin_count += 1

        for p in self.powerups[:]:
            if self.player.colliderect(p["rect"]):
                self.powerups.remove(p)
                self.nitro_until = now + 4000
                self.score_bonus += 50

        collided = any(self.player.colliderect(t["rect"]) for t in self.traffic) or any(self.player.colliderect(o) for o in self.obstacles)
        if collided:
            self.game_over = True

    def draw(self, screen, font):
        screen.fill((210, 215, 225))
        pygame.draw.rect(screen, (60, 60, 60), (ROAD_X, 0, ROAD_W, H))
        for i in range(1, LANES):
            x = ROAD_X + i * LANE_W
            y = -60 + self.road_off
            while y < H:
                pygame.draw.line(screen, (235, 235, 235), (x, y), (x, y + 36), 2)
                y += 60

        for c in self.coins:
            if self.img_coin:
                screen.blit(self.img_coin, self.img_coin.get_rect(center=c.center))
            else:
                pygame.draw.circle(screen, (255, 220, 30), c.center, 9)

        for o in self.obstacles:
            if self.img_obstacle:
                screen.blit(self.img_obstacle, self.img_obstacle.get_rect(center=o.center))
            else:
                pygame.draw.rect(screen, (230, 110, 30), o, border_radius=4)

        for p in self.powerups:
            if self.img_powerup:
                screen.blit(self.img_powerup, self.img_powerup.get_rect(center=p["rect"].center))
            else:
                pygame.draw.rect(screen, (170, 70, 230), p["rect"], border_radius=4)

        for t in self.traffic:
            if self.img_traffic:
                screen.blit(self.img_traffic, self.img_traffic.get_rect(center=t["rect"].center))
            else:
                pygame.draw.rect(screen, (220, 80, 80), t["rect"], border_radius=6)

        if self.img_player:
            screen.blit(self.img_player, self.player)
        else:
            pygame.draw.rect(screen, (52, 104, 225), self.player, border_radius=6)

        hud = [
            f"User: {self.username}",
            f"Score: {self.total_score()}",
            f"Distance: {int(self.distance)}",
            f"Coins: {self.coin_count}",
            f"Difficulty: {self.diff}",
        ]
        y = 12
        for line in hud:
            screen.blit(font.render(line, True, (20, 20, 20)), (12, y))
            y += 24


def menu_screen(screen, fonts):
    buttons = [
        Button(W // 2 - 140, 210, 280, 50, "Play", "play"),
        Button(W // 2 - 140, 275, 280, 50, "Leaderboard", "leader"),
        Button(W // 2 - 140, 340, 280, 50, "Quit", "quit"),
    ]
    while True:
        screen.fill((240, 243, 252))
        screen.blit(fonts["title"].render("TSIS3 Mini Racer", True, (20, 20, 20)), (W // 2 - 180, 95))
        for b in buttons:
            b.draw(screen, fonts["button"])
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit"
            for b in buttons:
                if b.click(e):
                    return b.action


def username_screen(screen, fonts):
    name = ""
    start_btn = Button(W // 2 - 140, 370, 280, 50, "Start", "start")
    back_btn = Button(W // 2 - 140, 435, 280, 50, "Back", "back")
    while True:
        screen.fill((240, 243, 252))
        screen.blit(fonts["title"].render("Username", True, (20, 20, 20)), (W // 2 - 90, 120))
        box = pygame.Rect(W // 2 - 170, 230, 340, 50)
        pygame.draw.rect(screen, (255, 255, 255), box, border_radius=8)
        pygame.draw.rect(screen, (20, 20, 20), box, 2, border_radius=8)
        txt = name if name else "Player"
        screen.blit(fonts["button"].render(txt, True, (20, 20, 20)), (box.x + 12, box.y + 11))
        start_btn.draw(screen, fonts["button"])
        back_btn.draw(screen, fonts["button"])
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit", None
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif e.key == pygame.K_RETURN:
                    return "start", name.strip() or "Player"
                elif e.unicode.isprintable() and len(name) < 18:
                    name += e.unicode
            if start_btn.click(e):
                return "start", name.strip() or "Player"
            if back_btn.click(e):
                return "back", None


def leaderboard_screen(screen, fonts):
    rows = load_leaderboard()[:10]
    back = Button(W // 2 - 140, 570, 280, 50, "Back", "back")
    while True:
        screen.fill((240, 243, 252))
        screen.blit(fonts["title"].render("Top 10", True, (20, 20, 20)), (W // 2 - 70, 60))
        y = 130
        for i, r in enumerate(rows, 1):
            line = f"{i:>2}. {r.get('name','Player'):<12} S:{r.get('score',0):<5} D:{r.get('distance',0):<5} C:{r.get('coins',0)}"
            screen.blit(fonts["small"].render(line, True, (35, 35, 35)), (130, y))
            y += 34
        if not rows:
            screen.blit(fonts["small"].render("No scores yet", True, (40, 40, 40)), (130, 130))
        back.draw(screen, fonts["button"])
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit"
            if back.click(e):
                return "back"


def game_over_screen(screen, fonts, stats):
    retry = Button(W // 2 - 140, 430, 280, 50, "Retry", "retry")
    menu = Button(W // 2 - 140, 495, 280, 50, "Main Menu", "menu")
    while True:
        screen.fill((240, 243, 252))
        screen.blit(fonts["title"].render("Game Over", True, (20, 20, 20)), (W // 2 - 120, 90))
        screen.blit(fonts["button"].render(f"Score: {stats['score']}", True, (20, 20, 20)), (W // 2 - 120, 190))
        screen.blit(fonts["button"].render(f"Distance: {stats['distance']}", True, (20, 20, 20)), (W // 2 - 120, 235))
        screen.blit(fonts["button"].render(f"Coins: {stats['coins']}", True, (20, 20, 20)), (W // 2 - 120, 280))
        retry.draw(screen, fonts["button"])
        menu.draw(screen, fonts["button"])
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit"
            if retry.click(e):
                return "retry"
            if menu.click(e):
                return "menu"


def run_game(screen, fonts, username):
    game = Game(username)
    clock = pygame.time.Clock()
    while not game.game_over:
        dt = clock.tick(FPS) / 1000.0
        now = pygame.time.get_ticks()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit", None
        keys = pygame.key.get_pressed()
        game.update(dt, keys, now)
        game.draw(screen, fonts["small"])
        pygame.display.flip()
    stats = {"score": game.total_score(), "distance": int(game.distance), "coins": game.coin_count, "difficulty": game.diff}
    add_score(username, stats["score"], stats["distance"], stats["coins"], stats["difficulty"])
    return "game_over", stats


def main():
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("TSIS3 Mini Racer")
    fonts = {
        "title": pygame.font.SysFont("arial", 46, bold=True),
        "button": pygame.font.SysFont("arial", 30),
        "small": pygame.font.SysFont("consolas", 22),
    }

    username = "Player"

    while True:
        action = menu_screen(screen, fonts)
        if action == "quit":
            break
        if action == "leader":
            if leaderboard_screen(screen, fonts) == "quit":
                break
            continue

        a, u = username_screen(screen, fonts)
        if a == "quit":
            break
        if a == "back":
            continue
        username = u

        while True:
            res, stats = run_game(screen, fonts, username)
            if res == "quit":
                pygame.quit()
                return
            go = game_over_screen(screen, fonts, stats)
            if go == "quit":
                pygame.quit()
                return
            if go == "menu":
                break

    pygame.quit()


if __name__ == "__main__":
    main()
