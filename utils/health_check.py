import os
import json

def check_interactions():
    path = os.path.join("data", "rlhf", "logs", "interactions.json")
    if not os.path.exists(path):
        print("❌ interactions.json nicht gefunden.")
        return
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    total = len(data)
    with_rewards = sum(1 for entry in data if isinstance(entry.get("reward"), (int, float)) and entry["reward"] != 0)
    print(f"✅ Interactions: {total} Einträge gefunden, davon {with_rewards} mit reward ≠ 0.")

def check_q_table():
    path = os.path.join("data", "rlhf", "q_table.json")
    if not os.path.exists(path):
        print("❌ q_table.json nicht gefunden.")
        return
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                print("⚠️ q_table.json existiert, ist aber leer.")
                return
            data = json.loads(content)
        if not data:
            print("⚠️ q_table.json ist leer ({} oder []).")
        else:
            print(f"✅ q_table.json enthält {len(data)} States/Aktionen.")
    except json.JSONDecodeError:
        print("❌ q_table.json enthält kein gültiges JSON (möglicherweise leer oder beschädigt).")

def check_embeddings():
    path = os.path.join("data", "rlhf", "embeddings.json")
    if not os.path.exists(path):
        print("⚠️ embeddings.json existiert nicht.")
    else:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"✅ embeddings.json vorhanden mit {len(data)} Einträgen.")

def run_health_check():
    print("🔍 RLHF System Health Check:\n")
    check_interactions()
    check_q_table()
    check_embeddings()
    print("\n🚀 Check abgeschlossen.")

if __name__ == "__main__":
    run_health_check()