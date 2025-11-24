from enum import Enum, auto

class Config:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FPS = 60
    TITLE = "BinSort (alpha build)"
    
    # Colors (R, G, B)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (50, 200, 50)  # Organic
    BLUE = (50, 50, 200)   # Inorganic
    RED = (200, 50, 50)
    GOLD = (255, 215, 0)
    
    # Gameplay
    PLAYER_SPEED = 15
    SWAP_COOLDOWN = 500  # ms
    BASE_TRASH_SPEED = 3
    
    # File Paths
    SAVE_FILE = "data/binsort_save.json"

# Enums for State Management
class GameState(Enum):
    TITLE = auto()
    LEVEL_SELECT = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()

class TrashType(Enum):
    ORGANIC = auto()
    INORGANIC = auto()
    BONUS = auto()