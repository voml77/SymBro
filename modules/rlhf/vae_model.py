import torch
import json
import os
from datetime import datetime

def evaluate_with_vae(vae, x):
    """Berechnet den Rekonstruktionsfehler (MSE) als Outlier-Score."""
    with torch.no_grad():
        x_recon, _, _ = vae(x)
        loss = torch.nn.functional.mse_loss(x_recon, x, reduction="mean")
    return loss.item()
from .vae_model import evaluate_with_vae

class VAE(torch.nn.Module):
    def __init__(self, input_dim, latent_dim):
        super(VAE, self).__init__()
        self.encoder = torch.nn.Sequential(
            torch.nn.Linear(input_dim, 32),
            torch.nn.ReLU(),
            torch.nn.Linear(32, latent_dim * 2)
        )
        self.decoder = torch.nn.Sequential(
            torch.nn.Linear(latent_dim, 32),
            torch.nn.ReLU(),
            torch.nn.Linear(32, input_dim),
            torch.nn.Sigmoid()
        )

    def encode(self, x):
        h = self.encoder(x)
        mu, logvar = h.chunk(2, dim=-1)
        return mu, logvar

    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std

    def decode(self, z):
        return self.decoder(z)

    def forward(self, x):
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        return self.decode(z), mu, logvar

INTERACTION_PATH = "data/rlhf/logs/interactions.json"
THRESHOLD = 0.3  # Outlier-Grenze (0–1 Skala, je nach Fehler)

def load_vae(input_dim=64, latent_dim=16, model_path="data/rlhf/vae.pt"):
    vae = VAE(input_dim, latent_dim)
    if os.path.exists(model_path):
        vae.load_state_dict(torch.load(model_path))
        vae.eval()
    return vae

def extract_vector_from_state(state):
    """Einfacher Vektorizer – zählt Tokenlänge pro Nachricht."""
    if not state:
        return torch.zeros(64)
    vec = torch.zeros(64)
    for i, entry in enumerate(state[-8:]):
        content = entry.get("content", "")
        vec[i] = min(len(content), 100) / 100.0  # Normalisiert
    return vec

def detect_outliers(vae, interactions, threshold=THRESHOLD):
    outlier_indices = []
    for idx, entry in enumerate(interactions):
        vec = extract_vector_from_state(entry.get("state", [])).unsqueeze(0)
        score = evaluate_with_vae(vae, vec)
        if score < threshold:
            outlier_indices.append(idx)
    return outlier_indices

def mark_outliers_in_logs(threshold=THRESHOLD):
    if not os.path.exists(INTERACTION_PATH):
        print("Keine Interaktionen vorhanden.")
        return

    with open(INTERACTION_PATH, "r", encoding="utf-8") as f:
        interactions = json.load(f)

    vae = load_vae()
    outliers = detect_outliers(vae, interactions, threshold=threshold)

    for i in outliers:
        interactions[i]["outlier"] = True

    with open(INTERACTION_PATH, "w", encoding="utf-8") as f:
        json.dump(interactions, f, indent=2)

    print(f"Outlier-Erkennung abgeschlossen. {len(outliers)} Interaktionen markiert.")

import matplotlib.pyplot as plt

def plot_reconstruction_errors(interactions_path=INTERACTION_PATH, model_path="data/rlhf/vae.pt", threshold=THRESHOLD):
    if not os.path.exists(interactions_path):
        print("Keine Interaktionsdaten zum Visualisieren gefunden.")
        return

    with open(interactions_path, "r", encoding="utf-8") as f:
        interactions = json.load(f)

    vae = load_vae(model_path=model_path)
    errors = []
    indices = []

    for idx, entry in enumerate(interactions):
        vec = extract_vector_from_state(entry.get("state", [])).unsqueeze(0)
        error = evaluate_with_vae(vae, vec)
        errors.append(error)
        indices.append(idx)

    plt.figure(figsize=(12, 5))
    plt.plot(indices, errors, marker='o', label='Rekonstruktionsfehler')
    plt.axhline(y=threshold, color='r', linestyle='--', label=f'Threshold = {threshold}')
    plt.xlabel("Interaktion-Index")
    plt.ylabel("Fehlerwert")
    plt.title("Rekonstruktionsfehler pro Interaktion")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def get_outlier_mask(interactions, threshold=THRESHOLD, model_path="data/rlhf/vae.pt"):
    """
    Gibt eine Liste von bools zurück: True = Outlier, False = normal
    """
    if not interactions:
        return []

    vae = load_vae(model_path=model_path)
    outlier_mask = []

    for entry in interactions:
        vec = extract_vector_from_state(entry.get("state", [])).unsqueeze(0)
        score = evaluate_with_vae(vae, vec)
        outlier_mask.append(score < threshold)

    return outlier_mask
