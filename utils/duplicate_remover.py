import json
import os

def remove_duplicates_from_interactions():
    """Entfernt Duplikate aus interactions.json (basierend auf vollständigem Eintrag) und gibt Anzahl der entfernten Duplikate aus."""
    path = os.path.join("data", "rlhf", "logs", "interactions.json")
    
    if not os.path.exists(path):
        print("❌ interactions.json nicht gefunden.")
        return

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            print("⚠️ interactions.json enthält keine Liste von Einträgen.")
            return

        initial_count = len(data)
        seen = set()
        cleaned_data = []
        for entry in data:
            identifier = json.dumps(entry, sort_keys=True)
            if identifier not in seen:
                seen.add(identifier)
                cleaned_data.append(entry)
        
        duplicates_removed = initial_count - len(cleaned_data)
        
        # Überschreibt die ursprüngliche Datei
        with open(path, "w", encoding="utf-8") as f:
            json.dump(cleaned_data, f, indent=4, ensure_ascii=False)
        
        print(f"🧹 Duplikat-Check abgeschlossen: {duplicates_removed} Duplikate entfernt.")
    except Exception as e:
        print(f"❌ Fehler beim Entfernen von Duplikaten: {e}")

if __name__ == "__main__":
    remove_duplicates_from_interactions()