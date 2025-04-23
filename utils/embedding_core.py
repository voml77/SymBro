# utils/embedding_core.py

from sentence_transformers import SentenceTransformer

# Beispiel-Modell – kannst natürlich dein eigenes nehmen:
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def generate_embedding(text):
    """
    Berechnet das Embedding für den gegebenen Text.
    """
    embedding = model.encode(text)
    return embedding