from core.audio_factory import AudioFactory
import pygame

class SoundManager:
    def __init__(self):
        # Initialize mixer
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=44100, size=-16, channels=1)
            
        # Pre-generate SFX
        self.sfx_catch = AudioFactory.generate_sound("square", 880, 0.1, 0.3)
        self.sfx_swap = AudioFactory.generate_sound("sine", 600, 0.05, 0.4)
        self.sfx_hurt = AudioFactory.generate_sound("saw", 150, 0.3, 0.4)
        self.sfx_bonus = AudioFactory.generate_sound("sine", 1200, 0.2, 0.3)
        self.sfx_click = AudioFactory.generate_sound("noise", 500, 0.05, 0.2)

    def play(self, name):
        if name == 'catch': self.sfx_catch.play()
        elif name == 'swap': self.sfx_swap.play()
        elif name == 'hurt': self.sfx_hurt.play()
        elif name == 'bonus': self.sfx_bonus.play()
        elif name == 'click': self.sfx_click.play()