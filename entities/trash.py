import config
from core.asset_factory import AssetFactory
import pygame
import random

class Trash(pygame.sprite.Sprite):
    def __init__(self, t_type: config.TrashType, speed: float):
        super().__init__()
        self.type = t_type
        self.image = AssetFactory.create_trash_sprite(t_type)
        self.rect = self.image.get_rect()
        
        # Random spawn X
        self.rect.x = random.randint(50, config.Config.SCREEN_WIDTH - 50)
        self.rect.y = -50
        
        self.float_y = float(self.rect.y)
        self.speed = speed

    def update(self):
        self.float_y += self.speed
        self.rect.y = int(self.float_y)
        
        # Kill if off screen
        if self.rect.top > config.Config.SCREEN_HEIGHT:
            self.kill()