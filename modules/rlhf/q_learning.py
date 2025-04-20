

import json
import os
import random

Q_TABLE_PATH = "data/rlhf/q_table.json"

class QLearningAgent:
    def __init__(self, actions, learning_rate=0.1, discount_factor=0.9, exploration_rate=0.2):
        self.q_table = self.load_q_table()
        self.actions = actions
        self.alpha = learning_rate
        self.gamma = discount_factor
        self.epsilon = exploration_rate

    def load_q_table(self):
        if os.path.exists(Q_TABLE_PATH):
            with open(Q_TABLE_PATH, "r") as f:
                return json.load(f)
        return {}

    def save_q_table(self):
        with open(Q_TABLE_PATH, "w") as f:
            json.dump(self.q_table, f, indent=2)

    def get_state_key(self, state):
        return json.dumps(state, sort_keys=True)

    def choose_action(self, state):
        state_key = self.get_state_key(state)
        if random.random() < self.epsilon or state_key not in self.q_table:
            return random.choice(self.actions)
        return max(self.q_table[state_key], key=self.q_table[state_key].get)

    def update(self, state, action, reward, next_state):
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state)

        if state_key not in self.q_table:
            self.q_table[state_key] = {a: 0.0 for a in self.actions}
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = {a: 0.0 for a in self.actions}

        current_q = self.q_table[state_key][action]
        max_next_q = max(self.q_table[next_state_key].values())
        new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        self.q_table[state_key][action] = new_q