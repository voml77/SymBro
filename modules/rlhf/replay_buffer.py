import random
import time
import heapq

class PrioritizedReplayBuffer:
    def __init__(self, capacity=1000, alpha=0.6, beta=0.4, epsilon=1e-6, decay=0.999):
        self.capacity = capacity
        self.alpha = alpha  # Prioritätsgewichtung
        self.beta = beta    # Wichtigkeit beim Sampling
        self.epsilon = epsilon
        self.decay = decay  # Zeitlicher Verfall der Priorität
        self.buffer = []
        self.next_index = 0
        self.counter = 0  # Für FIFO-Verhalten bei gleichem TD-Error

    def add(self, state, action, reward, next_state, priority):
        timestamp = time.time()
        priority = (abs(priority) + self.epsilon) ** self.alpha
        priority *= self._decay_factor(timestamp)
        experience = (priority, self.counter, timestamp, (state, action, reward, next_state))
        if len(self.buffer) < self.capacity:
            heapq.heappush(self.buffer, (-priority, self.counter, experience))
        else:
            heapq.heappushpop(self.buffer, (-priority, self.counter, experience))
        self.counter += 1

    def sample(self, batch_size=32):
        sorted_buffer = sorted(self.buffer, reverse=True)[:batch_size]
        samples = [exp[-1] for exp in sorted_buffer]
        return samples

    def _decay_factor(self, timestamp):
        age = time.time() - timestamp
        return self.decay ** age

    def __len__(self):
        return len(self.buffer)

    def update_priorities(self, updated_items):
        """
        updated_items: List of tuples (state, action, reward, next_state, new_td_error)
        """
        new_buffer = self.buffer.copy()
        for i, (priority, counter, experience) in enumerate(self.buffer):
            old_state, old_action, old_reward, old_next_state = experience[-1]
            for updated in updated_items:
                u_state, u_action, u_reward, u_next_state, new_td_error = updated
                if old_state == u_state and old_action == u_action and old_next_state == u_next_state:
                    timestamp = time.time()
                    new_priority = (abs(new_td_error) + self.epsilon) ** self.alpha
                    new_priority *= self._decay_factor(timestamp)
                    new_experience = (new_priority, counter, timestamp, (u_state, u_action, u_reward, u_next_state))
                    new_buffer[i] = (-new_priority, counter, new_experience)
                    break
        heapq.heapify(new_buffer)
        self.buffer = new_buffer

    def update(self, index, new_priority):
        if 0 <= index < len(self.buffer):
            _, counter, experience = self.buffer[index]
            timestamp = time.time()
            adjusted_priority = (abs(new_priority) + self.epsilon) ** self.alpha
            adjusted_priority *= self._decay_factor(timestamp)
            new_experience = (adjusted_priority, counter, timestamp, experience[-1])
            self.buffer[index] = (-adjusted_priority, counter, new_experience)

    def update_priorities_from_indices(self, indices, priorities):
        for idx, new_td_error in zip(indices, priorities):
            self.update(idx, new_td_error)

    def clear(self):
        """Leert den Replay Buffer."""
        self.buffer = []
        self.counter = 0
        self.next_index = 0

    def save_to_file(self, filepath):
        import pickle
        with open(filepath, "wb") as f:
            pickle.dump(self.buffer, f)
        print(f"💾 ReplayBuffer gespeichert unter {filepath}")

    def load_from_file(self, filepath):
        import pickle
        with open(filepath, "rb") as f:
            self.buffer = pickle.load(f)
        print(f"📥 ReplayBuffer geladen von {filepath}")
