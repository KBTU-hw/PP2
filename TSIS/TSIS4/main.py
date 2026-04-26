import pygame
import json
import os
from config import *
from db import db
from game import GameState
from ui import main_menu, username_screen, game_over_screen, leaderboard_screen, settings_screen


# Initialize Pygame
pygame.init()
pygame.display.set_caption("Snake Game - TSIS4")

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Create fonts
fonts = {
    "title": pygame.font.Font(None, 56),
    "button": pygame.font.Font(None, 32),
    "small": pygame.font.Font(None, 24),
}

# Settings file path
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")


def load_settings():
    """Load settings from JSON file"""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
        except:
            return get_default_settings()
    return get_default_settings()


def get_default_settings():
    """Get default settings"""
    return {
        "grid": False,
        "sound": False,
        "snake_color": SNAKE_COLOR_DEFAULT,
    }


def save_settings(settings):
    """Save settings to JSON file"""
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=2)
    except Exception as e:
        print(f"Error saving settings: {e}")


def game_loop(username, settings):
    """Main game loop"""
    snake_color = tuple(settings.get("snake_color", SNAKE_COLOR_DEFAULT))
    game = GameState(username, snake_color)
    
    # Get personal best
    personal_best = db.get_player_best_score(username)
    
    show_grid = settings.get("grid", False)

    while not game.game_over:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    game.snake.change_direction((1, 0))
                elif event.key == pygame.K_UP:
                    game.snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    game.snake.change_direction((0, 1))
                elif event.key == pygame.K_ESCAPE:
                    return "menu"
                elif event.key == pygame.K_g:
                    show_grid = not show_grid
        
        # Update game
        game.update()
        
        # Draw game
        game.draw(screen, show_grid)
        
        # Draw personal best
        font = pygame.font.Font(None, 24)
        best_text = font.render(f"Personal Best: {personal_best}", True, (255, 255, 255))
        screen.blit(best_text, (WIDTH - 220, 10))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    # Save game session
    player_id = db.get_or_create_player(username)
    if player_id:
        db.save_game_session(player_id, game.score, game.level)
    
    return "game_over", game


def main():
    """Main application loop"""
    # Initialize database
    db.connect()
    db.create_tables()
    
    # Load settings
    settings = load_settings()
    
    screen_state = "menu"

    while True:
        if screen_state == "menu":
            screen_state = main_menu(screen, fonts)
        
        elif screen_state == "play":
            screen_state = username_screen(screen, fonts)
        
        elif screen_state == "start":
            username = screen_state[1] if isinstance(screen_state, tuple) else "Player"
            screen_state = username_screen(screen, fonts)
        
        elif screen_state == "quit":
            break
        
        elif screen_state == "leaderboard":
            # Fetch leaderboard from database
            leaderboard_data = db.get_leaderboard(10)
            result = leaderboard_screen(screen, fonts, leaderboard_data)
            screen_state = "menu" if result == "back" else "quit"
        
        elif screen_state == "settings":
            result, new_settings = settings_screen(screen, fonts, settings)
            if result == "back":
                settings = new_settings
                save_settings(settings)
            screen_state = "menu" if result != "quit" else "quit"
        
        elif isinstance(screen_state, tuple) and screen_state[0] == "start":
            # Game loop
            username = screen_state[1]
            result = game_loop(username, settings)
            
            if isinstance(result, tuple) and result[0] == "game_over":
                game = result[1]
                personal_best = max(db.get_player_best_score(username), game.score)
                screen_state = game_over_screen(screen, fonts, game.score, game.level, personal_best)
            else:
                screen_state = result
        
        elif isinstance(screen_state, str) and screen_state == "game_over":
            # This shouldn't happen, but handle it
            screen_state = "menu"
        
        else:
            # Default handling for tuple returns from username_screen
            if isinstance(screen_state, tuple):
                action, username = screen_state
                if action == "start":
                    result = game_loop(username, settings)
                    if isinstance(result, tuple) and result[0] == "game_over":
                        game = result[1]
                        personal_best = max(db.get_player_best_score(username), game.score)
                        screen_state = game_over_screen(screen, fonts, game.score, game.level, personal_best)
                    else:
                        screen_state = result
                elif action == "back":
                    screen_state = "menu"
                elif action == "quit":
                    break
            else:
                screen_state = "menu"
    
    # Cleanup
    db.disconnect()
    pygame.quit()


if __name__ == "__main__":
    main()
