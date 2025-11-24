import config
from managers import *
from ui import *
from core.save_manager import SaveManager
from entities.player import Player
import pygame

class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.Config.SCREEN_WIDTH, config.Config.SCREEN_HEIGHT))
        pygame.display.set_caption(config.Config.TITLE)
        self.clock = pygame.time.Clock()
        
        # Hide OS Cursor
        pygame.mouse.set_visible(False)
        self.cursor = Cursor()
        
        self.sound_manager = SoundManager()
        self.save_manager = SaveManager()
        self.level_manager = LevelManager()
        self.ui_manager = UIManager()
        
        self.state = config.GameState.TITLE
        self.current_level_num = 1
        
        # Initialize Buttons
        self.buttons = {
            "title": [UIElement(config.Config.SCREEN_WIDTH//2 - 100, 400, 200, 50, "PLAY", "goto_level_select")],
            "level_select": [], # Populated dynamically
            "paused": []
        }
        self._init_level_buttons()
        
        self.reset_game_session()

    def _init_level_buttons(self):
        # Create grid of level buttons + Back button
        btns = []
        for i in range(1, 11):
            x = 150 + ((i-1)%5) * 100
            y = 250 + ((i-1)//5) * 80
            btns.append(UIElement(x, y, 80, 60, f"LVL {i}", f"lvl_{i}"))
        
        # Add Return to Title Button
        btns.append(UIElement(20, 20, 150, 40, "< BACK", "goto_title"))
        self.buttons["level_select"] = btns

    def reset_game_session(self):
        self.player = Player()
        self.trash_group = pygame.sprite.Group()
        self.spawner = None
        self.stats = {"caught": 0, "missed": 0, "total": 0}
        
    def start_level(self, level_num):
        if level_num > self.save_manager.data["unlocked_level"]:
            self.sound_manager.play("hurt") # Deny sound
            return
            
        self.sound_manager.play("click")
        self.current_level_num = level_num
        self.reset_game_session()
        level_data = self.level_manager.get_level_data(level_num)
        self.spawner = Spawner(level_data)
        self.state = config.GameState.PLAYING
        
    def handle_ui_click(self, action):
        self.sound_manager.play("click")
        
        if action == "goto_level_select":
            self.state = config.GameState.LEVEL_SELECT
        elif action == "goto_title":
            self.state = config.GameState.TITLE
        elif action.startswith("lvl_"):
            lvl_num = int(action.split("_")[1])
            self.start_level(lvl_num)

    def handle_gameplay_collisions(self):
        hits = pygame.sprite.spritecollide(self.player, self.trash_group, True)
        for trash in hits:
            if trash.type == config.TrashType.BONUS:
                self.player.health += 1
                self.sound_manager.play("bonus")
            elif trash.type == self.player.current_type:
                self.stats['caught'] += 1
                self.sound_manager.play("catch")
            else:
                self.player.health -= 1
                self.sound_manager.play("hurt")
        
        # Missed trash logic
        for trash in self.trash_group:
            if trash.rect.top > config.Config.SCREEN_HEIGHT:
                trash.kill()
                if trash.type != config.TrashType.BONUS:
                    self.player.health -= 1
                    self.sound_manager.play("hurt")

        if self.player.health <= 0:
            self.state = config.GameState.GAME_OVER
            
        if self.spawner.finished_spawning and len(self.trash_group) == 0 and self.player.health > 0:
            self.save_manager.unlock_level(self.current_level_num + 1)
            self._init_level_buttons() # Refresh unlock visuals if needed
            self.state = config.GameState.LEVEL_SELECT

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(config.Config.FPS)
            mouse_pos = pygame.mouse.get_pos()
            
            # --- INPUT HANDLING ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Mouse Click Logic
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.state in [config.GameState.TITLE, config.GameState.LEVEL_SELECT]:
                        active_btns = self.buttons["title"] if self.state == config.GameState.TITLE else self.buttons["level_select"]
                        for btn in active_btns:
                            if btn.check_hover(mouse_pos):
                                self.handle_ui_click(btn.action_code)

                # Keyboard Logic
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state == config.GameState.PLAYING:
                            self.state = config.GameState.PAUSED
                        elif self.state == config.GameState.PAUSED:
                            self.state = config.GameState.PLAYING
                    
                    if self.state == config.GameState.PLAYING and event.key == pygame.K_e:
                        self.player.swap_bin()
                        self.sound_manager.play("swap")
                        
                    if self.state == config.GameState.GAME_OVER:
                        if event.key == pygame.K_r: self.start_level(self.current_level_num)
                        elif event.key == pygame.K_b: self.state = config.GameState.LEVEL_SELECT

            # --- UPDATE ---
            self.cursor.update()
            
            if self.state == config.GameState.TITLE:
                for btn in self.buttons["title"]: btn.check_hover(mouse_pos)
            
            elif self.state == config.GameState.LEVEL_SELECT:
                for btn in self.buttons["level_select"]: btn.check_hover(mouse_pos)

            elif self.state == config.GameState.PLAYING:
                keys = pygame.key.get_pressed()
                self.player.update(keys, dt)
                self.spawner.update(pygame.time.get_ticks(), self.trash_group)
                self.trash_group.update()
                self.handle_gameplay_collisions()

            # --- DRAW ---
            self.screen.fill(config.Config.BLACK)
            
            if self.state == config.GameState.TITLE:
                self.ui_manager.draw_text(self.screen, config.Config.TITLE, 80, config.Config.SCREEN_WIDTH//2, 200, config.Config.GREEN, True)
                for btn in self.buttons["title"]: btn.draw(self.screen, self.ui_manager.font)
                
            elif self.state == config.GameState.LEVEL_SELECT:
                self.ui_manager.draw_text(self.screen, "SELECT LEVEL", 40, config.Config.SCREEN_WIDTH//2, 100, config.Config.WHITE, True)
                for btn in self.buttons["level_select"]:
                    # Visual dimming for locked levels
                    if btn.action_code.startswith("lvl_"):
                        lvl = int(btn.action_code.split("_")[1])
                        if lvl > self.save_manager.data["unlocked_level"]:
                            # Draw simplistic lock overlay
                            btn.draw(self.screen, self.ui_manager.font)
                            s = pygame.Surface((btn.rect.width, btn.rect.height), pygame.SRCALPHA)
                            s.fill((0, 0, 0, 150))
                            self.screen.blit(s, btn.rect)
                            continue
                    btn.draw(self.screen, self.ui_manager.font)

            elif self.state == config.GameState.PLAYING:
                self.screen.blit(self.player.image, self.player.rect)
                self.trash_group.draw(self.screen)
                self.ui_manager.draw_hud(self.screen, self.player, self.stats, self.current_level_num)
            
            elif self.state == config.GameState.GAME_OVER:
                self.ui_manager.draw_text(self.screen, "GAME OVER", 60, config.Config.SCREEN_WIDTH//2, 200, config.Config.RED, True)
                self.ui_manager.draw_text(self.screen, "[R] Restart   [B] Back", 30, config.Config.SCREEN_WIDTH//2, 300, config.Config.WHITE, True)

            # Draw Custom Cursor Last
            self.cursor.draw(self.screen)
            
            pygame.display.flip()