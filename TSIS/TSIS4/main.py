from pathlib import Path
import pygame

from db import get_personal_best, get_top_scores, save_result, setup_database
from game import SnakeGame

WIDTH, HEIGHT = 600, 400
CELL = 20
pygame.init()

BASE = Path(__file__).resolve().parent


class Button:
    def __init__(self, x, y, w, h, text, action):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.action = action

    def draw(self, screen, font):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(screen, (120, 160, 255) if hover else (230, 234, 244), self.rect, border_radius=8)
        pygame.draw.rect(screen, (20, 20, 20), self.rect, 2, border_radius=8)
        txt = font.render(self.text, True, (20, 20, 20))
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    def click(self, e):
        return e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and self.rect.collidepoint(e.pos)


def main_menu(screen, fonts):
    btns = [
        Button(WIDTH // 2 - 140, 200, 280, 50, "Play", "play"),
        Button(WIDTH // 2 - 140, 265, 280, 50, "Leaderboard", "leader"),
        Button(WIDTH // 2 - 140, 330, 280, 50, "Quit", "quit"),
    ]
    while True:
        screen.fill((240, 243, 252))
        screen.blit(fonts["title"].render("TSIS4 Mini Snake", True, (20, 20, 20)), (WIDTH // 2 - 170, 90))
        for b in btns:
            b.draw(screen, fonts["button"])
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit"
            for b in btns:
                if b.click(e):
                    return b.action


def username_screen(screen, fonts):
    text = ""
    start = Button(WIDTH // 2 - 140, 360, 280, 50, "Start", "start")
    back = Button(WIDTH // 2 - 140, 425, 280, 50, "Back", "back")
    while True:
        screen.fill((240, 243, 252))
        screen.blit(fonts["title"].render("Username", True, (20, 20, 20)), (WIDTH // 2 - 90, 120))
        box = pygame.Rect(WIDTH // 2 - 170, 230, 340, 50)
        pygame.draw.rect(screen, (255, 255, 255), box, border_radius=8)
        pygame.draw.rect(screen, (20, 20, 20), box, 2, border_radius=8)
        show = text if text else "Player"
        screen.blit(fonts["button"].render(show, True, (20, 20, 20)), (box.x + 12, box.y + 10))
        start.draw(screen, fonts["button"])
        back.draw(screen, fonts["button"])
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit", None
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif e.key == pygame.K_RETURN:
                    return "start", text.strip() or "Player"
                elif e.unicode.isprintable() and len(text) < 18:
                    text += e.unicode
            if start.click(e):
                return "start", text.strip() or "Player"
            if back.click(e):
                return "back", None


def leaderboard_screen(screen, fonts):
    back = Button(WIDTH // 2 - 140, 540, 280, 50, "Back", "back")
    rows = get_top_scores(10)
    while True:
        screen.fill((240, 243, 252))
        screen.blit(fonts["title"].render("Top 10 Leaderboard", True, (20, 20, 20)), (WIDTH // 2 - 220, 70))
        y = 130
        for i, row in enumerate(rows, 1):
            user, score, level, dt = row
            date_str = dt.strftime("%Y-%m-%d") if dt else "-"
            line = f"{i:>2}. {user:<12} score:{score:<5} level:{level:<3} {date_str}"
            screen.blit(fonts["small"].render(line, True, (40, 40, 40)), (80, y))
            y += 34
        if not rows:
            screen.blit(fonts["small"].render("No records yet", True, (40, 40, 40)), (80, 130))
        back.draw(screen, fonts["button"])
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit"
            if back.click(e):
                return "back"


def game_over_screen(screen, fonts, username, score, level):
    best = get_personal_best(username)
    retry = Button(WIDTH // 2 - 140, 430, 280, 50, "Retry", "retry")
    menu = Button(WIDTH // 2 - 140, 495, 280, 50, "Main Menu", "menu")
    while True:
        screen.fill((240, 243, 252))
        screen.blit(fonts["title"].render("Game Over", True, (20, 20, 20)), (WIDTH // 2 - 120, 95))
        screen.blit(fonts["button"].render(f"Score: {score}", True, (20, 20, 20)), (WIDTH // 2 - 130, 200))
        screen.blit(fonts["button"].render(f"Level: {level}", True, (20, 20, 20)), (WIDTH // 2 - 130, 245))
        screen.blit(fonts["button"].render(f"Personal Best: {best}", True, (20, 20, 20)), (WIDTH // 2 - 130, 290))
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
    game = SnakeGame(username)
    clock = pygame.time.Clock()

    while not game.game_over:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit", 0, 0
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    game.set_direction((-1, 0))
                elif e.key == pygame.K_RIGHT:
                    game.set_direction((1, 0))
                elif e.key == pygame.K_UP:
                    game.set_direction((0, -1))
                elif e.key == pygame.K_DOWN:
                    game.set_direction((0, 1))
                elif e.key == pygame.K_ESCAPE:
                    return "menu", game.score, game.level

        game.update()
        game.draw(screen, fonts["small"])
        pygame.display.flip()
        clock.tick(60)

    save_result(username, game.score, game.level)
    return "over", game.score, game.level


def main():
    setup_database()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSIS4 Mini Snake")
    fonts = {
        "title": pygame.font.SysFont("arial", 46, bold=True),
        "button": pygame.font.SysFont("arial", 30),
        "small": pygame.font.SysFont("consolas", 22),
    }

    while True:
        action = main_menu(screen, fonts)
        if action == "quit":
            break
        if action == "leader":
            if leaderboard_screen(screen, fonts) == "quit":
                break
            continue

        a, username = username_screen(screen, fonts)
        if a == "quit":
            break
        if a == "back":
            continue

        while True:
            status, score, level = run_game(screen, fonts, username)
            if status == "quit":
                pygame.quit()
                return
            if status == "menu":
                break
            go = game_over_screen(screen, fonts, username, score, level)
            if go == "quit":
                pygame.quit()
                return
            if go == "menu":
                break

    pygame.quit()


if __name__ == "__main__":
    main()
