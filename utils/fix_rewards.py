import json
import os

def fix_rewards(path="data/rlhf/logs/interactions.json"):
    if not os.path.exists(path):
        print("⚠️ Logdatei nicht gefunden.")
        return

    with open(path, "r", encoding="utf-8") as f:
        logs = json.load(f)

    converted = 0
    for entry in logs:
        reward = entry.get("reward")
        if isinstance(reward, str):
            try:
                entry["reward"] = float(reward)
                converted += 1
            except ValueError:
                continue

    with open(path, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=4)

    print(f"🛠️ {converted} Rewards als float gespeichert.")

if __name__ == "__main__":
    fix_rewards()