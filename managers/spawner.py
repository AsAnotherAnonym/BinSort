import config
import random
from entities.trash import Trash

class Spawner:
    def __init__(self, level_data):
        self.speed = level_data['speed']
        self.total_to_spawn = level_data['total_trash']
        self.spawn_interval = level_data['spawn_interval']
        
        self.spawned_count = 0
        self.last_spawn = 0
        self.finished_spawning = False
        
    def update(self, current_time, trash_group):
        if self.finished_spawning:
            return

        if current_time - self.last_spawn > self.spawn_interval:
            self.spawn_trash(trash_group)
            self.last_spawn = current_time
            
            if self.spawned_count >= self.total_to_spawn:
                self.finished_spawning = True
                
    def spawn_trash(self, group):
        self.spawned_count += 1
        
        # Chance logic
        roll = random.random()
        if roll < 0.05: # 5% chance for bonus
            t_type = config.TrashType.BONUS
        elif roll < 0.525:
            t_type = config.TrashType.ORGANIC
        else:
            t_type = config.TrashType.INORGANIC
            
        # Speed variance
        s = self.speed * random.uniform(0.9, 1.1)
        t = Trash(t_type, s)
        group.add(t)