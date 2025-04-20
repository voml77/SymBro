import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from modules.rlhf.rlhf_engine import QLearningAgent, train_from_buffer, sync_buffer_from_logs
from modules.rlhf.replay_buffer import buffer
import pprint

# 🧠 Agent initialisieren
agent = QLearningAgent(state_space=[], action_space=[
    "antwort_1", "antwort_2", "antwort_3"
])

# 🔁 Log synchronisieren
sync_buffer_from_logs(buffer)

# 🎓 Training durchführen
train_steps = 5
for i in range(train_steps):
    print(f"\n🚀 Trainingsrunde {i+1}/{train_steps}")
    train_from_buffer(agent, buffer, batch_size=10)

# 📊 Q-Tabelle ausgeben (sortiert nach Q-Wert)
print("\n🧠 Gelernte Q-Werte:")
sorted_q = sorted(agent.q_table.items(), key=lambda x: x[1], reverse=True)
for (state_action, value) in sorted_q[:15]:
    print(f"{state_action} => {round(value, 3)}")