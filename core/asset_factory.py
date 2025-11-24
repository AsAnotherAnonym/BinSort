import config
import pygame
import cairo
import math
import random

class AssetFactory:
    """
    Generates visuals using PyCairo and converts them to PyGame surfaces
    Renders small 'pixel' grids then scales up for 8-bit look

    Akan melakukan generate menggunakan PyCairo dan dikonversi ke surface2 pada PyGame
    Me-render grid 'pixel' kecil dan lalu akan di-scale up agar menyerupai style 8-bit
    """
    
    @staticmethod
    def cairo_to_pygame(surface: cairo.ImageSurface, scale: int = 1) -> pygame.Surface:
        """
        Converts a Cairo surface to a PyGame Surface
        
        Mengkonversi surface Cairo ke surface PyGame
        """
        width = surface.get_width()
        height = surface.get_height()
        
        # Get buffer. Cairo is BGRA usually on little-endian
        data = surface.get_data()
        
        # Create PyGame surface
        pyg_surf = pygame.image.frombuffer(data, (width, height), "ARGB")
        
        if scale > 1:
            pyg_surf = pygame.transform.scale(pyg_surf, (width * scale, height * scale))
            
        return pyg_surf

    @staticmethod
    def apply_texture(ctx, width, height, density=0.3):
        """
        Adds random noise pixels on top of existing shapes
        
        Menambahkan efek visual 'noise pixels' diatas objek yang sudah ada
        """
        ctx.set_operator(cairo.OPERATOR_ATOP) # Only draw where content already exists
        for _ in range(int(width * height * density)):
            x = random.randint(0, width)
            y = random.randint(0, height)
            alpha = random.uniform(0.1, 0.3)
            ctx.set_source_rgba(0, 0, 0, alpha)
            ctx.rectangle(x, y, 1, 1) # 1px noise
            ctx.fill()
        ctx.set_operator(cairo.OPERATOR_OVER) # Reset

    @staticmethod
    def create_cursor():
        """
        Draws a retro 8-bit mouse cursor
        
        Menggambar kursor mouse gaya retro 8-bit
        """
        w, h = 16, 16
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        ctx = cairo.Context(surf)
        
        # Draw Arrow
        ctx.set_source_rgba(1, 1, 1, 1) # White
        ctx.move_to(0, 0)
        ctx.line_to(0, 14)
        ctx.line_to(4, 10)
        ctx.line_to(7, 16)
        ctx.line_to(9, 15)
        ctx.line_to(6, 9)
        ctx.line_to(11, 9)
        ctx.close_path()
        ctx.fill_preserve()
        
        # Border
        ctx.set_source_rgba(0, 0, 0, 1) # Black outline
        ctx.set_line_width(1)
        ctx.stroke()
        
        return AssetFactory.cairo_to_pygame(surf, scale=2)

    # ... (Update create_bin_sprite and create_trash_sprite to call apply_texture) ...
    

    @staticmethod
    def create_bin_sprite(color_rgb, width=32, height=32):
        """
        Draws a bin
        
        Menggambar tong sampah 
        """
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        ctx = cairo.Context(surface)
        
        # Normalize colors for Cairo (0.0 - 1.0)
        r, g, b = [c/255.0 for c in color_rgb]
        
        # Draw Bin Body (Trapezoid-ish)
        ctx.set_source_rgba(r, g, b, 1)
        ctx.rectangle(4, 8, 24, 22)
        ctx.fill()
        
        # Draw Lid details
        ctx.set_source_rgba(r*0.8, g*0.8, b*0.8, 1)
        ctx.rectangle(2, 8, 28, 4) # Rim
        ctx.fill()
        
        # Pixel noise for texture
        ctx.set_source_rgba(0, 0, 0, 0.2)
        ctx.rectangle(8, 14, 4, 12) # Stripes
        ctx.rectangle(20, 14, 4, 12)
        ctx.fill()

        return AssetFactory.cairo_to_pygame(surface, scale=3) # Scale up for retro look

    @staticmethod
    def create_trash_sprite(t_type: config.TrashType):
        w, h = 16, 16
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        ctx = cairo.Context(surface)
        
        # ... (Draw shapes as before) ...
        if t_type == config.TrashType.ORGANIC:
            ctx.set_source_rgba(0.3, 0.8, 0.2, 1)
            ctx.arc(8, 8, 6, 0, 2*math.pi)
            ctx.fill()
        elif t_type == config.TrashType.INORGANIC:
            ctx.set_source_rgba(0.2, 0.3, 0.9, 1)
            ctx.rectangle(4, 4, 8, 10)
            ctx.fill()
        elif t_type == config.TrashType.BONUS:
            ctx.set_source_rgba(1.0, 0.2, 0.2, 1)
            ctx.arc(8, 8, 6, 0, 2*math.pi) # Simplified heart for brevity
            ctx.fill()

        # APPLY TEXTURE
        AssetFactory.apply_texture(ctx, w, h, density=0.2)

        return AssetFactory.cairo_to_pygame(surface, scale=3)

    @staticmethod
    def create_ui_panel(width, height, color):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        ctx = cairo.Context(surface)
        
        # Translucent panel
        r, g, b = [c/255.0 for c in color]
        ctx.set_source_rgba(r, g, b, 0.8)
        
        # Rounded rect
        radius = 10
        ctx.move_to(radius, 0)
        ctx.line_to(width - radius, 0)
        ctx.curve_to(width, 0, width, 0, width, radius)
        ctx.line_to(width, height - radius)
        ctx.curve_to(width, height, width, height, width - radius, height)
        ctx.line_to(radius, height)
        ctx.curve_to(0, height, 0, height, 0, height - radius)
        ctx.line_to(0, radius)
        ctx.curve_to(0, 0, 0, 0, radius, 0)
        ctx.close_path()
        ctx.fill()
        
        # Border
        ctx.set_source_rgba(1, 1, 1, 1)
        ctx.set_line_width(4)
        ctx.stroke()
        
        return AssetFactory.cairo_to_pygame(surface, scale=1)
