import config
from core.asset_factory import AssetFactory
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Assets
        self.img_organic = AssetFactory.create_bin_sprite(config.Config.GREEN)
        self.img_inorganic = AssetFactory.create_bin_sprite(config.Config.BLUE)
        
        self.current_type = config.TrashType.ORGANIC
        self.image = self.img_organic
        self.rect = self.image.get_rect()
        
        # Positioning
        self.rect.midbottom = (config.Config.SCREEN_WIDTH // 2, config.Config.SCREEN_HEIGHT - 20)
        
        # Stats
        self.health = 3
        self.last_swap_time = 0
        
    def update(self, keys, dt):
        # Movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= config.Config.PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += config.Config.PLAYER_SPEED
            
        # Mouse control override (optional)
        if pygame.mouse.get_pressed()[0]:
            mouse_x = pygame.mouse.get_pos()[0]
            if abs(mouse_x - self.rect.centerx) > 5:
                move = config.Config.PLAYER_SPEED if mouse_x > self.rect.centerx else -config.Config.PLAYER_SPEED
                self.rect.x += move

        # Screen clamping
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(config.Config.SCREEN_WIDTH, self.rect.right)

    def swap_bin(self):
        now = pygame.time.get_ticks()
        if now - self.last_swap_time > config.Config.SWAP_COOLDOWN:
            self.last_swap_time = now
            if self.current_type == config.TrashType.ORGANIC:
                self.current_type = config.TrashType.INORGANIC
                self.image = self.img_inorganic
            else:
                self.current_type = config.TrashType.ORGANIC
                self.image = self.img_organic