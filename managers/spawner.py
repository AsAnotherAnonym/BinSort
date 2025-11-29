import random
from config import TrashType
from entities.trash import Trash


class Spawner:

    def __init__(self, level_data):
        self.speed = level_data['speed']
        self.total = level_data['total_trash']
        self.interval = level_data['spawn_interval']
        
        self.count = 0
        self.last_spawn_time = 0
        self.finished = False
    
    def update(self, current_time, group):
        """Update spawner and create new trash if needed"""
        if self.finished:
            return
        
        if current_time - self.last_spawn_time > self.interval:
            self._spawn(group)
            self.last_spawn_time = current_time
            
            if self.count >= self.total:
                self.finished = True
    
    def _spawn(self, group):
        self.count += 1
        
        # Determine trash type (5% bonus, 47.5% organic, 47.5% inorganic)
        roll = random.random()
        if roll < 0.05:
            t_type = TrashType.BONUS
        elif roll < 0.525:
            t_type = TrashType.ORGANIC
        else:
            t_type = TrashType.INORGANIC
        
        # Add speed variation
        speed_variation = random.uniform(0.9, 1.1)
        trash = Trash(t_type, self.speed * speed_variation)
        group.add(trash)
    
    def is_finished(self):
        """Check if all trash has been spawned"""
        return self.finished
    
    def get_progress(self):
        """Get spawn progress (0.0 to 1.0)"""
        return self.count / self.total if self.total > 0 else 1.0