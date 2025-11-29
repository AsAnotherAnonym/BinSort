"""
Asset Factory - PyCairo to Pygame bridge
Generates all visual assets procedurally
"""
import pygame
import cairo
import math
import random
from config import Config, TrashType


class AssetFactory:
    """Procedural asset generation using Cairo"""
    
    @staticmethod
    def cairo_to_pygame(surface: cairo.ImageSurface, scale: int = 1) -> pygame.Surface:
        """Convert Cairo surface to Pygame surface"""
        width = surface.get_width()
        height = surface.get_height()
        data = surface.get_data()
        
        try:
            pyg_surf = pygame.image.frombuffer(data, (width, height), "BGRA")
        except ValueError:
            pyg_surf = pygame.image.frombuffer(data, (width, height), "RGBA")
        
        if scale > 1:
            pyg_surf = pygame.transform.scale(pyg_surf, (width * scale, height * scale))
        
        return pyg_surf
    
    @staticmethod
    def apply_texture(ctx, width, height, density=0.3):
        """Apply noise texture overlay"""
        ctx.set_operator(cairo.OPERATOR_ATOP)
        for _ in range(int(width * height * density)):
            x = random.randint(0, width)
            y = random.randint(0, height)
            alpha = random.uniform(0.1, 0.3)
            ctx.set_source_rgba(0, 0, 0, alpha)
            ctx.rectangle(x, y, 1, 1)
            ctx.fill()
        ctx.set_operator(cairo.OPERATOR_OVER)
    
    @staticmethod
    def create_menu_background(screen_width, screen_height):
        """Create forest scene background for menu"""
        scale = 4
        w = screen_width // scale
        h = screen_height // scale
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        ctx = cairo.Context(surface)
        
        # Sky gradient
        pat = cairo.LinearGradient(0, 0, 0, h)
        pat.add_color_stop_rgb(0, 0.2, 0.7, 0.8)
        pat.add_color_stop_rgb(1, 0.6, 0.9, 0.9)
        ctx.rectangle(0, 0, w, h)
        ctx.set_source(pat)
        ctx.fill()
        
        # Clouds
        ctx.set_source_rgb(1.0, 1.0, 1.0)
        for cx, cy in [(20, 30), (100, 15), (160, 40)]:
            ctx.rectangle(cx, cy, 30, 10)
            ctx.rectangle(cx+5, cy-5, 20, 10)
            ctx.fill()
        
        # Mountains
        ctx.set_source_rgb(0.35, 0.35, 0.55)
        ctx.move_to(0, h)
        ctx.line_to(0, h*0.6)
        ctx.line_to(w*0.2, h*0.4)
        ctx.line_to(w*0.4, h*0.6)
        ctx.line_to(w*0.6, h*0.3)
        ctx.line_to(w*0.8, h*0.5)
        ctx.line_to(w, h*0.4)
        ctx.line_to(w, h)
        ctx.close_path()
        ctx.fill()
        
        # Distant forest
        ctx.set_source_rgb(0.1, 0.25, 0.3)
        ctx.move_to(0, h)
        ctx.line_to(0, h*0.65)
        for i in range(0, w, 5):
            peak = random.randint(0, 8)
            ctx.line_to(i, h*0.65 - peak)
            ctx.line_to(i+2, h*0.65)
        ctx.line_to(w, h*0.65)
        ctx.line_to(w, h)
        ctx.close_path()
        ctx.fill()
        
        # Ground
        ctx.set_source_rgb(0.6, 0.8, 0.3)
        ctx.rectangle(0, h*0.65, w, h*0.35)
        ctx.fill()
        
        # Grass highlights
        ctx.set_source_rgba(0.7, 0.9, 0.4, 0.5)
        for _ in range(50):
            rx = random.randint(0, w)
            ry = random.randint(int(h*0.7), h)
            ctx.rectangle(rx, ry, 4, 2)
            ctx.fill()
        
        # Foreground trees
        ctx.set_source_rgb(0.5, 0.3, 0.2)
        ctx.rectangle(5, -10, 30, h+20)
        ctx.fill()
        ctx.set_source_rgba(0.6, 0.4, 0.25, 1)
        ctx.rectangle(25, -10, 5, h+20)
        ctx.fill()
        ctx.set_source_rgb(0.1, 0.4, 0.15)
        ctx.arc(20, 10, 40, 0, 2*math.pi)
        ctx.fill()
        
        ctx.set_source_rgb(0.5, 0.3, 0.2)
        ctx.rectangle(w-35, -10, 30, h+20)
        ctx.fill()
        ctx.set_source_rgba(0.6, 0.4, 0.25, 1)
        ctx.rectangle(w-30, -10, 5, h+20)
        ctx.fill()
        ctx.set_source_rgb(0.1, 0.4, 0.15)
        ctx.arc(w-20, 0, 45, 0, 2*math.pi)
        ctx.fill()
        
        # Bushes
        ctx.set_source_rgb(0.1, 0.3, 0.15)
        for i in range(-20, w+20, 15):
            radius = random.randint(10, 20)
            ctx.arc(i, h, radius, 0, 2*math.pi)
            ctx.fill()
        
        # Dark overlay
        ctx.set_source_rgba(0, 0, 0, 0.4)
        ctx.rectangle(0, 0, w, h)
        ctx.fill()
        
        return AssetFactory.cairo_to_pygame(surface, scale=scale)
    
    @staticmethod
    def create_game_background(screen_width, screen_height):
        """Create gameplay background"""
        scale = 4
        w = screen_width // scale
        h = screen_height // scale
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        ctx = cairo.Context(surface)
        
        def stroke_black():
            ctx.set_source_rgb(0, 0, 0)
            ctx.set_line_width(1)
            ctx.stroke()
        
        # Sky
        pat = cairo.LinearGradient(0, 0, 0, h)
        pat.add_color_stop_rgb(0, 0.2, 0.6, 1.0)
        pat.add_color_stop_rgb(1, 0.6, 0.8, 1.0)
        ctx.rectangle(0, 0, w, h)
        ctx.set_source(pat)
        ctx.fill()
        
        # Clouds
        ctx.set_source_rgb(1.0, 1.0, 1.0)
        for cx, cy in [(20, 30), (100, 15), (160, 40)]:
            ctx.rectangle(cx, cy, 30, 10)
            ctx.rectangle(cx+5, cy-5, 20, 10)
            ctx.fill()
        
        # Trees
        def draw_tree(tx, ty):
            ctx.set_source_rgb(0.55, 0.35, 0.15)
            ctx.rectangle(tx, ty-30, 8, 30)
            ctx.fill_preserve()
            stroke_black()
            ctx.set_source_rgb(0.2, 0.7, 0.2)
            ctx.arc(tx+4, ty-35, 12, 0, 6.28)
            ctx.fill_preserve()
            stroke_black()
        
        draw_tree(30, h-25)
        draw_tree(w-40, h-25)
        
        # Ground
        ctx.set_source_rgb(0.4, 0.8, 0.2)
        ctx.rectangle(0, h-25, w, 8)
        ctx.fill_preserve()
        stroke_black()
        ctx.set_source_rgb(0.5, 0.3, 0.15)
        ctx.rectangle(0, h-17, w, 17)
        ctx.fill_preserve()
        stroke_black()
        
        return AssetFactory.cairo_to_pygame(surface, scale=scale)
    
    @staticmethod
    def create_heart_sprite():
        """Create heart icon for HUD"""
        w, h = 16, 16
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        ctx = cairo.Context(surf)
        
        ctx.set_source_rgba(1, 0, 0, 1)
        ctx.move_to(8, 15)
        ctx.curve_to(8, 15, 0, 10, 0, 5)
        ctx.curve_to(0, 0, 7, 0, 8, 4)
        ctx.curve_to(9, 0, 16, 0, 16, 5)
        ctx.curve_to(16, 10, 8, 15, 8, 15)
        ctx.fill_preserve()
        ctx.set_source_rgba(0, 0, 0, 1)
        ctx.set_line_width(1)
        ctx.stroke()
        
        return AssetFactory.cairo_to_pygame(surf, scale=2)
    
    @staticmethod
    def create_cursor():
        """Create custom cursor sprite"""
        w, h = 16, 16
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        ctx = cairo.Context(surf)
        
        ctx.set_source_rgba(1, 1, 1, 1)
        ctx.move_to(0, 0)
        ctx.line_to(0, 14)
        ctx.line_to(4, 10)
        ctx.line_to(7, 16)
        ctx.line_to(9, 15)
        ctx.line_to(6, 9)
        ctx.line_to(11, 9)
        ctx.close_path()
        ctx.fill_preserve()
        ctx.set_source_rgba(0, 0, 0, 1)
        ctx.set_line_width(1)
        ctx.stroke()
        
        return AssetFactory.cairo_to_pygame(surf, scale=2)
    
    @staticmethod
    def create_bin_sprite(color_rgb):
        """Create trash bin sprite with outline"""
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 32, 32)
        ctx = cairo.Context(surface)
        r, g, b = [c/255.0 for c in color_rgb]
        
        def stroke_black():
            ctx.set_source_rgb(0, 0, 0)
            ctx.set_line_width(1)
            ctx.stroke()
        
        # Body
        ctx.set_source_rgba(r, g, b, 1)
        ctx.rectangle(4, 8, 24, 22)
        ctx.fill_preserve()
        stroke_black()
        
        # Lid
        ctx.set_source_rgba(r*0.8, g*0.8, b*0.8, 1)
        ctx.rectangle(2, 8, 28, 4)
        ctx.fill_preserve()
        stroke_black()
        
        # Details
        ctx.set_source_rgba(0, 0, 0, 0.2)
        ctx.rectangle(10, 15, 2, 10)
        ctx.fill()
        ctx.rectangle(15, 15, 2, 10)
        ctx.fill()
        ctx.rectangle(20, 15, 2, 10)
        ctx.fill()
        
        return AssetFactory.cairo_to_pygame(surface, scale=3)
    
    @staticmethod
    def create_trash_sprite(t_type: TrashType, variant_idx=0):
        """Create trash item sprites with outlines"""
        w, h = 24, 24
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        ctx = cairo.Context(surface)
        
        def stroke():
            ctx.set_source_rgb(0, 0, 0)
            ctx.set_line_width(1)
            ctx.stroke()
        
        if t_type == TrashType.ORGANIC:
            if variant_idx == 0:  # Lemon
                ctx.set_source_rgb(1.0, 0.9, 0.2)
                ctx.move_to(12, 4)
                ctx.curve_to(18, 8, 20, 16, 14, 20)
                ctx.curve_to(10, 20, 4, 16, 6, 8)
                ctx.close_path()
                ctx.fill_preserve()
                stroke()
                
                ctx.set_source_rgb(0.8, 0.7, 0.1)
                ctx.move_to(10, 8)
                ctx.line_to(14, 8)
                ctx.line_to(12, 2)
                ctx.close_path()
                ctx.fill_preserve()
                stroke()
            
            elif variant_idx == 1:  # Crumbled paper
                ctx.set_source_rgb(1.0, 1.0, 1.0)
                ctx.move_to(6, 4)
                ctx.line_to(18, 3)
                ctx.line_to(21, 10)
                ctx.line_to(19, 19)
                ctx.line_to(8, 21)
                ctx.line_to(3, 12)
                ctx.close_path()
                ctx.fill_preserve()
                stroke()
                
                ctx.set_source_rgb(0.8, 0.8, 0.8)
                ctx.set_line_width(2)
                ctx.move_to(10, 6)
                ctx.line_to(9, 18)
                ctx.stroke()
                ctx.move_to(14, 5)
                ctx.line_to(13, 16)
                ctx.stroke()
                ctx.move_to(17, 7)
                ctx.line_to(16, 15)
                ctx.stroke()
            
            else:  # Eaten apple
                ctx.set_source_rgb(0.8, 0.1, 0.1)
                ctx.move_to(6.5, 9)
                ctx.arc(10, 9, 3.5, math.pi, 0)
                ctx.arc(13.5, 9, 3.5, math.pi, 0)
                ctx.fill_preserve()
                stroke()
                
                ctx.set_source_rgb(0.8, 0.1, 0.1)
                ctx.move_to(7.5, 17)
                ctx.arc(10, 17, 3, 0, math.pi)
                ctx.arc(12.5, 17, 3, 0, math.pi)
                ctx.fill_preserve()
                stroke()
                
                ctx.set_source_rgb(1.0, 0.95, 0.8)
                ctx.rectangle(10, 9, 4, 8)
                ctx.fill_preserve()
                ctx.set_source_rgb(0, 0, 0)
                ctx.set_line_width(1)
                ctx.move_to(10, 9)
                ctx.line_to(10, 17)
                ctx.stroke()
                ctx.move_to(14, 9)
                ctx.line_to(14, 17)
                ctx.stroke()
                
                ctx.set_source_rgb(0.4, 0.2, 0.1)
                ctx.rectangle(11.5, 3, 1, 6)
                ctx.fill()
        
        elif t_type == TrashType.INORGANIC:
            if variant_idx == 0:  # Plastic bag
                ctx.set_source_rgba(0.8, 0.8, 1.0, 0.8)
                ctx.rectangle(6, 8, 12, 12)
                ctx.fill_preserve()
                stroke()
                ctx.move_to(6, 8)
                ctx.curve_to(6, 2, 18, 2, 18, 8)
                ctx.stroke()
            
            elif variant_idx == 1:  # Water bottle
                ctx.set_source_rgba(0.2, 0.5, 1.0, 0.8)
                ctx.rectangle(9.5, 2, 5, 2)
                ctx.fill_preserve()
                stroke()
                ctx.set_source_rgb(0.15, 0.15, 0.5)
                ctx.rectangle(9.5, 1, 5, 1)
                ctx.fill_preserve()
                stroke()
                ctx.set_source_rgba(0.2, 0.5, 1.0, 0.8)
                ctx.rectangle(8, 4, 8, 16)
                ctx.fill_preserve()
                stroke()
                ctx.set_source_rgb(0.1, 0.1, 0.8)
                ctx.rectangle(6, 8, 12, 4)
                ctx.fill()
            
            else:  # Can
                ctx.set_source_rgb(0.9, 0.2, 0.2)
                ctx.rectangle(7, 6, 10, 14)
                ctx.fill_preserve()
                stroke()
                ctx.set_source_rgb(0.7, 0.7, 0.7)
                ctx.rectangle(7, 6, 10, 2)
                ctx.fill()
        
        elif t_type == TrashType.BONUS:
            ctx.set_source_rgb(1.0, 0.8, 0.1)
            ctx.move_to(12, 2)
            ctx.line_to(15, 8)
            ctx.line_to(22, 9)
            ctx.line_to(17, 14)
            ctx.line_to(19, 21)
            ctx.line_to(12, 17)
            ctx.line_to(5, 21)
            ctx.line_to(7, 14)
            ctx.line_to(2, 9)
            ctx.line_to(9, 8)
            ctx.close_path()
            ctx.fill_preserve()
            stroke()
        
        AssetFactory.apply_texture(ctx, w, h, 0.15)
        return AssetFactory.cairo_to_pygame(surface, scale=2)