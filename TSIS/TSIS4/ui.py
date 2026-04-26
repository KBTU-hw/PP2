import pygame
from config import *


class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False
    
    def draw(self, surface, font, hovered=False):
        """Draw button on surface"""
        self.hovered = hovered
        color = BUTTON_HOVER_COLOR if hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, TEXT_COLOR, self.rect, 2, border_radius=8)
        
        text_surf = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def is_clicked(self, event):
        """Check if button was clicked"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False


class TextInput:
    def __init__(self, x, y, width, height, default=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = default
        self.active = True
    
    def handle_event(self, event):
        """Handle keyboard input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isprintable() and len(self.text) < 20:
                self.text += event.unicode
    
    def draw(self, surface, font):
        """Draw text input field"""
        pygame.draw.rect(surface, (50, 50, 50), self.rect, border_radius=8)
        pygame.draw.rect(surface, TEXT_COLOR, self.rect, 2, border_radius=8)
        
        cursor = "|" if (pygame.time.get_ticks() // 350) % 2 == 0 else ""
        text_surf = font.render(self.text + cursor, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(topleft=(self.rect.x + 10, self.rect.y + 8))
        surface.blit(text_surf, text_rect)


def centered_buttons(labels, start_y, gap=16):
    """Create centered buttons"""
    buttons = []
    y = start_y
    for text, action in labels:
        btn = Button(WIDTH // 2 - BUTTON_WIDTH // 2, y, BUTTON_WIDTH, BUTTON_HEIGHT, text, action)
        buttons.append(btn)
        y += BUTTON_HEIGHT + gap
    return buttons


def draw_title(surface, font, text):
    """Draw title text"""
    title_surf = font.render(text, True, (20, 20, 20))
    title_rect = title_surf.get_rect(center=(WIDTH // 2, 50))
    surface.blit(title_surf, title_rect)


def draw_label(surface, font, text, x, y):
    """Draw label text"""
    label_surf = font.render(text, True, (50, 50, 50))
    surface.blit(label_surf, (x, y))


def draw_card(surface, rect):
    """Draw a card background"""
    pygame.draw.rect(surface, MENU_CARD, rect, border_radius=12)
    pygame.draw.rect(surface, (200, 200, 200), rect, 2, border_radius=12)


def main_menu(screen, fonts):
    """Main menu screen"""
    buttons = centered_buttons(
        [
            ("Play", "play"),
            ("Leaderboard", "leaderboard"),
            ("Settings", "settings"),
            ("Quit", "quit"),
        ],
        200,
    )

    while True:
        screen.fill(MENU_BG)
        draw_title(screen, fonts["title"], "Snake Game")
        subtitle = fonts["small"].render("TSIS4", True, (100, 100, 100))
        screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, 120)))

        mouse = pygame.mouse.get_pos()
        for btn in buttons:
            btn.draw(screen, fonts["button"], btn.rect.collidepoint(mouse))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            for btn in buttons:
                if btn.is_clicked(event):
                    return btn.action


def username_screen(screen, fonts):
    """Username entry screen"""
    name = ""
    input_box = TextInput(WIDTH // 2 - 170, 280, 340, 48)
    buttons = centered_buttons([("Start Game", "start"), ("Back", "back")], 400)

    while True:
        screen.fill(MENU_BG)
        draw_title(screen, fonts["title"], "Enter Username")
        draw_card(screen, pygame.Rect(WIDTH // 2 - 240, 200, 480, 280))
        draw_label(screen, fonts["small"], "Type your name before starting", WIDTH // 2 - 160, 230)

        input_box.text = name
        input_box.draw(screen, fonts["button"])

        mouse = pygame.mouse.get_pos()
        for btn in buttons:
            btn.draw(screen, fonts["button"], btn.rect.collidepoint(mouse))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    return "start", name.strip() or "Player"
                elif event.unicode.isprintable() and len(name) < 18:
                    name += event.unicode
            
            for btn in buttons:
                if btn.is_clicked(event):
                    if btn.action == "back":
                        return "back", None
                    return "start", name.strip() or "Player"


def game_over_screen(screen, fonts, score, level, personal_best):
    """Game over screen"""
    buttons = centered_buttons(
        [
            ("Play Again", "retry"),
            ("Main Menu", "menu"),
            ("Quit", "quit"),
        ],
        450,
    )

    while True:
        screen.fill(MENU_BG)
        draw_title(screen, fonts["title"], "GAME OVER")
        draw_card(screen, pygame.Rect(WIDTH // 2 - 240, 200, 480, 220))
        
        y_pos = 220
        for text in [
            f"Final Score: {score}",
            f"Level Reached: {level}",
            f"Personal Best: {personal_best}",
        ]:
            label = fonts["button"].render(text, True, (20, 20, 20))
            screen.blit(label, (WIDTH // 2 - 100, y_pos))
            y_pos += 50

        mouse = pygame.mouse.get_pos()
        for btn in buttons:
            btn.draw(screen, fonts["button"], btn.rect.collidepoint(mouse))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            for btn in buttons:
                if btn.is_clicked(event):
                    return btn.action


def leaderboard_screen(screen, fonts, leaderboard_data):
    """Leaderboard screen"""
    back_btn = Button(WIDTH // 2 - BUTTON_WIDTH // 2, 500, BUTTON_WIDTH, BUTTON_HEIGHT, "Back", "back")

    while True:
        screen.fill(MENU_BG)
        draw_title(screen, fonts["title"], "Leaderboard - Top 10")
        
        # Draw leaderboard
        y_pos = 120
        table_font = pygame.font.Font(None, 20)
        
        # Header
        header = table_font.render("Rank | Username | Score | Level | Date", True, (50, 50, 50))
        screen.blit(header, (WIDTH // 2 - 180, y_pos))
        y_pos += 30
        
        # Entries
        for entry in leaderboard_data:
            rank, username, score, level, played_at = entry
            date_str = played_at.strftime("%m/%d") if played_at else "N/A"
            line = f"{rank:2d}   | {username:10s} | {score:5d} | {level:2d}    | {date_str}"
            text = table_font.render(line, True, (20, 20, 20))
            screen.blit(text, (WIDTH // 2 - 180, y_pos))
            y_pos += 25

        mouse = pygame.mouse.get_pos()
        back_btn.draw(screen, fonts["button"], back_btn.rect.collidepoint(mouse))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if back_btn.is_clicked(event):
                return "back"


def settings_screen(screen, fonts, settings):
    """Settings screen"""
    # Create toggle buttons
    grid_btn = Button(WIDTH // 2 - 100, 200, 200, 50, 
                     f"Grid: {'ON' if settings.get('grid', False) else 'OFF'}", "toggle_grid")
    sound_btn = Button(WIDTH // 2 - 100, 270, 200, 50,
                      f"Sound: {'ON' if settings.get('sound', False) else 'OFF'}", "toggle_sound")
    color_btn = Button(WIDTH // 2 - 100, 340, 200, 50, "Change Snake Color", "change_color")
    back_btn = Button(WIDTH // 2 - 100, 450, 200, 50, "Save & Back", "back")
    
    local_settings = settings.copy()

    while True:
        screen.fill(MENU_BG)
        draw_title(screen, fonts["title"], "Settings")
        
        # Update button text
        grid_text = f"Grid: {'ON' if local_settings.get('grid', False) else 'OFF'}"
        sound_text = f"Sound: {'ON' if local_settings.get('sound', False) else 'OFF'}"
        
        grid_btn.text = grid_text
        sound_btn.text = sound_text

        mouse = pygame.mouse.get_pos()
        for btn in [grid_btn, sound_btn, color_btn, back_btn]:
            btn.draw(screen, fonts["button"], btn.rect.collidepoint(mouse))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", settings
            
            if grid_btn.is_clicked(event):
                local_settings['grid'] = not local_settings.get('grid', False)
            
            if sound_btn.is_clicked(event):
                local_settings['sound'] = not local_settings.get('sound', False)
            
            if color_btn.is_clicked(event):
                # For now, cycle through predefined colors
                colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0)]
                current_color = tuple(local_settings.get('snake_color', (0, 255, 0)))
                try:
                    idx = colors.index(current_color)
                    local_settings['snake_color'] = colors[(idx + 1) % len(colors)]
                except ValueError:
                    local_settings['snake_color'] = colors[0]
            
            if back_btn.is_clicked(event):
                return "back", local_settings
