import config

class LevelManager:
    def __init__(self):
        self.levels = {}
        self.generate_levels()
        
    def generate_levels(self):
        # Algorithmic generation of 10 levels
        for i in range(1, 11):
            # Speed increases log/linearly
            speed = config.Config.BASE_TRASH_SPEED + (i * 0.35)
            # Amount increases
            amount = 10 + (i * 5)
            # Spawn interval decreases
            interval = max(500, 2000 - (i * 120))
            
            self.levels[i] = {
                "speed": speed,
                "total_trash": amount,
                "spawn_interval": interval
            }
            
    def get_level_data(self, level_num):
        return self.levels.get(level_num, self.levels[1])