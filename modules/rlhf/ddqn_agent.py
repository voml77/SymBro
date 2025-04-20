import numpy as np
import random
import torch
import torch.nn as nn
import torch.optim as optim

class LSTM_QNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(LSTM_QNetwork, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        h_0 = torch.zeros(1, x.size(0), 64).to(x.device)
        c_0 = torch.zeros(1, x.size(0), 64).to(x.device)
        lstm_out, _ = self.lstm(x, (h_0, c_0))
        out = self.fc(lstm_out[:, -1, :])
        return out

class DDQNAgent:
    def __init__(self, state_size, action_size, gamma=0.99, epsilon=1.0, epsilon_min=0.1, epsilon_decay=0.995):
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay

        self.q_network = LSTM_QNetwork(state_size, 64, action_size)
        self.target_network = LSTM_QNetwork(state_size, 64, action_size)
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=0.001)
        self.criterion = nn.MSELoss()
        self.update_target_network()

    def update_target_network(self):
        # Placeholder: Später echte Netzwerk-Kopie
        self.target_network = self.q_network

    def select_action(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        # Placeholder: Später Vorhersage mit q_network
        return np.argmax(np.random.rand(self.action_size))  # Dummy-Wahl

    def train_step(self, batch):
        # Placeholder für Trainingslogik
        # batch = (states, actions, rewards, next_states, dones)
        pass

    def decay_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
