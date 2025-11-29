"""
Audio generation and management
"""
import pygame
import math
import random
import array


class AudioFactory:
    
    @staticmethod
    def generate_sound(wave_type="square", frequency=440, duration=0.1, volume=0.5):
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        buf = array.array('h')
        
        for i in range(n_samples):
            t = float(i) / sample_rate
            
            # Generate waveform
            if wave_type == "sine":
                val = math.sin(2 * math.pi * frequency * t)
            elif wave_type == "square":
                val = 1.0 if math.sin(2 * math.pi * frequency * t) > 0 else -1.0
            elif wave_type == "saw":
                val = 2.0 * (t * frequency - math.floor(t * frequency + 0.5))
            elif wave_type == "noise":
                val = random.uniform(-1, 1)
            else:
                val = 0
            
            # Apply envelope
            envelope = 1.0 - (i / n_samples)
            sample = int(val * volume * envelope * 32767)
            buf.append(sample)
        
        return pygame.mixer.Sound(buffer=buf)


class SoundManager:
    
    def __init__(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=44100, size=-16, channels=1)
        
        # Pre-generate all sound effects
        self.sfx_catch = AudioFactory.generate_sound("square", 880, 0.1, 0.3)
        self.sfx_swap = AudioFactory.generate_sound("sine", 600, 0.05, 0.4)
        self.sfx_hurt = AudioFactory.generate_sound("saw", 150, 0.3, 0.4)
        self.sfx_bonus = AudioFactory.generate_sound("sine", 1200, 0.2, 0.3)
        self.sfx_click = AudioFactory.generate_sound("noise", 500, 0.05, 0.2)
    
    def play(self, name):
        sound_map = {
            'catch': self.sfx_catch,
            'swap': self.sfx_swap,
            'hurt': self.sfx_hurt,
            'bonus': self.sfx_bonus,
            'click': self.sfx_click
        }
        
        if name in sound_map:
            sound_map[name].play()