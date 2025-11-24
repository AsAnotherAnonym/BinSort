import config
import json
import os

class SaveManager:
    def __init__(self):
        self.data = {"unlocked_level": 1}
        self.load()
        
    def save(self):
        with open(config.Config.SAVE_FILE, 'w') as f:
            json.dump(self.data, f)
            
    def load(self):
        if os.path.exists(config.Config.SAVE_FILE):
            try:
                with open(config.Config.SAVE_FILE, 'r') as f:
                    self.data = json.load(f)
            except:
                pass # Corrupt file or error, keep default
                
    def unlock_level(self, level):
        if level > self.data["unlocked_level"]:
            self.data["unlocked_level"] = level
            self.save()