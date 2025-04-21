import os
import json
import random
import datetime
from modules.rlhf.replay_buffer import PrioritizedReplayBuffer

action_space = ["antwort_1", "antwort_2", "antwort_3"]

class QLearningAgent:
    def __init__(self, state_space, action_space, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0):
        self.state_space = state_space
        self.action_space = action_space
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = exploration_rate
        self.q_table = {}

    def serialize(self, state, action):
        return str((state, action))

    def get_q_value(self, state, action):
        return self.q_table.get(self.serialize(state, action), 0.0)

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.action_space)
        else:
            q_values = [self.get_q_value(state, a) for a in self.action_space]
            max_q = max(q_values)
            return self.action_space[q_values.index(max_q)]

    def update(self, state, action, reward, next_state):
        key = self.serialize(state, action)
        old_q = self.get_q_value(state, action)
        future_rewards = max([self.get_q_value(next_state, a) for a in self.action_space])
        new_q = (1 - self.lr) * old_q + self.lr * (reward + self.gamma * future_rewards)
        self.q_table[key] = new_q

    def save(self, path="data/rlhf/q_table.json"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump({str(k): v for k, v in self.q_table.items()}, f)

    def load(self, path="data/rlhf/q_table.json"):
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
                self.q_table = {eval(k): v for k, v in data.items()}

    def compute_td_error(self, state, action, reward, next_state):
        current_q = self.get_q_value(state, action)
        next_max_q = max([self.get_q_value(next_state, a) for a in self.action_space])
        target_q = reward + self.gamma * next_max_q
        td_error = abs(current_q - target_q)
        return td_error

buffer = PrioritizedReplayBuffer(capacity=1000)

def log_interaction(state, action, reward, next_state):
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "state": state,
        "action": action,
        "reward": reward,
        "next_state": next_state
    }

    log_dir = os.path.join("data", "rlhf", "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "interactions.json")

    try:
        with open(log_path, "r", encoding="utf-8") as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []

    logs.append(log_entry)

    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)


def update_reward_for_last_interaction(reward):
    """Aktualisiert das Reward-Feld des letzten Eintrags in logs.json."""
    import json
    import os

    log_file = os.path.join("data", "rlhf", "logs", "interactions.json")
    if not os.path.exists(log_file):
        print("⚠️ Keine Interaktions-Logdatei gefunden.")
        return

    try:
        with open(log_file, "r", encoding="utf-8") as f:
            logs = json.load(f)

        if not logs:
            print("⚠️ Keine Einträge in der Logdatei.")
            return

        if reward == 1.0:
            logs[-1]["reward"] = "PENDING_POSITIV"
        elif reward == -1.0:
            logs[-1]["reward"] = "PENDING_NEGATIV"
        else:
            logs[-1]["reward"] = "PENDING"

        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=4)

        print(f"✅ Reward aktualisiert: {reward}")
    except Exception as e:
        print(f"Fehler beim Aktualisieren des Rewards: {e}")
    
    # Automatisches Replay-Training nach Belohnung
    try:
        global_buffer = buffer  # Nutze direkt die lokale Instanz
        agent = QLearningAgent(state_space=[], action_space=action_space)  # <- ggf. action_space anpassen!
        sync_buffer_from_logs(global_buffer)
        train_from_buffer(agent, global_buffer, batch_size=5)
    except Exception as e:
        print(f"⚠️ Autotraining fehlgeschlagen: {e}")

def sync_buffer_from_logs(buffer, max_entries=1000):
    """Lädt Interaktionen aus interactions.json und füllt den ReplayBuffer."""
    path = os.path.join("data", "rlhf", "logs", "interactions.json")
    if not os.path.exists(path):
        print("⚠️ interactions.json nicht gefunden.")
        return

    try:
        with open(path, "r", encoding="utf-8") as f:
            logs = json.load(f)

        count = 0
        for entry in reversed(logs):
            if count >= max_entries:
                break
            state = entry.get("state")
            action = entry.get("action")
            reward = entry.get("reward")
            next_state = entry.get("next_state")

            if None not in (state, action, reward, next_state):
                agent = QLearningAgent(state_space=[], action_space=action_space)  # Temporärer Agent zur TD-Berechnung
                try:
                    # Nur numerische Rewards zulassen
                    if isinstance(reward, (int, float)):
                        td_error = agent.compute_td_error(state, action, reward, next_state)
                        buffer.add(state, action, reward, next_state, priority=td_error)
                        count += 1
                    else:
                        print(f"⏭️  Eintrag übersprungen: reward='{reward}' ist kein numerischer Wert.")
                except Exception as inner_e:
                    print(f"⚠️ Fehler bei Eintrag Nr. {count}: {inner_e}")
                    print(f"   ↪️  state={state} ({type(state)}), action={action} ({type(action)}), reward={reward} ({type(reward)}), next_state={next_state} ({type(next_state)})")

        print(f"🔁 ReplayBuffer initialisiert mit {str(count)} Einträgen aus Logdatei.")
    except Exception as e:
        print(f"Fehler beim Synchronisieren mit Logdatei: {e}")

def apply_td_errors_to_buffer(indices, priorities):
    """
    Übergibt TD-Fehler an den PrioritizedReplayBuffer zur Prioritätsaktualisierung.
    """
    try:
        buffer.update_priorities_from_indices(indices, priorities)
    except Exception as e:
        print(f"⚠️ Fehler beim Aktualisieren der Prioritäten: {e}")

def load_logs_to_replay_buffer(buffer, max_entries=1000):
    """Alias für sync_buffer_from_logs, um Namenskonflikte zu vermeiden und Lesbarkeit zu verbessern."""
    sync_buffer_from_logs(buffer, max_entries=max_entries)

__all__ = ["log_interaction", "update_reward_for_last_interaction", "update_priorities", "load_logs_to_replay_buffer", "buffer"]

def train_from_buffer(agent, buffer, batch_size=10):
    samples_data = buffer.sample(batch_size)
    samples, indices, _ = samples_data
    if len(samples) < batch_size:
        print("⚠️ Zu wenig Daten im ReplayBuffer für Training.")
        return

    priorities = []

    for idx, (state, action, reward, next_state) in enumerate(samples):
        # Agent lernt mit Sample
        agent.update(state, action, reward, next_state)

        # TD-Fehler neu berechnen
        td_error = agent.compute_td_error(state, action, reward, next_state)
        priorities.append(td_error)

    # Prioritäten im Buffer aktualisieren
    apply_td_errors_to_buffer(indices, priorities)

    print(f"🎓 Agent mit {batch_size} Samples trainiert.")

def summarize_log_rewards():
    """Gibt eine Übersicht über bewertete und unbeantwortete Einträge im RLHF-Log."""
    path = os.path.join("data", "rlhf", "logs", "interactions.json")
    if not os.path.exists(path):
        print("⚠️ Kein Logfile vorhanden.")
        return

    try:
        with open(path, "r", encoding="utf-8") as f:
            logs = json.load(f)

        pending, rated, positive, negative = 0, 0, 0, 0
        for entry in logs:
            reward = entry.get("reward")
            if isinstance(reward, (int, float)):
                rated += 1
                if reward > 0:
                    positive += 1
                elif reward < 0:
                    negative += 1
            else:
                pending += 1

        print(f"\n📊 Log-Zusammenfassung: {rated} bewertet, {pending} noch offen.")
        print(f"✅ Positive Bewertungen: {positive}")
        print(f"⚠️ Negative Bewertungen: {negative}\n")

        if pending > 0:
            print("🔍 Möchtest du jetzt offene 'PENDING'-Einträge manuell bewerten?")
            response = input("➡️  Eingabe 'j' zum Starten, sonst Enter drücken: ").strip().lower()
            if response == "j":
                for i, entry in enumerate(logs):
                    reward = entry.get("reward")
                    if not isinstance(reward, (int, float)):
                        print(f"\n🔸 Eintrag {i+1}/{len(logs)}")
                        print(f"🧠 STATE: {entry['state']}")
                        print(f"🤖 ACTION: {entry['action']}")
                        print(f"📨 RESPONSE: {entry['next_state']}")
                        user_input = input("📝 Reward vergeben (1.0 = positiv, -1.0 = negativ, Enter = überspringen): ").strip()
                        if user_input:
                            try:
                                entry["reward"] = float(user_input)
                                print("✅ Reward gesetzt.")
                            except ValueError:
                                print("⚠️ Ungültiger Wert – Eintrag übersprungen.")

                with open(path, "w", encoding="utf-8") as f:
                    json.dump(logs, f, ensure_ascii=False, indent=4)
                print("\n💾 Alle neuen Bewertungen wurden gespeichert.")
            else:
                for entry in logs:
                    reward = entry.get("reward")
                    if reward == "PENDING_POSITIV":
                        entry["reward"] = 0.1
                    elif reward == "PENDING_NEGATIV":
                        entry["reward"] = -0.1
                    elif reward == "PENDING":
                        entry["reward"] = 0.0

                with open(path, "w", encoding="utf-8") as f:
                    json.dump(logs, f, ensure_ascii=False, indent=4)
                print("\n🧠 Automatische Bewertung durchgeführt (0.1 / -0.1 / 0.0).")
    except Exception as e:
        print(f"Fehler beim Zusammenfassen der Logdatei: {e}")

def clear_interaction_log(confirm=True):
    """Löscht alle Einträge in interactions.json."""
    path = os.path.join("data", "rlhf", "logs", "interactions.json")
    if not os.path.exists(path):
        print("⚠️ Keine Interaktions-Logdatei vorhanden.")
        return
    if confirm:
        response = input("⚠️ Bist du sicher, dass du alle Einträge löschen möchtest? (j/n): ").strip().lower()
        if response != "j":
            print("❌ Löschvorgang abgebrochen.")
            return
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)
        print("🗑️ interactions.json wurde geleert.")
    except Exception as e:
        print(f"Fehler beim Löschen: {e}")