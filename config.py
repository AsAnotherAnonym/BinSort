from enum import Enum, auto

class Config:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FPS = 60
    TITLE = "BinSort"
    
    FONT_FILE = "PressStart2P.ttf"
    
    # Color palette
    WHITE = (255, 255, 255)
    BLACK = (20, 20, 20)
    GREEN = (100, 230, 50)
    BLUE = (50, 150, 255)
    RED = (255, 80, 80)
    GOLD = (255, 220, 0)
    
    # Gameplay
    PLAYER_SPEED = 14
    SWAP_COOLDOWN = 250
    BASE_TRASH_SPEED = 6
    
    SAVE_FILE = "data/binsort_save.json"


class GameState(Enum):
    TITLE = auto()
    LEVEL_SELECT = auto()
    LEVEL_INTRO = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()


class TrashType(Enum):
    ORGANIC = auto()
    INORGANIC = auto()
    BONUS = auto()