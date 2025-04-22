from sentence_transformers import SentenceTransformer, util
import numpy as np
import os
import torch

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
        _model.eval()
    return _model

# Beispielhafte Skill-Intentionen (können später geladen/erweitert werden)
skill_intents = {
    "reflect_on_user": [
        "was hast du über mich gelernt",
        "wie würdest du mich einschätzen",
        "was denkst du über mich",
        "was weißt du über meine Persönlichkeit"
    ],
    "joke_skill": [
        "erzähl mir einen witz",
        "mach einen scherz",
        "bring mich zum lachen"
    ],
    "gpt_chat": [
        "erklär mir etwas",
        "was ist künstliche intelligenz",
        "hilf mir mit einer idee"
    ]
}

# Embeddings laden oder erzeugen
embedding_dir = "data/embeddings"
os.makedirs(embedding_dir, exist_ok=True)

intent_embeddings = {}

for skill, examples in skill_intents.items():
    path = os.path.join(embedding_dir, f"{skill}_intents.npy")
    if os.path.exists(path):
        intent_embeddings[skill] = np.load(path)
    else:
        embeddings = get_model().encode(examples)
        intent_embeddings[skill] = embeddings
        np.save(path, embeddings)

def select_skill(user_input: str, threshold: float = 0.7):
    """Gibt den wahrscheinlichsten Skillnamen zurück oder 'gpt_chat' als Fallback."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    input_embedding = get_model().encode(user_input, convert_to_tensor=True).to(device)
    best_skill = "gpt_chat"
    best_score = 0.0

    for skill, embeddings in intent_embeddings.items():
        cosine_scores = util.cos_sim(input_embedding, torch.tensor(embeddings).to(input_embedding.device))
        max_score = float(torch.max(cosine_scores))

        if max_score > best_score and max_score >= threshold:
            best_skill = skill
            best_score = max_score

    return best_skill