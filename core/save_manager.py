import json
import os
from config import Config


class SaveManager:
    
    def __init__(self):
        self.data = {"unlocked_level": 1}
        self._ensure_data_dir()
        self.load()
    
    def _ensure_data_dir(self):
        data_dir = os.path.dirname(Config.SAVE_FILE)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def save(self):
        try:
            with open(Config.SAVE_FILE, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Error saving game: {e}")
    
    def load(self):
        if os.path.exists(Config.SAVE_FILE):
            try:
                with open(Config.SAVE_FILE, 'r') as f:
                    self.data = json.load(f)
            except Exception as e:
                print(f"Error loading save file: {e}")
    
    def unlock_level(self, level):
        if level > self.data["unlocked_level"]:
            self.data["unlocked_level"] = level
            self.save()
    
    def get_unlocked_level(self):
        return self.data["unlocked_level"]
    
    def reset_progress(self):
        self.data = {"unlocked_level": 1}
        self.save()