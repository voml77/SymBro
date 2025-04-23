# utils/embedding_generator.py

import json
import os
from utils.embedding_core import generate_embedding
from utils.embedding_analyzer import get_outlier_weight
import numpy as np

def generate_and_save_embedding(sample, sample_id):
    embedding = generate_embedding(sample)
    embedding = np.array(embedding)
    if embedding.ndim == 3:
        embedding = embedding.squeeze()
    if embedding.ndim == 1:
        embedding = embedding.reshape(1, -1)
    # Sicherheitsprüfung: Outlier-Check nur bei ausreichender Anzahl
    existing_path = os.path.join("data", "rlhf", "embeddings.json")
    try:
        with open(existing_path, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
        all_embeddings = [entry["embedding"] for entry in existing_data if "embedding" in entry]
        if len(all_embeddings) < 10:
            print("⚠️ Outlier-Check übersprungen – zu wenige Vergleichsembeddings.")
            outlier_weight = 1.0
        else:
            outlier_weight = get_outlier_weight(embedding)
    except Exception as e:
        print(f"⚠️ Fehler beim Outlier-Check: {e}")
        outlier_weight = 1.0

    entry = {
        "id": sample_id,
        "embedding": embedding.tolist(),  # falls NumPy-Array
        "outlier_weight": outlier_weight
    }

    path = os.path.join("data", "rlhf", "embeddings.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    
    print(f"✅ Embedding für '{sample_id}' gespeichert (Outlier-Weight: {outlier_weight}).")


# -------------------------------------------------------------
# Neue Funktion: Lade Embeddings in ReplayBuffer
from modules.rlhf.replay_buffer import PrioritizedReplayBuffer as ReplayBuffer
import os
import json

# Automatischer Embedding-Sync

def load_embeddings_to_buffer(buffer):
    """
    Lädt Embeddings aus embeddings.json und füllt den ReplayBuffer.
    Priorität wird aus reward * outlier_weight berechnet.
    """
    embeddings_path = os.path.join("data", "rlhf", "embeddings.json")
    interactions_path = os.path.join("data", "rlhf", "logs", "interactions.json")

    if not os.path.exists(embeddings_path):
        print("⚠️ embeddings.json nicht gefunden.")
        return
    if not os.path.exists(interactions_path):
        print("⚠️ interactions.json nicht gefunden.")
        return

    with open(embeddings_path, "r", encoding="utf-8") as f:
        embeddings = json.load(f)
    with open(interactions_path, "r", encoding="utf-8") as f:
        interactions = json.load(f)

    interaction_map = {entry.get("id"): entry for entry in interactions}

    count = 0
    for entry in embeddings:
        sample_id = entry.get("id")
        embedding = entry.get("embedding")
        outlier_weight = entry.get("outlier_weight", 1.0)
        log_entry = interaction_map.get(sample_id)

        if log_entry:
            reward = log_entry.get("reward")
            state = log_entry.get("state")
            action = log_entry.get("action")
            next_state = log_entry.get("next_state")

            if None not in (state, action, reward, next_state):
                if isinstance(reward, (int, float)):
                    priority = reward * outlier_weight
                    buffer.add(state, action, reward, next_state, priority)
                    count += 1
                else:
                    print(f"⏭️  Ungültiger Reward für ID '{sample_id}' → übersprungen.")
        else:
            print(f"⏭️  Kein Log-Eintrag für Embedding-ID '{sample_id}' gefunden.")

    print(f"✅ ReplayBuffer befüllt mit {count} Einträgen aus embeddings.json und interactions.json.")

def auto_sync_embeddings_to_buffer(buffer):
    """
    Automatischer Sync: prüft, ob neue Embeddings vorliegen und synchronisiert diese mit dem ReplayBuffer.
    Sollte idealerweise zyklisch oder beim Start des Trainings aufgerufen werden.
    """
    try:
        load_embeddings_to_buffer(buffer)
    except Exception as e:
        print(f"⚠️ Fehler beim automatischen Embedding-Sync: {e}")