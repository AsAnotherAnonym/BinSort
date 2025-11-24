import pygame
import math
import random
import array

class AudioFactory:
    @staticmethod
    def generate_sound(wave_type="square", frequency=440, duration=0.1, volume=0.5):
        """
        Generates object SFX's from math library

        Melakukan generate SFX untuk objek-objek dengan library math
        """
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        buf = array.array('h') # 'h' is signed short (16-bit)
        
        for i in range(n_samples):
            t = float(i) / sample_rate
            
            # Oscillators
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
            
            # Apply generic decay envelope (fade out)
            envelope = 1.0 - (i / n_samples)
            
            # Scale to 16-bit integer range (-32767 to 32767)
            sample = int(val * volume * envelope * 32767)
            buf.append(sample)
            
        return pygame.mixer.Sound(buffer=buf)