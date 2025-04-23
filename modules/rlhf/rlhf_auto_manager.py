import os
import json
from utils.embedding_generator import auto_sync_embeddings_to_buffer

def has_new_embeddings():
    path = os.path.join("data", "rlhf", "embeddings.json")
    if not os.path.exists(path):
        return False

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return any("replay_synced" not in e or not e["replay_synced"] for e in data)

def start_rlhf_pipeline():
    if has_new_embeddings():
        print("🔄 Neue Embeddings erkannt – synchronisiere...")
        auto_sync_embeddings_to_buffer()
        print("✅ Synchronisierung abgeschlossen.")
        # Optional subprocess starten
        os.system("python3 train_rlhf.py")
    else:
        print("📭 Keine neuen Embeddings – Training übersprungen.")