from core.asset_factory import AssetFactory
import pygame

class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = AssetFactory.create_cursor()
        self.rect = self.image.get_rect()
        
    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.topleft = pos
        
    def draw(self, screen):
        # Draw on top of everything
        if pygame.mouse.get_focused():
            screen.blit(self.image, self.rect)