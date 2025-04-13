import json
import os
import datetime

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

    def save_chat(self, messages):
        chat_id = datetime.datetime.now().strftime("chat_%Y%m%d_%H%M%S")
        title = self.generate_title_from_message(messages[0]["content"]) if messages else "Neuer Chat"
        chat_data = {
            "id": chat_id,
            "title": title,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "messages": messages
        }
        chat_dir = 'data/chats/'
        os.makedirs(chat_dir, exist_ok=True)
        chat_path = os.path.join(chat_dir, f"{chat_id}.json")
        with open(chat_path, 'w') as f:
            json.dump(chat_data, f, indent=4)
        self.update_chats_list(chat_data)

    def update_chats_list(self, chat_data):
        chats_file = 'data/chats/chats.json'
        os.makedirs('data/chats/', exist_ok=True)
        chats = []

        if os.path.exists(chats_file):
            with open(chats_file, 'r') as f:
                chats = json.load(f)

        # Prüfen ob Chat bereits existiert (z.B. bei Überschreiben)
        chats = [chat for chat in chats if chat['id'] != chat_data['id']]
        chats.append({
            "id": chat_data["id"],
            "title": chat_data["title"]
        })

        with open(chats_file, 'w') as f:
            json.dump(chats, f, indent=4)

    def generate_title_from_message(self, message):
        title = message.strip()
        return title[:30]

    def load_chats(self):
        chat_dir = 'data/chats/'
        if not os.path.exists(chat_dir):
            return []

        chats = []
        for filename in os.listdir(chat_dir):
            if filename.endswith('.json'):
                path = os.path.join(chat_dir, filename)
                with open(path, 'r') as f:
                    chat_data = json.load(f)
                    chats.append({
                        "id": chat_data.get("id"),
                        "title": chat_data.get("title")
                    })
        return chats

    def delete_chat(self, chat_id):
        chat_path = os.path.join('data/chats/', f"{chat_id}.json")
        if os.path.exists(chat_path):
            os.remove(chat_path)