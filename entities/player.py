import pygame
from config import Config, TrashType
from core.asset_factory import AssetFactory


class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        
        # Load both bin sprites
        self.img_organic = AssetFactory.create_bin_sprite(Config.GREEN)
        self.img_inorganic = AssetFactory.create_bin_sprite(Config.BLUE)
        
        # Set initial state
        self.current_type = TrashType.ORGANIC
        self.image = self.img_organic
        self.rect = self.image.get_rect()
        self.rect.midbottom = (Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT - 20)
        
        # Stats
        self.health = 3
        self.last_swap_time = 0
    
    def update(self, keys, dt):
        """Update player position based on input"""
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= Config.PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += Config.PLAYER_SPEED
        
        # Keep player on screen
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(Config.SCREEN_WIDTH, self.rect.right)
    
    def swap_bin(self):
        now = pygame.time.get_ticks()
        if now - self.last_swap_time > Config.SWAP_COOLDOWN:
            self.last_swap_time = now
            
            if self.current_type == TrashType.ORGANIC:
                self.current_type = TrashType.INORGANIC
                self.image = self.img_inorganic
            else:
                self.current_type = TrashType.ORGANIC
                self.image = self.img_organic
            
            return True
        return False
    
    def take_damage(self):
        self.health -= 1
    
    def heal(self):
        self.health += 1
    
    def is_alive(self):
        return self.health > 0
    
    def reset(self):
        self.health = 3
        self.current_type = TrashType.ORGANIC
        self.image = self.img_organic
        self.rect.midbottom = (Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT - 20)