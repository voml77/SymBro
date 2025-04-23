

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from utils.embedding_analyzer import get_positive_embeddings, get_emotion_weight

def calculate_reward(sample_embedding, confidence=1.0):
    """
    Berechnet den numerischen Reward für ein Sample basierend auf:
    - Cosine Similarity zur nächsten positiv bewerteten Referenz (50%)
    - Confidence Score (30%)
    - Emotion Weight (20%)
    """
    # 1. Cosine Similarity zur nächsten positiven Referenz
    positive_embeddings = get_positive_embeddings()
    if not positive_embeddings:
        print("⚠️ Keine positiven Referenz-Embeddings vorhanden → Reward = 0.0")
        return 0.0

    sample_vec = np.array(sample_embedding).reshape(1, -1)
    pos_vecs = np.array(positive_embeddings)
    similarities = cosine_similarity(sample_vec, pos_vecs)
    max_similarity = np.max(similarities)

    # 2. Emotion Weight (z.B. aus Sentiment- oder Emoji-Analyse)
    emotion_weight = get_emotion_weight(sample_embedding)

    # 3. Reward-Berechnung
    reward = (0.5 * max_similarity) + (0.3 * confidence) + (0.2 * emotion_weight)
    return reward