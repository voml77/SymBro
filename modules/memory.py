import json
import os
import datetime

class Memory:
    def __init__(self):
        self.base_dir = 'data/memory/'
        self.chat_dir = 'data/chats/'
        self.chats_index_file = os.path.join(self.chat_dir, 'chats.json')
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
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(self.chat_dir, exist_ok=True)
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

    def save_chat(self, chat_id, title, messages):
        if not isinstance(messages, list) or not all(isinstance(m, dict) for m in messages):
            print("Ungültige Nachrichtenstruktur – Abbruch")
            return

        chat_data_to_save = {
            "id": chat_id,
            "title": title,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "messages": messages
        }

        os.makedirs(self.chat_dir, exist_ok=True)
        chat_path = os.path.join(self.chat_dir, f"{chat_id}.json")
        try:
            with open(chat_path, 'w') as f:
                json.dump(chat_data_to_save, f, indent=4)
        except Exception as e:
            print(f"Fehler beim Speichern des Chats ({chat_id}): {e}")
        self.update_chats_list(chat_id, title)

    def update_chats_list(self, chat_id, title, is_favorite=False):
        os.makedirs(self.chat_dir, exist_ok=True)
        chats = []

        if os.path.exists(self.chats_index_file):
            try:
                with open(self.chats_index_file, 'r') as f:
                    chats = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Fehler beim Laden der Chat-Liste: {e}")

        updated = False
        for chat in chats:
            if chat["id"] == chat_id:
                chat["title"] = title
                chat["favorite"] = is_favorite
                updated = True
                break
        if not updated:
            chats.append({
                "id": chat_id,
                "title": title,
                "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "favorite": is_favorite
            })

        with open(self.chats_index_file, 'w') as f:
            json.dump(chats, f, indent=4)

    def generate_title_from_message(self, message):
        title = message.strip()
        return title[:30]

    def load_chats(self):
        if not os.path.exists(self.chats_index_file):
            return []

        try:
            with open(self.chats_index_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Fehler beim Laden von {self.chats_index_file}: {e}")
            return []

    def load_chat_by_id(self, chat_id):
        chat_path = os.path.join(self.chat_dir, f"{chat_id}.json")
        if os.path.exists(chat_path):
            with open(chat_path, 'r') as f:
                return json.load(f)
        return None

    def delete_chat(self, chat_id):
        chat_path = os.path.join(self.chat_dir, f"{chat_id}.json")
        if os.path.exists(chat_path):
            os.remove(chat_path)