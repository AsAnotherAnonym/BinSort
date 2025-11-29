import pygame
import random
from config import Config, TrashType
from core.asset_factory import AssetFactory


class Trash(pygame.sprite.Sprite):
    
    def __init__(self, t_type: TrashType, speed: float):
        super().__init__()
        
        self.type = t_type
        
        # Pick random visual variant (0, 1, or 2)
        variant = random.randint(0, 2)
        self.image = AssetFactory.create_trash_sprite(t_type, variant)
        
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, Config.SCREEN_WIDTH - 50)
        self.rect.y = -50
        
        # Use float for smooth movement
        self.float_y = float(self.rect.y)
        self.speed = speed
    
    def update(self):
        """Move trash downward"""
        self.float_y += self.speed
        self.rect.y = int(self.float_y)
    
    def is_offscreen(self):
        """Check if trash has fallen off screen"""
        return self.rect.top > Config.SCREEN_HEIGHT