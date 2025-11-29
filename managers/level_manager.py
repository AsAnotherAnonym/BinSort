from config import Config


class LevelManager:
    
    def __init__(self):
        self.levels = {}
        self._generate_levels()
    
    def _generate_levels(self):
        for i in range(1, 11):
            self.levels[i] = {
                "speed": Config.BASE_TRASH_SPEED + (i * 0.25),
                "total_trash": 10 + (i * 5),
                "spawn_interval": max(550, 2300 - (i * 130))
            }
    
    def get_level_data(self, level_num):
        return self.levels.get(level_num, self.levels[1])
    
    def get_total_levels(self):
        return len(self.levels)