import json
import os

class Memory:
    def __init__(self):
        self.base_dir = 'data/memory/'
        self.files = {
            'general': os.path.join(self.base_dir, 'general.json'),
            'events': os.path.join(self.base_dir, 'events.json'),
            'preferences': os.path.join(self.base_dir, 'preferences.json')
        }
        self.memory = {
            'general': {},
            'events': {},
            'preferences': {}
        }
        self.load_memory()

    def load_memory(self):
        for category, file_path in self.files.items():
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                with open(file_path, 'r') as f:
                    self.memory[category] = json.load(f)

    def remember(self, category, key, value):
        if category in self.memory:
            self.memory[category][key] = value
            self.save_memory(category)
        else:
            print(f"Unbekannte Kategorie: {category}")

    def recall(self, category, key):
        return self.memory.get(category, {}).get(key, None)

    def save_memory(self, category):
        if category in self.memory:
            os.makedirs(os.path.dirname(self.files[category]), exist_ok=True)
            with open(self.files[category], 'w') as f:
                json.dump(self.memory[category], f, indent=4)