# Snake Game - TSIS4 with Database Integration

A comprehensive Snake game built with Pygame and PostgreSQL featuring persistent leaderboards, advanced gameplay mechanics, and a polished UI.

## Features

### Core Gameplay
- **Wall/Border Collision Detection**: Snake dies when hitting walls
- **Self-Collision Detection**: Game ends if snake hits itself
- **Food System**: Random food placement with multiple food types
  - Normal Food (10 points)
  - Weighted Food (25 points, orange)
  - Disappearing Food (pink, expires after 10 seconds)
  - Poison Food (dark red, shortens snake by 2 segments)
- **Level Progression**: Advance to next level after collecting 5 food items
- **Speed Increase**: Snake moves faster as you level up

### Advanced Features
- **Power-ups** (temporary, 5-second duration):
  - Speed Boost: Increases snake movement speed
  - Slow Motion: Decreases snake movement speed
  - Shield: Ignore next collision (wall, self, or obstacle)
- **Obstacles**: Random wall blocks appear from Level 3 onwards
  - Never spawn in positions that trap the snake
  - Colliding with obstacles causes game over
- **Database Integration**:
  - Save player usernames to PostgreSQL
  - Auto-save score and level after each game
  - Display top 10 all-time scores
  - Track personal best score during gameplay

### User Interface
- **Main Menu**: Play, Leaderboard, Settings, Quit
- **Username Entry**: Enter player name before starting game
- **Game Over Screen**: Shows final score, level, and personal best
- **Leaderboard Screen**: Display top 10 all-time scores with date played
- **Settings Screen**: 
  - Toggle grid overlay (press 'G' in-game to toggle)
  - Toggle sound (placeholder)
  - Change snake color

## Requirements

- Python 3.7+
- Pygame
- psycopg2 (PostgreSQL adapter)
- PostgreSQL database

## Installation

1. **Install Dependencies**:
```bash
pip install pygame psycopg2-binary
```

2. **Set Up Database**:
```bash
# Create the snake_game database
createdb snake_game

# Load the schema
psql snake_game < schema.sql
```

3. **Configure Database Connection** (optional):
   Edit `config.py` if your PostgreSQL credentials differ from defaults:
   - DB_USER: postgres
   - DB_PASSWORD: postgres
   - DB_HOST: localhost
   - DB_PORT: 5432

## Running the Game

```bash
python main.py
```

## Controls

- **Arrow Keys**: Move the snake (Up, Down, Left, Right)
- **Enter**: Confirm actions in menus
- **Escape**: Pause/Return to main menu during gameplay
- **G**: Toggle grid overlay during gameplay
- **Backspace**: Delete characters in text input

## Game Mechanics

### Levels
- Start at Level 1 with base speed
- Each level requires collecting 5 food items
- Speed increases by 1 unit per level (max 10)
- Obstacles appear starting from Level 3

### Scoring
- Normal Food: +10 points
- Weighted Food: +25 points
- Poison Food: -50 points (and shortens snake)
- Power-ups: Improve gameplay, don't directly award points

### Game Over Conditions
1. Hit a wall border
2. Snake hits itself
3. Collide with an obstacle
4. Eat poison food when snake length is 1

## File Structure

```
TSIS4/
├── main.py              # Entry point, screen management
├── game.py              # Core game logic (Snake, Food, PowerUps, Obstacles)
├── ui.py                # UI components (buttons, screens)
├── db.py                # Database operations (PostgreSQL)
├── config.py            # Game configuration constants
├── settings.json        # User preferences (grid, sound, snake color)
└── schema.sql           # PostgreSQL schema definition
```

## Configuration

Edit `config.py` to customize:
- **Game Resolution**: WIDTH, HEIGHT
- **Grid Size**: GRID_SIZE (pixels per cell)
- **Colors**: Snake, food, obstacles, UI
- **Timing**: Food expiration, power-up duration
- **Difficulty**: Initial speed, max speed, obstacles per level
- **Database**: Connection parameters

## Database Schema

### players table
- `id`: Player identifier
- `username`: Unique player name

### game_sessions table
- `id`: Session identifier
- `player_id`: Reference to player
- `score`: Final score
- `level_reached`: Highest level achieved
- `played_at`: Timestamp of game

## Tips

1. **Collect Weighted Food**: Higher point value, orange colored
2. **Use Power-ups**: Shield helps avoid obstacles on higher levels
3. **Watch Food Timer**: Pink disappearing food expires after 10 seconds
4. **Avoid Poison**: Dark red food shortens your snake
5. **Plan Ahead**: On higher levels with obstacles, navigate carefully

## Troubleshooting

**Database Connection Error**:
- Ensure PostgreSQL is running
- Check username and password in `config.py`
- Verify database 'snake_game' exists

**Pygame Import Error**:
- Install pygame: `pip install pygame`
- On Mac, may need: `pip install pygame --pre`

**psycopg2 Error**:
- Install: `pip install psycopg2-binary`

## Future Enhancements

- Sound effects and background music
- Difficulty levels
- Multiplayer support
- More power-up types
- User accounts and authentication
- Statistics tracking (total games, win rate, etc.)

## Credits

Created for TSIS4 - Advanced Programming Assignment
Built with Pygame and PostgreSQL
