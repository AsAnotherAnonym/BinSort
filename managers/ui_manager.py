import config
from core.asset_factory import AssetFactory
import pygame

class UIManager:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 20, bold=True)
        self.title_font = pygame.font.SysFont("Arial", 60, bold=True)
        
        # Generate UI panels via Cairo
        self.panel_bg = AssetFactory.create_ui_panel(300, 200, (50, 50, 50))
        
    def draw_text(self, surface, text, size, x, y, color=config.Config.WHITE, center=False):
        # Simple wrapper for PyGame font (Dynamic text is better handled by PyGame than cairo per frame)
        f = pygame.font.SysFont("Arial", size, bold=True)
        render = f.render(text, True, color)
        rect = render.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        surface.blit(render, rect)
        
    def draw_hud(self, surface, player, stats, level):
        # Health
        self.draw_text(surface, f"HP: {player.health}", 30, 20, 20, config.Config.RED)
        
        # Stats
        ratio = 0
        if stats['total'] > 0:
            ratio = int((stats['caught'] / stats['total']) * 100)
            
        self.draw_text(surface, f"Level: {level}", 20, 20, 60)
        self.draw_text(surface, f"Caught: {stats['caught']}", 20, 20, 85)
        self.draw_text(surface, f"Ratio: {ratio}%", 20, 20, 110)
        
        # Bin Indicator
        ind_text = "ORGANIC" if player.current_type == config.TrashType.ORGANIC else "INORGANIC"
        ind_color = config.Config.GREEN if player.current_type == config.TrashType.ORGANIC else config.Config.BLUE
        self.draw_text(surface, f"BIN: {ind_text}", 30, config.Config.SCREEN_WIDTH - 250, 20, ind_color)