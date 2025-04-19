import os
import json
import random
import datetime

class QLearningAgent:
    def __init__(self, state_space, action_space, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0):
        self.state_space = state_space
        self.action_space = action_space
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = exploration_rate
        self.q_table = {}

    def get_q_value(self, state, action):
        return self.q_table.get((state, action), 0.0)

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.action_space)
        else:
            q_values = [self.get_q_value(state, a) for a in self.action_space]
            max_q = max(q_values)
            return self.action_space[q_values.index(max_q)]

    def update(self, state, action, reward, next_state):
        old_q = self.get_q_value(state, action)
        future_rewards = max([self.get_q_value(next_state, a) for a in self.action_space])
        new_q = (1 - self.lr) * old_q + self.lr * (reward + self.gamma * future_rewards)
        self.q_table[(state, action)] = new_q

    def save(self, path="data/rlhf/q_table.json"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump({str(k): v for k, v in self.q_table.items()}, f)

    def load(self, path="data/rlhf/q_table.json"):
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
                self.q_table = {eval(k): v for k, v in data.items()}

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

        logs[-1]["reward"] = reward

        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=4)

        print(f"✅ Reward aktualisiert: {reward}")
    except Exception as e:
        print(f"Fehler beim Aktualisieren des Rewards: {e}")
