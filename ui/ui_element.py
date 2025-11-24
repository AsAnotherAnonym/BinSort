import config
from core.asset_factory import AssetFactory
import pygame
import cairo

class UIElement:
    def __init__(self, x, y, w, h, text, action_code):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.action_code = action_code # Store ID or Function
        self.hovered = False
        
        # Generate Button Surfaces (Normal vs Hover)
        self.surf_normal = self._gen_surf((60, 60, 60))
        self.surf_hover = self._gen_surf((100, 100, 100))
        
    def _gen_surf(self, color):
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.rect.width, self.rect.height)
        ctx = cairo.Context(s)
        
        # Background
        r, g, b = [c/255.0 for c in color]
        ctx.set_source_rgba(r, g, b, 1)
        ctx.rectangle(0, 0, self.rect.width, self.rect.height)
        ctx.fill()
        
        # Border
        ctx.set_source_rgba(1, 1, 1, 1)
        ctx.set_line_width(2)
        ctx.rectangle(0, 0, self.rect.width, self.rect.height)
        ctx.stroke()
        
        return AssetFactory.cairo_to_pygame(s, 1)

    def draw(self, screen, font):
        surf = self.surf_hover if self.hovered else self.surf_normal
        screen.blit(surf, self.rect)
        
        # Text Overlay
        txt = font.render(self.text, True, config.Config.WHITE)
        txt_rect = txt.get_rect(center=self.rect.center)
        screen.blit(txt, txt_rect)
        
    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
        return self.hovered