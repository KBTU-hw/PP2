# Game Configuration
WIDTH = 800
HEIGHT = 600
GRID_SIZE = 20
FPS = 10

# Colors
BG_COLOR = (26, 26, 26)
SNAKE_COLOR = (0, 255, 0)
SNAKE_COLOR_DEFAULT = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)
POISON_COLOR = (139, 0, 0)  # Dark red
OBSTACLE_COLOR = (100, 100, 100)
POWER_UP_COLOR = (255, 255, 0)
SHIELD_COLOR = (0, 255, 255)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (50, 50, 50)
BUTTON_HOVER_COLOR = (80, 80, 80)
MENU_BG = (240, 243, 252)
MENU_CARD = (252, 253, 255)

# Food Types
FOOD_NORMAL = "normal"
FOOD_WEIGHTED = "weighted"
FOOD_DISAPPEARING = "disappearing"
FOOD_POISON = "poison"

# Power-up Types
POWERUP_SPEED_BOOST = "speed_boost"
POWERUP_SLOW_MOTION = "slow_motion"
POWERUP_SHIELD = "shield"

# Timing (in milliseconds)
FOOD_DISAPPEAR_TIME = 10000  # 10 seconds
POWERUP_SPAWN_TIME = 8000    # 8 seconds
POWERUP_EFFECT_DURATION = 5000  # 5 seconds
SHIELD_DURATION = float('inf')  # Until triggered

# Speed settings (grid units per frame)
INITIAL_SPEED = 1
MAX_SPEED = 10

# Level settings
LEVEL_FOOD_THRESHOLD = 5  # Food items needed to advance level
OBSTACLE_START_LEVEL = 3
MAX_OBSTACLES_PER_LEVEL = 5

# Database
DB_NAME = "snake_game"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"
DB_PORT = 5432

# Food scores
FOOD_NORMAL_POINTS = 10
FOOD_WEIGHTED_POINTS = 25
FOOD_POISON_POINTS = -50

# UI
BUTTON_WIDTH = 280
BUTTON_HEIGHT = 52
BUTTON_GAP = 16
