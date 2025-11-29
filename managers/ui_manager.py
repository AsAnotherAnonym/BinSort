import pygame
import cairo
from config import Config, TrashType
from core.asset_factory import AssetFactory


class UIElement:
    
    def __init__(self, x, y, w, h, text, action_code, color_theme=Config.BLUE):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.action_code = action_code
        self.hovered = False
        self.color_theme = color_theme
        
        # Pre-generate surfaces for performance
        self.surf_normal = self._gen_surf(hover=False)
        self.surf_hover = self._gen_surf(hover=True)
    
    def _gen_surf(self, hover=False):
        """Generate button surface with 3D effect"""
        depth = 6
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.rect.width, self.rect.height + depth)
        ctx = cairo.Context(s)
        
        w, h = self.rect.width, self.rect.height
        r, g, b = [c/255.0 for c in self.color_theme]
        
        # Adjust brightness for hover/shadow
        shadow_r, shadow_g, shadow_b = r * 0.6, g * 0.6, b * 0.6
        if hover:
            r, g, b = min(1, r*1.2), min(1, g*1.2), min(1, b*1.2)
        
        # Black outline
        ctx.set_source_rgba(0, 0, 0, 1)
        self._rounded_rect(ctx, 0, depth, w, h, 8)
        self._rounded_rect(ctx, 0, 0, w, h, 8)
        ctx.fill()
        
        # Shadow (darker bottom)
        ctx.set_source_rgba(shadow_r, shadow_g, shadow_b, 1)
        self._rounded_rect(ctx, 2, 2 + depth - 2, w-4, h-4, 6)
        ctx.fill()
        
        # Main face
        ctx.set_source_rgba(r, g, b, 1)
        self._rounded_rect(ctx, 2, 2, w-4, h-6, 6)
        ctx.fill()
        
        return AssetFactory.cairo_to_pygame(s, 1)
    
    def _rounded_rect(self, ctx, x, y, w, h, r):
        """Draw rounded rectangle path"""
        ctx.move_to(x+r, y)
        ctx.line_to(x+w-r, y)
        ctx.curve_to(x+w, y, x+w, y, x+w, y+r)
        ctx.line_to(x+w, y+h-r)
        ctx.curve_to(x+w, y+h, x+w, y+h, x+w-r, y+h)
        ctx.line_to(x+r, y+h)
        ctx.curve_to(x, y+h, x, y+h, x, y+h-r)
        ctx.line_to(x, y+r)
        ctx.curve_to(x, y, x, y, x+r, y)
        ctx.close_path()
    
    def draw(self, screen, ui_manager):
        """Render button to screen"""
        surf = self.surf_hover if self.hovered else self.surf_normal
        screen.blit(surf, self.rect)
        
        # Draw text centered on button face
        txt_center_x = self.rect.centerx
        txt_center_y = self.rect.centery - 2
        ui_manager.draw_text(screen, self.text, 20, txt_center_x, txt_center_y, 
                            color=Config.BLACK, center=True, outline=False)
    
    def check_hover(self, mouse_pos):
        """Check if mouse is over button"""
        self.hovered = self.rect.collidepoint(mouse_pos)
        return self.hovered


class Cursor(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.image = AssetFactory.create_cursor()
        self.rect = self.image.get_rect()
    
    def update(self):
        """Update cursor position"""
        self.rect.topleft = pygame.mouse.get_pos()
    
    def draw(self, screen):
        """Draw cursor if mouse is focused"""
        if pygame.mouse.get_focused():
            screen.blit(self.image, self.rect)


class UIManager:
    
    def __init__(self):
        pygame.font.init()
        self.fonts = {}
        self.heart_icon = AssetFactory.create_heart_sprite()
    
    def get_font(self, size):
        """Get or create font of specified size"""
        if size not in self.fonts:
            try:
                self.fonts[size] = pygame.font.Font(Config.FONT_FILE, size)
            except (FileNotFoundError, OSError):
                if size == 20:
                    print(f"Warning: {Config.FONT_FILE} not found. Using Arial.")
                self.fonts[size] = pygame.font.SysFont("Arial", size, bold=True)
        return self.fonts[size]
    
    def draw_text(self, surface, text, size, x, y, color=Config.WHITE, center=False, outline=True):
        """Draw text with optional outline"""
        f = self.get_font(size)
        
        def render_at(txt, col, pos_x, pos_y):
            surf = f.render(txt, False, col)
            rect = surf.get_rect()
            if center:
                rect.center = (pos_x, pos_y)
            else:
                rect.topleft = (pos_x, pos_y)
            surface.blit(surf, rect)
        
        # Draw outline
        if outline:
            offsets = [(-2, -2), (-2, 2), (2, -2), (2, 2), 
                      (-2, 0), (2, 0), (0, -2), (0, 2)]
            for ox, oy in offsets:
                render_at(text, Config.BLACK, x + ox, y + oy)
        
        # Draw main text
        render_at(text, color, x, y)
    
    def draw_hud(self, surface, player, stats, level):
        """Draw heads-up display during gameplay"""
        # Heart icon + HP
        surface.blit(self.heart_icon, (20, 20))
        self.draw_text(surface, f"x {player.health}", 25, 60, 22, Config.RED)
        
        # Level and score
        self.draw_text(surface, f"Level: {level}", 15, 20, 60)
        self.draw_text(surface, f"Score: {stats['caught']}/{stats['total']}", 15, 20, 85)
        
        # Bin type indicator
        ind_col = Config.GREEN if player.current_type == TrashType.ORGANIC else Config.BLUE
        self.draw_text(surface, f"BIN: {player.current_type.name}", 23, 
                      Config.SCREEN_WIDTH - 350, 60, ind_col)