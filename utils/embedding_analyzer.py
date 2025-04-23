import os
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sentence_transformers import SentenceTransformer

# utils/embedding_analyzer.py

import numpy as np

def load_embeddings_from_embeddings_file(filepath="data/rlhf/embeddings.json"):
    if not os.path.exists(filepath):
        print(f"⚠️ Datei {filepath} nicht gefunden.")
        return [], []
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    embeddings = [np.array(entry["embedding"]) for entry in data if "embedding" in entry]
    labels = [entry.get("outlier_weight", 1.0) for entry in data]
    return embeddings, labels

def get_outlier_weight(embedding, use_knn=True, n_neighbors=5):
    embedding = np.array(embedding)
    if embedding.ndim == 3:
        embedding = embedding.squeeze()
    if embedding.ndim == 1:
        embedding = embedding.reshape(1, -1)

    embeddings, _ = load_embeddings_from_embeddings_file()

    if len(embeddings) < n_neighbors + 1:
        print("⚠️ Outlier-Check übersprungen – zu wenige Vergleichsembeddings.")
        return 1.0

    embeddings = [np.array(e) for e in embeddings]
    embeddings = [e.squeeze() if e.ndim == 3 else e for e in embeddings]
    embeddings = [e.reshape(1, -1) if e.ndim == 1 else e for e in embeddings]
    embeddings = np.vstack(embeddings)

    nbrs = NearestNeighbors(n_neighbors=n_neighbors).fit(embeddings)

    distances_all, _ = nbrs.kneighbors(embeddings)
    mean_distances_all = distances_all.mean(axis=1)
    mean = mean_distances_all.mean()
    std = mean_distances_all.std()

    distances, _ = nbrs.kneighbors(embedding)
    mean_distance = distances.mean()

    deviation = (mean_distance - mean)
    factor = 1.5  # Justierbarer Streckfaktor
    scaling = deviation / (std * factor) if std > 0 else 0
    weight = 1.0 - scaling
    weight = max(0.1, min(1.0, weight))  # Clamp

    print(f"🎯 Outlier-Weight: {weight:.3f} (mean_distance: {mean_distance:.3f}, μ: {mean:.3f}, σ: {std:.3f})")

    return weight

def is_outlier(embedding, threshold=0.5):
    """Optional: True, wenn Gewicht unterhalb des Schwellenwerts."""
    return get_outlier_weight(embedding) < threshold

# Modell initialisieren
model = SentenceTransformer('all-MiniLM-L6-v2')

def load_embeddings_from_interactions(filepath="data/rlhf/logs/interactions.json"):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"{filepath} not found.")
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    embeddings = []
    labels = []
    for entry in data:
        text = str(entry.get("state", "")) + " " + str(entry.get("action", "")) + " " + str(entry.get("next_state", ""))
        embedding = model.encode(text)
        reward = entry.get("reward", "PENDING")
        labels.append(reward)
        embeddings.append(embedding)
    return np.array(embeddings), labels

def reduce_and_plot(embeddings, labels, method="pca"):
    if method == "pca":
        reducer = PCA(n_components=2)
    elif method == "tsne":
        reducer = TSNE(n_components=2, random_state=42)
    else:
        raise ValueError("method must be 'pca' or 'tsne'")
    
    reduced = reducer.fit_transform(embeddings)
    
    colors = {"PENDING": "gray", 1.0: "green", -1.0: "red"}
    plt.figure(figsize=(8, 6))
    for reward in set(labels):
        idx = [i for i, r in enumerate(labels) if r == reward]
        plt.scatter(reduced[idx, 0], reduced[idx, 1], label=str(reward), alpha=0.6, color=colors.get(reward, "blue"))
    
    plt.legend(title="Reward")
    plt.title(f"Embedding Visualisierung ({method.upper()})")
    plt.xlabel("Komponente 1")
    plt.ylabel("Komponente 2")
    plt.show()


from sklearn.neighbors import NearestNeighbors

def knn_outlier_detection(embeddings, n_neighbors=5):
    embeddings = np.array(embeddings)
    nbrs = NearestNeighbors(n_neighbors=n_neighbors).fit(embeddings)
    distances, _ = nbrs.kneighbors(embeddings)
    mean_distances = distances.mean(axis=1)
    threshold = np.percentile(mean_distances, 95)  # Top 5% als Outlier
    outliers = mean_distances > threshold
    return outliers

if __name__ == "__main__":
    embeddings, labels = load_embeddings_from_interactions()
    
    print(f"🔢 Anzahl der Datenpunkte: {len(embeddings)}")
    
    if len(embeddings) < 600:
        print("🟢 KNN Outlier Detection mit PCA aktiviert (weniger als 600 Datenpunkte).")
        reduced = PCA(n_components=2).fit_transform(embeddings)
        reduce_and_plot(embeddings, labels, method="pca")
        
        outliers = knn_outlier_detection(reduced)
        print(f"🚩 Erkannte Outlier (KNN): {np.sum(outliers)} von {len(embeddings)}")
        
        # Optional: Outlier visualisieren
        plt.figure(figsize=(8, 6))
        colors = np.where(outliers, "red", "blue")
        plt.scatter(reduced[:, 0], reduced[:, 1], c=colors, alpha=0.6)
        plt.title("KNN Outlier Detection (PCA-reduziert)")
        plt.xlabel("Komponente 1")
        plt.ylabel("Komponente 2")
        plt.show()

    else:
        print("🟠 t-SNE Visualisierung und VAE Outlier Detection aktiviert (600+ Datenpunkte).")
        reduce_and_plot(embeddings, labels, method="tsne")
        
        from utils.vae_model import vae_outlier_detection  # VAE-Funktion annehmen
        outliers = vae_outlier_detection(embeddings)
        print(f"🚩 Erkannte Outlier (VAE): {np.sum(outliers)} von {len(embeddings)}")

        # Visualisierung der VAE-Outlier
        plt.figure(figsize=(8, 6))
        colors = np.where(outliers, "red", "blue")
        plt.scatter(reduced[:, 0], reduced[:, 1], c=colors, alpha=0.6)
        plt.title("VAE Outlier Detection (t-SNE-reduziert)")
        plt.xlabel("Komponente 1")
        plt.ylabel("Komponente 2")
        plt.show()