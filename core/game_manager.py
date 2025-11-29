import pygame
import sys
from config import Config, GameState, TrashType
from core.asset_factory import AssetFactory
from core.save_manager import SaveManager
from audio.sound_manager import SoundManager
from entities.player import Player
from managers.level_manager import LevelManager
from managers.spawner import Spawner
from managers.ui_manager import UIManager, UIElement, Cursor


class GameManager:
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        pygame.display.set_caption(Config.TITLE)
        self.clock = pygame.time.Clock()
        
        # Hide system cursor
        pygame.mouse.set_visible(False)
        self.cursor = Cursor()
        
        # Initialize managers
        self.sound = SoundManager()
        self.save = SaveManager()
        self.lvl_mgr = LevelManager()
        self.ui = UIManager()
        
        # Generate backgrounds
        print("Generating Background Assets...")
        self.bg_menu = AssetFactory.create_menu_background(Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
        self.bg_game = AssetFactory.create_game_background(Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
        
        # Game state
        self.state = GameState.TITLE
        self.current_level_num = 1
        
        # Initialize UI buttons
        self._init_buttons()
        
        # Reset game session
        self.reset_session()
    
    def _init_buttons(self):
        self.buttons = {
            "title": [
                UIElement(Config.SCREEN_WIDTH//2 - 100, 400, 200, 50, 
                         "PLAY", "goto_level_select", Config.GREEN)
            ],
            "level_select": [],
            "paused": [
                UIElement(Config.SCREEN_WIDTH//2 - 100, 300, 200, 50, 
                         "RESUME", "resume", Config.GREEN),
                UIElement(Config.SCREEN_WIDTH//2 - 100, 370, 200, 50, 
                         "TITLE", "goto_title", Config.BLUE)
            ],
            "game_over": [
                UIElement(Config.SCREEN_WIDTH//2 - 120, 300, 240, 50, 
                         "RESTART", "restart", Config.GOLD),
                UIElement(Config.SCREEN_WIDTH//2 - 120, 370, 240, 50, 
                         "MENU", "goto_level_select", Config.RED)
            ]
        }
        
        # Level select buttons (10 levels in 2 rows)
        for i in range(1, 11):
            x = 150 + ((i-1) % 5) * 100
            y = 250 + ((i-1) // 5) * 80
            self.buttons["level_select"].append(
                UIElement(x, y, 80, 60, f"{i}", f"lvl_{i}", Config.GOLD)
            )
        
        # Back button
        self.buttons["level_select"].append(
            UIElement(20, 20, 120, 40, "<BACK", "goto_title", Config.RED)
        )
    
    def reset_session(self):
        self.player = Player()
        self.trash_group = pygame.sprite.Group()
        self.spawner = None
        self.stats = {"caught": 0, "missed": 0, "total": 0}
    
    def start_level(self, level_num):
        if level_num > self.save.get_unlocked_level():
            self.sound.play("hurt")
            return
        
        self.sound.play("click")
        self.current_level_num = level_num
        self.reset_session()
        self.spawner = Spawner(self.lvl_mgr.get_level_data(level_num))
        
        # Show tutorial for first two levels
        if level_num <= 2:
            self.state = GameState.LEVEL_INTRO
        else:
            self.state = GameState.PLAYING
    
    def handle_click(self, action):
        self.sound.play("click")
        
        if action == "goto_level_select":
            self.state = GameState.LEVEL_SELECT
        elif action == "goto_title":
            self.state = GameState.TITLE
        elif action == "resume":
            self.state = GameState.PLAYING
        elif action == "restart":
            self.start_level(self.current_level_num)
        elif action.startswith("lvl_"):
            level = int(action.split("_")[1])
            self.start_level(level)
    
    def handle_collision(self, trash):
        # Check if trash entered through the lid (top collision)
        lid_threshold = self.player.rect.top + 15
        
        if trash.rect.bottom <= lid_threshold:
            # Entered through lid - check type match
            trash.kill()
            
            if trash.type == TrashType.BONUS:
                self.player.heal()
                self.sound.play("bonus")
            elif trash.type == self.player.current_type:
                self.stats['caught'] += 1
                self.stats['total'] += 1
                self.sound.play("catch")
            else:
                self.player.take_damage()
                self.stats['total'] += 1
                self.sound.play("hurt")
        else:
            # Hit the side - always hurts (unless bonus)
            trash.kill()
            if trash.type != TrashType.BONUS:
                self.player.take_damage()
                self.stats['total'] += 1
                self.sound.play("hurt")
    
    def update_gameplay(self, dt):
        keys = pygame.key.get_pressed()
        self.player.update(keys, dt)
        self.spawner.update(pygame.time.get_ticks(), self.trash_group)
        self.trash_group.update()
        
        # Check collisions
        hits = pygame.sprite.spritecollide(self.player, self.trash_group, False)
        for trash in hits:
            self.handle_collision(trash)
        
        # Check missed trash
        for trash in self.trash_group:
            if trash.is_offscreen():
                trash.kill()
                if trash.type != TrashType.BONUS:
                    self.player.take_damage()
                    self.stats['total'] += 1
                    self.sound.play("hurt")
        
        # Check game over
        if not self.player.is_alive():
            self.state = GameState.GAME_OVER
        
        # Check level complete
        if self.spawner.is_finished() and not self.trash_group and self.player.is_alive():
            self.save.unlock_level(self.current_level_num + 1)
            self.state = GameState.LEVEL_SELECT
    
    def draw_title_screen(self, mouse_pos):
        self.screen.blit(self.bg_menu, (0, 0))
        self.ui.draw_text(self.screen, Config.TITLE, 50, 
                         Config.SCREEN_WIDTH//2, 200, Config.GREEN, True)
        
        for btn in self.buttons["title"]:
            btn.check_hover(mouse_pos)
            btn.draw(self.screen, self.ui)
    
    def draw_level_select(self, mouse_pos):
        self.screen.blit(self.bg_menu, (0, 0))
        self.ui.draw_text(self.screen, "SELECT LEVEL", 30, 
                         Config.SCREEN_WIDTH//2, 150, Config.WHITE, True)
        
        for btn in self.buttons["level_select"]:
            btn.check_hover(mouse_pos)
            btn.draw(self.screen, self.ui)
            
            # Lock unavailable levels
            if btn.action_code.startswith("lvl_"):
                level = int(btn.action_code.split("_")[1])
                if level > self.save.get_unlocked_level():
                    s = pygame.Surface((btn.rect.w, btn.rect.h), pygame.SRCALPHA)
                    s.fill((0, 0, 0, 150))
                    self.screen.blit(s, btn.rect)
    
    def draw_level_intro(self):
        # Dim background
        self.draw_gameplay()
        s = pygame.Surface((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))
        self.screen.blit(s, (0, 0))
        
        self.ui.draw_text(self.screen, f"LEVEL {self.current_level_num}", 40, 
                         Config.SCREEN_WIDTH//2, 150, Config.WHITE, True)
        
        # Instructions
        self.ui.draw_text(self.screen, "[ A ] or [ < ] to Move Left", 23, 
                         Config.SCREEN_WIDTH//2, 250, Config.WHITE, True)
        self.ui.draw_text(self.screen, "[ D ]  or [ > ] to Move Right", 23, 
                         Config.SCREEN_WIDTH//2, 300, Config.WHITE, True)
        
        cd_secs = Config.SWAP_COOLDOWN / 1000.0
        self.ui.draw_text(self.screen, f"[ E ]  Swap Bin (CD: {cd_secs}s)", 23, 
                         Config.SCREEN_WIDTH//2, 350, Config.GOLD, True)
        
        self.ui.draw_text(self.screen, "Press ANY KEY to Start", 20, 
                         Config.SCREEN_WIDTH//2, 500, Config.GREEN, True)
    
    def draw_gameplay(self):
        """Draw gameplay screen"""
        self.screen.blit(self.bg_game, (0, 0))
        self.screen.blit(self.player.image, self.player.rect)
        self.trash_group.draw(self.screen)
        self.ui.draw_hud(self.screen, self.player, self.stats, self.current_level_num)
    
    def draw_paused(self, mouse_pos):
        """Draw pause screen"""
        self.draw_gameplay()
        
        # Dim overlay
        s = pygame.Surface((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))
        self.screen.blit(s, (0, 0))
        
        self.ui.draw_text(self.screen, "PAUSED", 40, 
                         Config.SCREEN_WIDTH//2, 200, Config.WHITE, True)
        
        for btn in self.buttons["paused"]:
            btn.check_hover(mouse_pos)
            btn.draw(self.screen, self.ui)
    
    def draw_game_over(self, mouse_pos):
        """Draw game over screen"""
        # Dim overlay
        s = pygame.Surface((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))
        self.screen.blit(s, (0, 0))
        
        self.ui.draw_text(self.screen, "GAME OVER", 50, 
                         Config.SCREEN_WIDTH//2, 200, Config.RED, True)
        
        for btn in self.buttons["game_over"]:
            btn.check_hover(mouse_pos)
            btn.draw(self.screen, self.ui)
    
    def run(self):
        running = True
        
        while running:
            dt = self.clock.tick(Config.FPS)
            mouse_pos = pygame.mouse.get_pos()
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Level intro - any key starts
                if self.state == GameState.LEVEL_INTRO:
                    if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                        self.state = GameState.PLAYING
                
                # Mouse clicks
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    active_btns = []
                    if self.state == GameState.TITLE:
                        active_btns = self.buttons["title"]
                    elif self.state == GameState.LEVEL_SELECT:
                        active_btns = self.buttons["level_select"]
                    elif self.state == GameState.PAUSED:
                        active_btns = self.buttons["paused"]
                    elif self.state == GameState.GAME_OVER:
                        active_btns = self.buttons["game_over"]
                    
                    for btn in active_btns:
                        if btn.check_hover(mouse_pos):
                            self.handle_click(btn.action_code)
                
                # Keyboard input
                if event.type == pygame.KEYDOWN:
                    # Pause/unpause
                    if event.key == pygame.K_ESCAPE:
                        if self.state == GameState.PLAYING:
                            self.state = GameState.PAUSED
                        elif self.state == GameState.PAUSED:
                            self.state = GameState.PLAYING
                    
                    # Swap bin
                    if self.state == GameState.PLAYING and event.key == pygame.K_e:
                        if self.player.swap_bin():
                            self.sound.play("swap")
                    
                    # Game over shortcuts
                    if self.state == GameState.GAME_OVER:
                        if event.key == pygame.K_r:
                            self.start_level(self.current_level_num)
                        elif event.key == pygame.K_b:
                            self.state = GameState.LEVEL_SELECT
            
            # Update
            self.cursor.update()
            
            if self.state == GameState.PLAYING:
                self.update_gameplay(dt)
            
            # Drawing
            self.screen.fill(Config.BLACK)
            
            if self.state == GameState.TITLE:
                self.draw_title_screen(mouse_pos)
            elif self.state == GameState.LEVEL_SELECT:
                self.draw_level_select(mouse_pos)
            elif self.state == GameState.LEVEL_INTRO:
                self.draw_level_intro()
            elif self.state == GameState.PLAYING:
                self.draw_gameplay()
            elif self.state == GameState.PAUSED:
                self.draw_paused(mouse_pos)
            elif self.state == GameState.GAME_OVER:
                self.draw_game_over(mouse_pos)
            
            # Always draw cursor on top
            self.cursor.draw(self.screen)
            pygame.display.flip()
        
        # Cleanup
        self.save.save()
        pygame.quit()
        sys.exit()